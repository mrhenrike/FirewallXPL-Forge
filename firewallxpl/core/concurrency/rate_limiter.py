"""Token bucket rate limiter for scan throttling.

Controls request rate to avoid overwhelming targets or triggering IDS/IPS.
Supports both sync and async usage.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Optional


class TokenBucket:
    """Token bucket algorithm for rate limiting.

    Args:
        rate: Minimum seconds between requests (inverse of requests/sec).
        burst: Maximum burst capacity (tokens). Defaults to 1.
    """

    def __init__(self, rate: float, burst: int = 1) -> None:
        self.rate: float = max(rate, 0.001)
        self.burst: int = max(burst, 1)
        self._tokens: float = float(burst)
        self._last_time: float = time.monotonic()
        self._lock: threading.Lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_time
        self._tokens = min(self.burst, self._tokens + elapsed / self.rate)
        self._last_time = now

    def acquire(self) -> None:
        """Block until a token is available (sync)."""
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
            time.sleep(self.rate * 0.1)

    async def acquire_async(self) -> None:
        """Await until a token is available (async)."""
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
            await asyncio.sleep(self.rate * 0.1)

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens
