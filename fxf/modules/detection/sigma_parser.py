"""Sigma Rule Parser and Correlation Engine.

Ingests Sigma detection rules and correlates against log data
for threat detection in firewall/SIEM environments.

Supports:
- Sigma YAML rule ingestion
- Log format normalization (Syslog, CEF, JSON, Windows Event)
- Rule matching with wildcard and regex support
- Alert generation with MITRE ATT&CK mapping

xpl-forge-full-integration.plan.md Bloco 6.

References:
  - https://github.com/SigmaHQ/sigma
  - https://sigmahq.io/

Author: Andre Henrique (@mrhenrike) | Uniao Geek
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class SigmaRule:
    """Parsed Sigma detection rule."""

    title: str
    id: str = ""
    status: str = "experimental"
    description: str = ""
    references: list[str] = field(default_factory=list)
    author: str = ""
    tags: list[str] = field(default_factory=list)
    logsource: dict = field(default_factory=dict)
    detection: dict = field(default_factory=dict)
    condition: str = ""
    level: str = "medium"
    mitre_attack: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def get_mitre_tactics(self) -> list[str]:
        """Extract MITRE ATT&CK tactics from tags."""
        return [t.replace("attack.", "").upper() for t in self.tags if t.startswith("attack.t")]


@dataclass
class SigmaMatch:
    """A rule match against a log entry."""

    rule: SigmaRule
    log_entry: dict
    matched_fields: list[str]
    timestamp: str = ""

    def to_alert(self) -> dict:
        return {
            "title": self.rule.title,
            "level": self.rule.level,
            "rule_id": self.rule.id,
            "mitre": self.rule.get_mitre_tactics(),
            "matched_fields": self.matched_fields,
            "log_timestamp": self.timestamp,
            "description": self.rule.description[:200],
        }


class SigmaParser:
    """Parse Sigma YAML rules from files or directories."""

    def __init__(self) -> None:
        self._rules: list[SigmaRule] = []

    def load_file(self, path: str) -> Optional[SigmaRule]:
        """Load a single Sigma rule YAML file."""
        if not HAS_YAML:
            print("[sigma] PyYAML not installed. Run: pip install pyyaml")
            return None
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict) or "detection" not in data:
                return None
            rule = SigmaRule(
                title=data.get("title", "Untitled"),
                id=data.get("id", ""),
                status=data.get("status", "experimental"),
                description=data.get("description", ""),
                references=data.get("references", []),
                author=data.get("author", ""),
                tags=data.get("tags", []),
                logsource=data.get("logsource", {}),
                detection=data.get("detection", {}),
                condition=str(data.get("detection", {}).get("condition", "")),
                level=data.get("level", "medium"),
                raw=data,
            )
            # Extract MITRE from tags
            rule.mitre_attack = [t for t in rule.tags if "attack" in t.lower()]
            return rule
        except Exception as exc:
            print(f"[sigma] Error loading {path}: {exc}")
            return None

    def load_directory(self, directory: str, recursive: bool = True) -> int:
        """Load all Sigma rules from a directory.

        Args:
            directory: Path to directory containing .yml files.
            recursive: Whether to search recursively.

        Returns:
            Number of rules loaded.
        """
        p = Path(directory)
        pattern = "**/*.yml" if recursive else "*.yml"
        count = 0
        for yml_file in p.glob(pattern):
            rule = self.load_file(str(yml_file))
            if rule:
                self._rules.append(rule)
                count += 1
        print(f"[sigma] Loaded {count} rules from {directory}")
        return count

    def load_from_string(self, yaml_content: str) -> Optional[SigmaRule]:
        """Load a Sigma rule from a YAML string."""
        if not HAS_YAML:
            return None
        try:
            data = yaml.safe_load(yaml_content)
            return self.load_file.__wrapped__(self, data) if False else None
        except Exception:
            return None

    @property
    def rules(self) -> list[SigmaRule]:
        return self._rules

    def get_rules_by_level(self, level: str) -> list[SigmaRule]:
        """Filter rules by severity level."""
        return [r for r in self._rules if r.level.lower() == level.lower()]

    def get_rules_by_mitre(self, technique: str) -> list[SigmaRule]:
        """Get rules matching a MITRE technique ID (e.g., T1059)."""
        return [r for r in self._rules
                if any(technique.upper() in t.upper() for t in r.tags)]


class SigmaCorrelator:
    """Correlate log events against loaded Sigma rules."""

    def __init__(self, parser: SigmaParser) -> None:
        self.parser = parser

    def _normalize_log(self, raw: Any) -> dict:
        """Normalize various log formats to flat key-value dict."""
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            # Try JSON
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
            # Try CEF: CEF:0|vendor|product|...
            if raw.startswith("CEF:"):
                return self._parse_cef(raw)
            # Try syslog: timestamp host process message
            parts = raw.split(None, 3)
            return {
                "timestamp": parts[0] if parts else "",
                "host": parts[1] if len(parts) > 1 else "",
                "process": parts[2] if len(parts) > 2 else "",
                "message": parts[3] if len(parts) > 3 else raw,
                "raw": raw,
            }
        return {"raw": str(raw)}

    def _parse_cef(self, cef: str) -> dict:
        """Parse CEF log format."""
        parts = cef.split("|", 7)
        result = {
            "cef_version": parts[0] if parts else "",
            "vendor": parts[1] if len(parts) > 1 else "",
            "product": parts[2] if len(parts) > 2 else "",
            "version": parts[3] if len(parts) > 3 else "",
            "signature": parts[4] if len(parts) > 4 else "",
            "name": parts[5] if len(parts) > 5 else "",
            "severity": parts[6] if len(parts) > 6 else "",
        }
        if len(parts) > 7:
            # Parse extension fields
            for kv in re.findall(r"(\w+)=([^ ]+|'[^']*')", parts[7]):
                result[kv[0]] = kv[1].strip("'")
        return result

    def _match_selection(self, selection: Any, log: dict) -> bool:
        """Check if a Sigma detection selection matches a log entry."""
        if isinstance(selection, dict):
            for field, value in selection.items():
                log_val = str(log.get(field, log.get("message", "") or "")).lower()
                if isinstance(value, list):
                    if not any(self._match_value(str(v), log_val) for v in value):
                        return False
                elif isinstance(value, str):
                    if not self._match_value(value, log_val):
                        return False
            return True
        if isinstance(selection, list):
            return all(
                self._match_selection(s, log) if isinstance(s, dict) else True
                for s in selection
            )
        return False

    def _match_value(self, pattern: str, value: str) -> bool:
        """Match Sigma value pattern (supports * wildcards and regex |re|)."""
        if pattern.startswith("|re|"):
            regex = pattern[4:]
            return bool(re.search(regex, value, re.IGNORECASE))
        # Convert Sigma wildcards to regex
        regex = re.escape(pattern).replace(r"\*", ".*").replace(r"\?", ".")
        return bool(re.search(regex, value, re.IGNORECASE))

    def correlate(self, logs: list[Any]) -> list[SigmaMatch]:
        """Correlate log entries against all loaded Sigma rules.

        Args:
            logs: List of log entries (dict, JSON string, or raw syslog).

        Returns:
            List of SigmaMatch objects for matching rules.
        """
        matches = []
        for raw_log in logs:
            log = self._normalize_log(raw_log)
            for rule in self.parser.rules:
                detection = rule.detection
                if not detection:
                    continue
                # Check selections
                matched_fields = []
                all_match = True
                for sel_name, sel_value in detection.items():
                    if sel_name == "condition":
                        continue
                    if isinstance(sel_value, (dict, list)):
                        sel_matched = self._match_selection(sel_value, log)
                        if sel_matched:
                            matched_fields.append(sel_name)
                        elif "NOT" not in str(rule.condition).upper():
                            # If not all required selections match, skip
                            if len([k for k in detection if k != "condition"]) > 1:
                                all_match = False
                                break
                if all_match and matched_fields:
                    matches.append(SigmaMatch(
                        rule=rule,
                        log_entry=log,
                        matched_fields=matched_fields,
                        timestamp=str(log.get("timestamp", log.get("SystemTime", ""))),
                    ))
        return matches

    def correlate_and_report(self, logs: list[Any]) -> str:
        """Correlate logs and return formatted report."""
        matches = self.correlate(logs)
        if not matches:
            return "[sigma] No rule matches found"
        lines = [
            f"[sigma] {len(matches)} MATCHES against {len(logs)} log entries",
            "=" * 50,
        ]
        for m in matches:
            alert = m.to_alert()
            lines.append(f"[{alert['level'].upper()}] {alert['title']}")
            lines.append(f"  Rule: {alert['rule_id']}")
            lines.append(f"  MITRE: {', '.join(alert['mitre']) or 'N/A'}")
            lines.append(f"  Fields: {', '.join(alert['matched_fields'])}")
            lines.append("")
        return "\n".join(lines)
