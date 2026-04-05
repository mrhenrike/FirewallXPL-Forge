"""Core PCAP/PCAPNG parsing utilities for offline wireless analysis.

Provides structured extraction of 802.11 frames, EAPOL handshakes,
cleartext credentials, and AP/station mapping from capture files.

Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""

from __future__ import annotations

import logging
import os
import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("firewallxpl.pcap")

try:
    from scapy.all import (
        PcapReader,
        PcapNgReader,
        rdpcap,
        Dot11,
        Dot11Beacon,
        Dot11ProbeReq,
        Dot11ProbeResp,
        Dot11AssoReq,
        Dot11AssoResp,
        Dot11Auth,
        Dot11Deauth,
        Dot11Elt,
        EAPOL,
        TCP,
        UDP,
        Raw,
        IP,
        conf as scapy_conf,
    )

    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

SUPPORTED_EXTENSIONS = {".pcap", ".pcapng", ".cap", ".dump"}


# ---------------------------------------------------------------------------
# Data classes for structured output
# ---------------------------------------------------------------------------

@dataclass
class AccessPoint:
    """Represents a discovered wireless access point."""

    bssid: str
    ssid: str = ""
    channel: int = 0
    encryption: str = "OPEN"
    cipher: str = ""
    auth: str = ""
    beacon_count: int = 0
    vendor_oui: str = ""

    @property
    def key(self) -> str:
        return self.bssid.upper()


@dataclass
class Station:
    """Represents a wireless client station."""

    mac: str
    associated_bssid: str = ""
    probed_ssids: Set[str] = field(default_factory=set)
    data_frames: int = 0

    @property
    def key(self) -> str:
        return self.mac.upper()


@dataclass
class EAPOLHandshake:
    """Represents a captured WPA/WPA2 4-way handshake."""

    bssid: str
    client_mac: str
    ssid: str = ""
    messages: List[int] = field(default_factory=list)
    packets: List[Any] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        """A usable handshake needs at least messages 1+2 or 2+3."""
        msg_set = set(self.messages)
        return ({1, 2}.issubset(msg_set) or {2, 3}.issubset(msg_set))

    @property
    def completeness(self) -> str:
        unique = sorted(set(self.messages))
        if len(unique) == 4:
            return "full"
        if self.is_complete:
            return "partial_usable"
        return "incomplete"


@dataclass
class ExtractedCredential:
    """Represents a cleartext credential found in traffic."""

    protocol: str
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    username: str = ""
    password: str = ""
    extra: str = ""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _detect_encryption(packet: Any) -> Tuple[str, str, str]:
    """Derive encryption, cipher and auth from beacon/probe-response IEs."""
    encryption = "OPEN"
    cipher = ""
    auth = ""

    cap = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                         "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").strip()
    has_privacy = "privacy" in cap.lower() if cap else False

    rsn_found = False
    wpa_found = False
    elt = packet.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 48:  # RSN (WPA2)
            rsn_found = True
            cipher, auth = _parse_rsn_wpa_ie(bytes(elt.info))
        elif elt.ID == 221 and elt.info and elt.info[:4] == b"\x00\x50\xf2\x01":
            wpa_found = True
            if not rsn_found:
                cipher, auth = _parse_rsn_wpa_ie(bytes(elt.info[4:]))
        elt = elt.payload.getlayer(Dot11Elt)

    if rsn_found:
        encryption = "WPA2"
    elif wpa_found:
        encryption = "WPA"
    elif has_privacy:
        encryption = "WEP"

    return encryption, cipher, auth


def _parse_rsn_wpa_ie(data: bytes) -> Tuple[str, str]:
    """Extract cipher suite and AKM from RSN/WPA IE body."""
    cipher_map = {1: "WEP-40", 2: "TKIP", 4: "CCMP", 5: "WEP-104"}
    akm_map = {1: "MGT", 2: "PSK"}
    cipher = ""
    auth = ""
    try:
        if len(data) < 10:
            return cipher, auth
        offset = 2  # version
        offset += 4  # group cipher suite
        pw_count = struct.unpack("<H", data[offset:offset + 2])[0]
        offset += 2
        for _ in range(pw_count):
            suite_type = data[offset + 3]
            cipher = cipher_map.get(suite_type, "CIPHER-{}".format(suite_type))
            offset += 4
        akm_count = struct.unpack("<H", data[offset:offset + 2])[0]
        offset += 2
        for _ in range(akm_count):
            akm_type = data[offset + 3]
            auth = akm_map.get(akm_type, "AKM-{}".format(akm_type))
            offset += 4
    except (struct.error, IndexError):
        pass
    return cipher, auth


def _extract_ssid(packet: Any) -> str:
    """Extract SSID from Dot11Elt layer."""
    elt = packet.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 0:
            try:
                return elt.info.decode("utf-8", errors="replace").strip("\x00")
            except Exception:
                return ""
        elt = elt.payload.getlayer(Dot11Elt)
    return ""


def _extract_channel(packet: Any) -> int:
    """Extract channel from DS Parameter Set IE."""
    elt = packet.getlayer(Dot11Elt)
    while elt:
        if elt.ID == 3 and elt.info:
            return elt.info[0]
        elt = elt.payload.getlayer(Dot11Elt)
    return 0


def _classify_eapol_message(raw_eapol: bytes) -> int:
    """Determine EAPOL 4-way handshake message number (1-4)."""
    if len(raw_eapol) < 99:
        return 0
    try:
        key_info = struct.unpack("!H", raw_eapol[5:7])[0]
    except struct.error:
        return 0

    install = bool(key_info & (1 << 6))
    ack = bool(key_info & (1 << 7))
    mic = bool(key_info & (1 << 8))
    secure = bool(key_info & (1 << 9))

    if ack and not mic:
        return 1
    if mic and not ack and not install and not secure:
        return 2
    if ack and mic and install and secure:
        return 3
    if mic and not ack and secure:
        return 4
    return 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_pcap_path(file_path: str) -> Path:
    """Validate that file_path points to a supported capture file.

    Args:
        file_path: Path to the capture file.

    Returns:
        Resolved Path object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the extension is unsupported or scapy is missing.
    """
    if not SCAPY_AVAILABLE:
        raise ValueError(
            "scapy is required for PCAP analysis. "
            "Install it with: pip install scapy"
        )
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError("Capture file not found: {}".format(path))
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported capture format '{}'. Supported: {}".format(
                path.suffix, ", ".join(sorted(SUPPORTED_EXTENSIONS))
            )
        )
    return path


def load_packets(file_path: str, max_packets: int = 0) -> List[Any]:
    """Load packets from a PCAP/PCAPNG file.

    Args:
        file_path: Path to the capture file.
        max_packets: Maximum number of packets to read (0 = unlimited).

    Returns:
        List of scapy packet objects.
    """
    path = validate_pcap_path(file_path)
    logger.info("Loading capture file: %s", path)
    packets = rdpcap(str(path), count=max_packets if max_packets > 0 else -1)
    logger.info("Loaded %d packets from %s", len(packets), path.name)
    return list(packets)


def extract_access_points(packets: List[Any]) -> Dict[str, AccessPoint]:
    """Extract all access points from 802.11 beacon and probe-response frames.

    Args:
        packets: List of scapy packets.

    Returns:
        Dict mapping BSSID to AccessPoint.
    """
    aps: Dict[str, AccessPoint] = {}
    for pkt in packets:
        if not pkt.haslayer(Dot11):
            continue
        if not (pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp)):
            continue

        bssid = pkt[Dot11].addr3
        if not bssid:
            continue
        bssid = bssid.upper()

        ssid = _extract_ssid(pkt)
        channel = _extract_channel(pkt)
        encryption, cipher, auth = _detect_encryption(pkt)

        if bssid in aps:
            ap = aps[bssid]
            ap.beacon_count += 1
            if ssid and not ap.ssid:
                ap.ssid = ssid
            if channel and not ap.channel:
                ap.channel = channel
        else:
            aps[bssid] = AccessPoint(
                bssid=bssid,
                ssid=ssid,
                channel=channel,
                encryption=encryption,
                cipher=cipher,
                auth=auth,
                beacon_count=1,
            )
    return aps


def extract_stations(packets: List[Any]) -> Dict[str, Station]:
    """Extract client stations from 802.11 frames.

    Args:
        packets: List of scapy packets.

    Returns:
        Dict mapping station MAC to Station.
    """
    broadcast = {"FF:FF:FF:FF:FF:FF", "00:00:00:00:00:00"}
    stations: Dict[str, Station] = {}

    for pkt in packets:
        if not pkt.haslayer(Dot11):
            continue

        dot11 = pkt[Dot11]
        frame_type = dot11.type
        frame_subtype = dot11.subtype

        # Probe requests → station with probed SSID
        if pkt.haslayer(Dot11ProbeReq):
            src = (dot11.addr2 or "").upper()
            if src and src not in broadcast:
                sta = stations.setdefault(src, Station(mac=src))
                ssid = _extract_ssid(pkt)
                if ssid:
                    sta.probed_ssids.add(ssid)
            continue

        # Data frames (type 2) → station associated to AP
        if frame_type == 2:
            to_ds = dot11.FCfield & 0x1
            from_ds = dot11.FCfield & 0x2

            if to_ds and not from_ds:
                client_mac = (dot11.addr2 or "").upper()
                bssid = (dot11.addr1 or "").upper()
            elif from_ds and not to_ds:
                client_mac = (dot11.addr1 or "").upper()
                bssid = (dot11.addr2 or "").upper()
            else:
                continue

            if client_mac and client_mac not in broadcast:
                sta = stations.setdefault(client_mac, Station(mac=client_mac))
                if bssid:
                    sta.associated_bssid = bssid
                sta.data_frames += 1

    return stations


def extract_eapol_handshakes(
    packets: List[Any],
    ap_map: Optional[Dict[str, AccessPoint]] = None,
) -> List[EAPOLHandshake]:
    """Extract WPA/WPA2 4-way EAPOL handshakes from capture.

    Args:
        packets: List of scapy packets.
        ap_map: Optional AP mapping to resolve SSIDs.

    Returns:
        List of EAPOLHandshake objects grouped by (BSSID, client_mac).
    """
    handshakes: Dict[Tuple[str, str], EAPOLHandshake] = {}

    for pkt in packets:
        if not pkt.haslayer(EAPOL):
            continue
        if not pkt.haslayer(Dot11):
            continue

        dot11 = pkt[Dot11]
        eapol_raw = bytes(pkt[EAPOL])
        msg_num = _classify_eapol_message(eapol_raw)
        if msg_num == 0:
            continue

        to_ds = dot11.FCfield & 0x1
        from_ds = dot11.FCfield & 0x2

        if to_ds and not from_ds:
            client_mac = (dot11.addr2 or "").upper()
            bssid = (dot11.addr1 or "").upper()
        elif from_ds and not to_ds:
            client_mac = (dot11.addr1 or "").upper()
            bssid = (dot11.addr2 or "").upper()
        else:
            bssid = (dot11.addr3 or dot11.addr1 or "").upper()
            client_mac = (dot11.addr2 or "").upper()

        key = (bssid, client_mac)
        hs = handshakes.setdefault(
            key,
            EAPOLHandshake(bssid=bssid, client_mac=client_mac),
        )
        hs.messages.append(msg_num)
        hs.packets.append(pkt)

        if ap_map and bssid in ap_map and not hs.ssid:
            hs.ssid = ap_map[bssid].ssid

    return list(handshakes.values())


def extract_cleartext_credentials(packets: List[Any]) -> List[ExtractedCredential]:
    """Extract cleartext credentials from TCP streams (HTTP, FTP, Telnet, SNMP).

    Args:
        packets: List of scapy packets.

    Returns:
        List of ExtractedCredential objects.
    """
    creds: List[ExtractedCredential] = []
    ftp_sessions: Dict[Tuple[str, str], Dict[str, str]] = {}

    for pkt in packets:
        if not pkt.haslayer(IP):
            continue
        if not pkt.haslayer(Raw):
            continue

        ip_layer = pkt[IP]
        payload = bytes(pkt[Raw].load)

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            continue

        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        src_port = pkt[TCP].sport if pkt.haslayer(TCP) else (pkt[UDP].sport if pkt.haslayer(UDP) else 0)
        dst_port = pkt[TCP].dport if pkt.haslayer(TCP) else (pkt[UDP].dport if pkt.haslayer(UDP) else 0)

        # HTTP Basic Auth
        auth_match = re.search(r"Authorization:\s*Basic\s+([A-Za-z0-9+/=]+)", text, re.IGNORECASE)
        if auth_match:
            import base64
            try:
                decoded = base64.b64decode(auth_match.group(1)).decode("utf-8", errors="replace")
                user, _, pwd = decoded.partition(":")
                creds.append(ExtractedCredential(
                    protocol="HTTP-Basic",
                    src_ip=src_ip, dst_ip=dst_ip,
                    src_port=src_port, dst_port=dst_port,
                    username=user, password=pwd,
                ))
            except Exception:
                pass

        # HTTP form POST body (common patterns)
        if dst_port in (80, 8080, 443) or "POST" in text[:10]:
            form_user = re.search(
                r"(?:user(?:name)?|login|email)=([^&\s]+)", text, re.IGNORECASE
            )
            form_pass = re.search(
                r"(?:pass(?:word)?|pwd|passwd)=([^&\s]+)", text, re.IGNORECASE
            )
            if form_user and form_pass:
                creds.append(ExtractedCredential(
                    protocol="HTTP-Form",
                    src_ip=src_ip, dst_ip=dst_ip,
                    src_port=src_port, dst_port=dst_port,
                    username=form_user.group(1),
                    password=form_pass.group(1),
                ))

        # FTP USER/PASS
        if dst_port == 21 or src_port == 21:
            session_key = (src_ip, dst_ip) if dst_port == 21 else (dst_ip, src_ip)
            ftp_user_match = re.match(r"USER\s+(.+)\r?\n", text, re.IGNORECASE)
            ftp_pass_match = re.match(r"PASS\s+(.+)\r?\n", text, re.IGNORECASE)
            if ftp_user_match:
                ftp_sessions.setdefault(session_key, {})["user"] = ftp_user_match.group(1).strip()
            if ftp_pass_match:
                ftp_sessions.setdefault(session_key, {})["pass"] = ftp_pass_match.group(1).strip()

        # Telnet (raw login patterns)
        if dst_port == 23 or src_port == 23:
            login_match = re.search(r"(?:login|username):\s*(\S+)", text, re.IGNORECASE)
            pass_match = re.search(r"(?:password|passwd):\s*(\S+)", text, re.IGNORECASE)
            if login_match:
                creds.append(ExtractedCredential(
                    protocol="Telnet",
                    src_ip=src_ip, dst_ip=dst_ip,
                    src_port=src_port, dst_port=dst_port,
                    username=login_match.group(1),
                    password=pass_match.group(1) if pass_match else "",
                ))

        # SNMP community strings (v1/v2c) in UDP payload
        if pkt.haslayer(UDP) and (dst_port == 161 or src_port == 161):
            snmp_match = re.search(rb"[\x04]([\x20-\x7e]{2,32})", payload)
            if snmp_match:
                community = snmp_match.group(1).decode("ascii", errors="ignore")
                creds.append(ExtractedCredential(
                    protocol="SNMP",
                    src_ip=src_ip, dst_ip=dst_ip,
                    src_port=src_port, dst_port=dst_port,
                    username="", password="",
                    extra="community={}".format(community),
                ))

    # Consolidate FTP sessions
    for (client_ip, server_ip), session in ftp_sessions.items():
        if "user" in session:
            creds.append(ExtractedCredential(
                protocol="FTP",
                src_ip=client_ip, dst_ip=server_ip,
                src_port=0, dst_port=21,
                username=session.get("user", ""),
                password=session.get("pass", ""),
            ))

    return creds


def save_handshake_pcap(
    handshake: EAPOLHandshake,
    output_path: str,
    include_beacons: Optional[List[Any]] = None,
) -> Path:
    """Save EAPOL handshake packets to a standalone PCAP for cracking.

    Args:
        handshake: The EAPOLHandshake to export.
        output_path: Destination file path.
        include_beacons: Optional beacon packets to include (needed by some tools).

    Returns:
        Path to the written PCAP file.
    """
    from scapy.all import wrpcap

    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    pkts = []
    if include_beacons:
        pkts.extend(include_beacons)
    pkts.extend(handshake.packets)

    wrpcap(str(out), pkts)
    logger.info("Saved %d packets to %s", len(pkts), out)
    return out
