"""Advanced offline Wi-Fi attack parsers and utilities.

Extracts WEP IVs, PMKID hashes, TKIP MIC parameters, SAE/Dragonfly
commits (WPA3 Dragonblood) and EAP/PEAP/MSCHAPv2 identity+challenge
pairs from PCAP/PCAPNG captures for offline processing.

Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("firewallxpl.pcap.wifi_offline")

try:
    from scapy.all import (
        Dot11,
        Dot11Beacon,
        Dot11ProbeResp,
        Dot11WEP,
        Dot11Elt,
        Dot11Auth,
        EAPOL,
        EAP,
        IP,
        Raw,
        rdpcap,
    )
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


# =====================================================================
# Data classes
# =====================================================================

@dataclass
class WEPIVSample:
    """A single WEP initialisation vector + first encrypted byte."""
    bssid: str
    iv: bytes  # 3 bytes
    key_index: int
    first_encrypted_byte: int
    packet_index: int


@dataclass
class WEPAnalysis:
    """Aggregated WEP IV extraction result."""
    bssid: str
    ssid: str
    iv_count: int
    unique_ivs: int
    weak_ivs: int  # FMS-vulnerable IVs
    samples: List[WEPIVSample] = field(default_factory=list)

    @property
    def crackable_fms(self) -> bool:
        """FMS attack generally needs ~60k-80k unique IVs (weak) or ~40k with PTW."""
        return self.unique_ivs >= 5000

    @property
    def crackable_ptw(self) -> bool:
        """PTW attack needs far fewer IVs (~20k-40k data packets)."""
        return self.iv_count >= 20000


@dataclass
class PMKIDEntry:
    """A PMKID extracted from the first EAPOL message (RSN PMKID)."""
    bssid: str
    client_mac: str
    ssid: str
    pmkid: str  # hex
    hashcat_line: str  # mode 22000 format


@dataclass
class TKIPMICInfo:
    """TKIP MIC parameters for Michael attack analysis."""
    bssid: str
    client_mac: str
    ssid: str
    mic_failures_detected: int
    qos_data_packets: int
    tkip_fragments: int
    chopchop_candidate: bool
    beck_tews_feasible: bool


@dataclass
class SAECommit:
    """SAE (Simultaneous Authentication of Equals) commit frame data for Dragonblood analysis."""
    bssid: str
    client_mac: str
    ssid: str
    group_id: int
    scalar: bytes
    element: bytes
    anti_clogging_token: Optional[bytes]
    timestamp_us: float
    frame_index: int


@dataclass
class DragonbloodAnalysis:
    """Dragonblood timing/cache side-channel analysis result."""
    bssid: str
    ssid: str
    commits: List[SAECommit]
    timing_deltas_us: List[float]
    group_downgrade_detected: bool
    transition_mode_detected: bool
    timing_variance_suspicious: bool

    @property
    def vulnerability_indicators(self) -> List[str]:
        indicators = []
        if self.group_downgrade_detected:
            indicators.append("CVE-2019-9494: SAE group downgrade")
        if self.transition_mode_detected:
            indicators.append("CVE-2019-9496: WPA3 transition mode downgrade to WPA2")
        if self.timing_variance_suspicious and len(self.commits) >= 3:
            indicators.append("CVE-2019-9494: Timing side-channel in SAE handshake (Dragonblood)")
        if any(c.group_id in (1, 2, 5, 22) for c in self.commits):
            indicators.append("Weak group usage detected (NIST curves with known implementation issues)")
        return indicators


@dataclass
class EAPIdentity:
    """EAP identity and challenge-response data for WPE-style offline cracking."""
    bssid: str
    client_mac: str
    ssid: str
    eap_type: str  # PEAP, EAP-TTLS, EAP-MD5, MSCHAPv2, LEAP, EAP-FAST
    identity: str
    challenge: Optional[bytes]
    response: Optional[bytes]
    success: Optional[bool]
    hashcat_line: str  # for offline cracking


# =====================================================================
# WEP IV extraction
# =====================================================================

def _is_weak_iv_fms(iv: bytes) -> bool:
    """Check if IV is weak per FMS (Fluhrer-Mantin-Shamir) criteria."""
    if len(iv) < 3:
        return False
    a, b, _ = iv[0], iv[1], iv[2]
    # Classic FMS: (A+3, N-1, X) pattern
    return b == 255 and a >= 3 and a <= 15


def extract_wep_ivs(packets: List[Any]) -> Dict[str, WEPAnalysis]:
    """Extract WEP initialisation vectors from encrypted data frames.

    Args:
        packets: List of scapy packets.

    Returns:
        Dict mapping BSSID to WEPAnalysis.
    """
    results: Dict[str, WEPAnalysis] = {}

    # First pass: get SSIDs from beacons
    ssid_map: Dict[str, str] = {}
    for pkt in packets:
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = (pkt[Dot11].addr3 or "").upper()
            elt = pkt.getlayer(Dot11Elt)
            while elt:
                if elt.ID == 0:
                    try:
                        ssid_map[bssid] = elt.info.decode("utf-8", errors="replace").strip("\x00")
                    except Exception:
                        pass
                    break
                elt = elt.payload.getlayer(Dot11Elt)

    for idx, pkt in enumerate(packets):
        if not pkt.haslayer(Dot11):
            continue
        if not pkt.haslayer(Dot11WEP):
            continue

        dot11 = pkt[Dot11]
        wep = pkt[Dot11WEP]

        # Determine BSSID
        to_ds = dot11.FCfield & 0x1
        from_ds = dot11.FCfield & 0x2
        if to_ds and not from_ds:
            bssid = (dot11.addr1 or "").upper()
        elif from_ds and not to_ds:
            bssid = (dot11.addr2 or "").upper()
        else:
            bssid = (dot11.addr3 or dot11.addr1 or "").upper()

        if not bssid:
            continue

        iv = bytes(wep)[:3] if len(bytes(wep)) >= 3 else b"\x00\x00\x00"
        key_idx = (bytes(wep)[3] >> 6) & 0x3 if len(bytes(wep)) >= 4 else 0
        first_enc = bytes(wep)[4] if len(bytes(wep)) >= 5 else 0

        if bssid not in results:
            results[bssid] = WEPAnalysis(
                bssid=bssid,
                ssid=ssid_map.get(bssid, ""),
                iv_count=0,
                unique_ivs=0,
                weak_ivs=0,
            )

        analysis = results[bssid]
        sample = WEPIVSample(
            bssid=bssid,
            iv=iv,
            key_index=key_idx,
            first_encrypted_byte=first_enc,
            packet_index=idx,
        )
        analysis.samples.append(sample)
        analysis.iv_count += 1

        if _is_weak_iv_fms(iv):
            analysis.weak_ivs += 1

    # Count unique IVs
    for analysis in results.values():
        seen: Set[bytes] = set()
        for s in analysis.samples:
            seen.add(s.iv)
        analysis.unique_ivs = len(seen)

    return results


# =====================================================================
# PMKID extraction (WPA/WPA2 clientless attack)
# =====================================================================

def extract_pmkid(packets: List[Any], ssid_map: Optional[Dict[str, str]] = None) -> List[PMKIDEntry]:
    """Extract PMKID from the first EAPOL message (AP → client).

    The PMKID is in the RSN Key Data of EAPOL message 1 when the AP
    includes it (most modern APs do). This enables clientless WPA attacks
    (hashcat mode 22000 / hcxtools).

    Args:
        packets: List of scapy packets.
        ssid_map: Optional BSSID → SSID mapping.

    Returns:
        List of PMKIDEntry objects.
    """
    if ssid_map is None:
        ssid_map = {}
        for pkt in packets:
            if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                bssid = (pkt[Dot11].addr3 or "").upper()
                elt = pkt.getlayer(Dot11Elt)
                while elt:
                    if elt.ID == 0:
                        try:
                            ssid_map[bssid] = elt.info.decode("utf-8", errors="replace").strip("\x00")
                        except Exception:
                            pass
                        break
                    elt = elt.payload.getlayer(Dot11Elt)

    results: List[PMKIDEntry] = []

    for pkt in packets:
        if not pkt.haslayer(EAPOL):
            continue
        if not pkt.haslayer(Dot11):
            continue

        eapol_raw = bytes(pkt[EAPOL])
        if len(eapol_raw) < 99:
            continue

        # Check if message 1 (ack set, mic not set)
        try:
            key_info = struct.unpack("!H", eapol_raw[5:7])[0]
        except struct.error:
            continue

        ack = bool(key_info & (1 << 7))
        mic = bool(key_info & (1 << 8))

        if not (ack and not mic):
            continue  # Not message 1

        # Key data starts at offset 99 in EAPOL-Key
        key_data_len = struct.unpack("!H", eapol_raw[97:99])[0] if len(eapol_raw) >= 99 else 0
        if key_data_len == 0 or len(eapol_raw) < 99 + key_data_len:
            continue

        key_data = eapol_raw[99:99 + key_data_len]

        # Search for PMKID RSN KDE: type=0xdd, OUI=00:0f:ac, data_type=4
        pmkid = _find_pmkid_in_key_data(key_data)
        if not pmkid:
            continue

        dot11 = pkt[Dot11]
        # Message 1: AP → Client, so addr1=client, addr2=AP(BSSID)
        to_ds = dot11.FCfield & 0x1
        from_ds = dot11.FCfield & 0x2
        if from_ds and not to_ds:
            bssid = (dot11.addr2 or "").upper()
            client = (dot11.addr1 or "").upper()
        else:
            bssid = (dot11.addr3 or dot11.addr2 or "").upper()
            client = (dot11.addr1 or dot11.addr2 or "").upper()

        ssid = ssid_map.get(bssid, "")
        pmkid_hex = pmkid.hex()

        # hashcat 22000 format: WPA*02*PMKID*MAC_AP*MAC_STA*ESSID_HEX
        essid_hex = ssid.encode("utf-8").hex() if ssid else ""
        mac_ap = bssid.replace(":", "").lower()
        mac_sta = client.replace(":", "").lower()
        hashcat_line = "WPA*02*{}*{}*{}*{}".format(pmkid_hex, mac_ap, mac_sta, essid_hex)

        results.append(PMKIDEntry(
            bssid=bssid,
            client_mac=client,
            ssid=ssid,
            pmkid=pmkid_hex,
            hashcat_line=hashcat_line,
        ))

    return results


def _find_pmkid_in_key_data(key_data: bytes) -> Optional[bytes]:
    """Search for PMKID RSN KDE tag inside EAPOL key data."""
    offset = 0
    while offset < len(key_data) - 2:
        tag_type = key_data[offset]
        if tag_type == 0xdd:
            tag_len = key_data[offset + 1] if offset + 1 < len(key_data) else 0
            if tag_len >= 20 and offset + 2 + tag_len <= len(key_data):
                oui = key_data[offset + 2:offset + 5]
                data_type = key_data[offset + 5]
                if oui == b"\x00\x0f\xac" and data_type == 4:
                    return key_data[offset + 6:offset + 6 + 16]
            offset += 2 + tag_len
        elif tag_type == 0x30:
            tag_len = key_data[offset + 1] if offset + 1 < len(key_data) else 0
            offset += 2 + tag_len
        else:
            break
    return None


# =====================================================================
# TKIP / Michael attack analysis
# =====================================================================

def analyze_tkip_vulnerabilities(packets: List[Any], ssid_map: Optional[Dict[str, str]] = None) -> List[TKIPMICInfo]:
    """Analyze PCAP for TKIP MIC weaknesses (Beck-Tews / Ohigashi-Morii / ChopChop).

    Args:
        packets: List of scapy packets.
        ssid_map: Optional BSSID → SSID mapping.

    Returns:
        List of TKIPMICInfo per detected TKIP network.
    """
    if ssid_map is None:
        ssid_map = _build_ssid_map(packets)

    tkip_networks: Dict[str, TKIPMICInfo] = {}

    for pkt in packets:
        if not pkt.haslayer(Dot11):
            continue

        dot11 = pkt[Dot11]

        # Detect TKIP from beacons/probe responses
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = (dot11.addr3 or "").upper()
            if _uses_tkip(pkt):
                if bssid not in tkip_networks:
                    tkip_networks[bssid] = TKIPMICInfo(
                        bssid=bssid,
                        client_mac="",
                        ssid=ssid_map.get(bssid, ""),
                        mic_failures_detected=0,
                        qos_data_packets=0,
                        tkip_fragments=0,
                        chopchop_candidate=False,
                        beck_tews_feasible=False,
                    )
            continue

        # Count QoS data frames for TKIP networks (needed for Beck-Tews)
        if dot11.type == 2:  # Data frame
            to_ds = dot11.FCfield & 0x1
            from_ds = dot11.FCfield & 0x2
            bssid = ""
            client = ""
            if to_ds and not from_ds:
                bssid = (dot11.addr1 or "").upper()
                client = (dot11.addr2 or "").upper()
            elif from_ds and not to_ds:
                bssid = (dot11.addr2 or "").upper()
                client = (dot11.addr1 or "").upper()

            if bssid in tkip_networks:
                info = tkip_networks[bssid]
                if client:
                    info.client_mac = client

                # QoS data: subtype 8 (QoS Data) or 12 (QoS Null)
                if dot11.subtype in (8, 12):
                    info.qos_data_packets += 1

                # Check for MIC failure indication (deauth reason 14)
                more_fragments = bool(dot11.FCfield & 0x4)
                if more_fragments:
                    info.tkip_fragments += 1

        # Detect MIC failure deauth (reason code 14)
        if dot11.subtype == 12 and dot11.type == 0:  # Deauthentication
            try:
                reason = struct.unpack("<H", bytes(pkt[Dot11])[24:26])[0]
                if reason == 14:  # MIC failure
                    bssid = (dot11.addr3 or dot11.addr1 or "").upper()
                    if bssid in tkip_networks:
                        tkip_networks[bssid].mic_failures_detected += 1
            except Exception:
                pass

    # Assess feasibility
    for info in tkip_networks.values():
        # Beck-Tews: needs QoS data frames, works on TKIP-only or mixed mode
        info.beck_tews_feasible = info.qos_data_packets >= 10
        # ChopChop: works when we have encrypted data frames
        info.chopchop_candidate = info.qos_data_packets >= 1 or info.tkip_fragments >= 1

    return list(tkip_networks.values())


def _uses_tkip(pkt: Any) -> bool:
    """Check if beacon/probe-response advertises TKIP cipher."""
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        # RSN (ID 48) or WPA vendor (ID 221, OUI 00:50:f2:01)
        if elt.ID == 48 and elt.info:
            if b"\x00\x0f\xac\x02" in bytes(elt.info):  # TKIP suite
                return True
        elif elt.ID == 221 and elt.info and elt.info[:4] == b"\x00\x50\xf2\x01":
            if b"\x00\x50\xf2\x02" in bytes(elt.info):  # TKIP (WPA1)
                return True
        elt = elt.payload.getlayer(Dot11Elt)
    return False


# =====================================================================
# WPA3 / SAE / Dragonblood
# =====================================================================

def extract_sae_commits(packets: List[Any], ssid_map: Optional[Dict[str, str]] = None) -> DragonbloodAnalysis:
    """Extract SAE (Dragonfly) commit frames for Dragonblood analysis.

    Detects CVE-2019-9494 (timing side-channel), CVE-2019-9496 (transition
    mode downgrade) and weak group usage from captured SAE authentication frames.

    Args:
        packets: List of scapy packets.
        ssid_map: Optional BSSID → SSID mapping.

    Returns:
        DragonbloodAnalysis with commits and vulnerability indicators.
    """
    if ssid_map is None:
        ssid_map = _build_ssid_map(packets)

    commits: List[SAECommit] = []
    timestamps: List[float] = []
    transition_mode = False
    group_downgrade = False
    seen_groups: Set[int] = set()
    primary_bssid = ""
    last_ts: float = 0.0

    for idx, pkt in enumerate(packets):
        if not pkt.haslayer(Dot11):
            continue
        if not pkt.haslayer(Dot11Auth):
            continue

        dot11 = pkt[Dot11]
        auth = pkt[Dot11Auth]

        # SAE uses algo=3 (SAE) or algo=4 (SAE with FT)
        if auth.algo not in (3, 4):
            # Check for transition mode: WPA3 AP also accepts algo=0 (Open)
            if auth.algo == 0:
                bssid = (dot11.addr3 or dot11.addr1 or "").upper()
                if bssid and bssid in ssid_map:
                    transition_mode = True
            continue

        # seq_num 1 = Commit, seq_num 2 = Confirm
        if auth.seqnum != 1:
            continue

        bssid = (dot11.addr3 or dot11.addr1 or "").upper()
        client = (dot11.addr2 or "").upper()
        if not primary_bssid:
            primary_bssid = bssid

        # Parse SAE commit body (after auth header)
        body = bytes(auth.payload) if auth.payload else b""
        if len(body) < 36:
            continue

        # SAE commit: group_id(2) + anti_clogging_token(variable) + scalar(32) + element(64)
        group_id = struct.unpack("<H", body[0:2])[0]
        seen_groups.add(group_id)

        # Simplified: assume no anti-clogging token for initial commit
        scalar = body[2:34]
        element = body[34:98] if len(body) >= 98 else body[34:]
        anti_clogging = None

        ts = float(pkt.time) * 1e6 if hasattr(pkt, "time") else idx * 1000.0

        commits.append(SAECommit(
            bssid=bssid,
            client_mac=client,
            ssid=ssid_map.get(bssid, ""),
            group_id=group_id,
            scalar=scalar,
            element=element,
            anti_clogging_token=anti_clogging,
            timestamp_us=ts,
            frame_index=idx,
        ))

        if last_ts > 0:
            timestamps.append(ts - last_ts)
        last_ts = ts

    # Check group downgrade: if multiple groups seen, attacker may force weaker group
    if len(seen_groups) > 1:
        group_downgrade = True

    # Timing analysis: high variance in commit timing may indicate cache/timing side-channel
    timing_suspicious = False
    if len(timestamps) >= 3:
        avg = sum(timestamps) / len(timestamps)
        variance = sum((t - avg) ** 2 for t in timestamps) / len(timestamps)
        std_dev = variance ** 0.5
        # Coefficient of variation > 0.5 is suspicious
        if avg > 0 and (std_dev / avg) > 0.5:
            timing_suspicious = True

    return DragonbloodAnalysis(
        bssid=primary_bssid,
        ssid=ssid_map.get(primary_bssid, ""),
        commits=commits,
        timing_deltas_us=timestamps,
        group_downgrade_detected=group_downgrade,
        transition_mode_detected=transition_mode,
        timing_variance_suspicious=timing_suspicious,
    )


# =====================================================================
# WPE — EAP/PEAP/MSCHAPv2 identity + challenge harvest
# =====================================================================

def extract_eap_identities(packets: List[Any], ssid_map: Optional[Dict[str, str]] = None) -> List[EAPIdentity]:
    """Extract EAP identities and challenge-response pairs for WPE-style offline attacks.

    Captures EAP-PEAP, EAP-TTLS, EAP-MD5, LEAP and MSCHAPv2 exchanges
    from PCAPs (typically from evil-twin / rogue AP captures).

    Args:
        packets: List of scapy packets.
        ssid_map: Optional BSSID → SSID mapping.

    Returns:
        List of EAPIdentity objects.
    """
    if ssid_map is None:
        ssid_map = _build_ssid_map(packets)

    EAP_TYPE_MAP = {
        1: "EAP-Identity",
        4: "EAP-MD5",
        13: "EAP-TLS",
        17: "LEAP",
        21: "EAP-TTLS",
        25: "PEAP",
        26: "MSCHAPv2",
        43: "EAP-FAST",
    }

    sessions: Dict[str, Dict[str, Any]] = {}  # keyed by client_mac
    results: List[EAPIdentity] = []

    for pkt in packets:
        if not pkt.haslayer(EAP):
            continue

        eap = pkt[EAP]
        eap_code = eap.code  # 1=Request, 2=Response, 3=Success, 4=Failure
        eap_type = eap.type if hasattr(eap, "type") else 0

        bssid = ""
        client = ""
        if pkt.haslayer(Dot11):
            dot11 = pkt[Dot11]
            to_ds = dot11.FCfield & 0x1
            from_ds = dot11.FCfield & 0x2
            if to_ds and not from_ds:
                bssid = (dot11.addr1 or "").upper()
                client = (dot11.addr2 or "").upper()
            elif from_ds and not to_ds:
                bssid = (dot11.addr2 or "").upper()
                client = (dot11.addr1 or "").upper()
            else:
                bssid = (dot11.addr3 or "").upper()
                client = (dot11.addr2 or "").upper()

        if not client:
            continue

        session = sessions.setdefault(client, {
            "bssid": bssid,
            "identity": "",
            "eap_type": "",
            "challenge": None,
            "response": None,
            "success": None,
        })

        if bssid:
            session["bssid"] = bssid

        eap_payload = bytes(eap.payload) if eap.payload else b""

        # Identity response
        if eap_code == 2 and eap_type == 1:
            identity = eap_payload.decode("utf-8", errors="replace").strip("\x00").strip()
            if identity:
                session["identity"] = identity

        # EAP-MD5 Challenge
        elif eap_type == 4:
            if eap_code == 1 and len(eap_payload) >= 17:  # Request with challenge
                value_size = eap_payload[0]
                session["challenge"] = eap_payload[1:1 + value_size]
                session["eap_type"] = "EAP-MD5"
            elif eap_code == 2 and len(eap_payload) >= 17:  # Response
                value_size = eap_payload[0]
                session["response"] = eap_payload[1:1 + value_size]

        # LEAP
        elif eap_type == 17:
            session["eap_type"] = "LEAP"
            if eap_code == 1 and len(eap_payload) >= 11:
                session["challenge"] = eap_payload[3:11]  # 8-byte challenge
            elif eap_code == 2 and len(eap_payload) >= 27:
                session["response"] = eap_payload[3:27]  # 24-byte response

        # MSCHAPv2 (inside EAP or standalone)
        elif eap_type == 26:
            session["eap_type"] = "MSCHAPv2"
            if len(eap_payload) >= 4:
                mschap_opcode = eap_payload[0]
                if mschap_opcode == 1 and len(eap_payload) >= 20:  # Challenge
                    session["challenge"] = eap_payload[4:20]
                elif mschap_opcode == 2 and len(eap_payload) >= 54:  # Response
                    session["response"] = eap_payload[4:54]  # peer challenge + NT response

        # PEAP / EAP-TTLS (mark the type, inner auth extracted above if decrypted)
        elif eap_type in (21, 25):
            session["eap_type"] = EAP_TYPE_MAP.get(eap_type, "PEAP/TTLS")

        # EAP-FAST
        elif eap_type == 43:
            session["eap_type"] = "EAP-FAST"

        # Success/Failure
        if eap_code == 3:
            session["success"] = True
        elif eap_code == 4:
            session["success"] = False

    # Build results from sessions with identities or challenge/response
    for client_mac, sess in sessions.items():
        if not sess["identity"] and not sess["challenge"]:
            continue

        bssid = sess["bssid"]
        ssid = ssid_map.get(bssid, "")
        eap_type = sess["eap_type"] or "Unknown"

        hashcat_line = ""
        if sess["challenge"] and sess["response"]:
            if eap_type == "MSCHAPv2":
                # NetNTLMv1 / MSCHAPv2 hashcat format (mode 5500)
                hashcat_line = "{}::::{}:{}".format(
                    sess["identity"] or "unknown",
                    sess["response"].hex(),
                    sess["challenge"].hex(),
                )
            elif eap_type == "LEAP":
                hashcat_line = "{}:$LEAP${}${}".format(
                    sess["identity"] or "unknown",
                    sess["challenge"].hex(),
                    sess["response"].hex(),
                )
            elif eap_type == "EAP-MD5":
                hashcat_line = "{}:$MD5${}${}".format(
                    sess["identity"] or "unknown",
                    sess["challenge"].hex(),
                    sess["response"].hex(),
                )

        results.append(EAPIdentity(
            bssid=bssid,
            client_mac=client_mac,
            ssid=ssid,
            eap_type=eap_type,
            identity=sess["identity"],
            challenge=sess["challenge"],
            response=sess["response"],
            success=sess["success"],
            hashcat_line=hashcat_line,
        ))

    return results


# =====================================================================
# Shared helpers
# =====================================================================

def _build_ssid_map(packets: List[Any]) -> Dict[str, str]:
    """Build BSSID → SSID mapping from beacons/probe-responses."""
    ssid_map: Dict[str, str] = {}
    for pkt in packets:
        if not pkt.haslayer(Dot11):
            continue
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = (pkt[Dot11].addr3 or "").upper()
            elt = pkt.getlayer(Dot11Elt)
            while elt:
                if elt.ID == 0:
                    try:
                        ssid_map[bssid] = elt.info.decode("utf-8", errors="replace").strip("\x00")
                    except Exception:
                        pass
                    break
                elt = elt.payload.getlayer(Dot11Elt)
    return ssid_map
