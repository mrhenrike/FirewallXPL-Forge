"""Managed process pool for CPU-bound tasks in FirewallXPL-Forge.

Wraps concurrent.futures.ProcessPoolExecutor for hash computation,
payload generation, and wordlist mutation.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ProcessPoolExecutor, Future
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("firewallxpl.concurrency.process_pool")


class ManagedProcessPool:
    """Process pool for CPU-intensive operations."""

    def __init__(self, max_workers: Optional[int] = None) -> None:
        """Initialize with optional worker count (defaults to CPU count)."""
        self.max_workers: int = max_workers or min(os.cpu_count() or 1, 8)
        self._executor: Optional[ProcessPoolExecutor] = None
        self._submitted: int = 0
        self._completed: int = 0

    def start(self) -> None:
        """Start the process pool."""
        if self._executor is None:
            self._executor = ProcessPoolExecutor(max_workers=self.max_workers)

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """Submit a CPU-bound task."""
        if self._executor is None:
            self.start()
        self._submitted += 1
        future = self._executor.submit(fn, *args, **kwargs)
        future.add_done_callback(lambda _: setattr(self, '_completed', self._completed + 1))
        return future

    def map(self, fn: Callable[..., Any], iterables: Any, chunksize: int = 1) -> Any:
        """Map function over iterables using process pool."""
        if self._executor is None:
            self.start()
        return self._executor.map(fn, iterables, chunksize=chunksize)

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the pool."""
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None

    @property
    def metrics(self) -> Dict[str, int]:
        return {
            "max_workers": self.max_workers,
            "submitted": self._submitted,
            "completed": self._completed,
        }

    def __enter__(self) -> "ManagedProcessPool":
        self.start()
        return self

    def __exit__(self, *args: Any) -> None:
        self.shutdown(wait=True)
