"""Reusable connection pools for HTTP, SSH, and other protocols.

Maintains keep-alive connections to reduce handshake overhead during
multi-module scans against the same target.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Dict, Optional

logger = logging.getLogger("firewallxpl.concurrency.connection_pool")

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False


class HTTPConnectionPool:
    """Pooled HTTP session with keep-alive and retry logic."""

    def __init__(
        self,
        pool_size: int = 20,
        retries: int = 2,
        backoff_factor: float = 0.3,
        timeout: float = 10.0,
    ) -> None:
        self.pool_size: int = pool_size
        self.timeout: float = timeout
        self._sessions: Dict[str, Any] = {}
        self._lock: threading.Lock = threading.Lock()
        self._retries: int = retries
        self._backoff: float = backoff_factor

    def get_session(self, target: str) -> Any:
        """Get or create a pooled session for a target."""
        if not _HAS_REQUESTS:
            raise RuntimeError("requests library not available")

        with self._lock:
            if target not in self._sessions:
                session = requests.Session()
                retry = Retry(
                    total=self._retries,
                    backoff_factor=self._backoff,
                    status_forcelist=[500, 502, 503, 504],
                )
                adapter = HTTPAdapter(
                    pool_connections=self.pool_size,
                    pool_maxsize=self.pool_size,
                    max_retries=retry,
                )
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                session.verify = False
                self._sessions[target] = session
            return self._sessions[target]

    def close(self, target: Optional[str] = None) -> None:
        """Close sessions for a target or all targets."""
        with self._lock:
            if target:
                session = self._sessions.pop(target, None)
                if session:
                    session.close()
            else:
                for s in self._sessions.values():
                    s.close()
                self._sessions.clear()

    @property
    def active_count(self) -> int:
        return len(self._sessions)

    def __enter__(self) -> "HTTPConnectionPool":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
