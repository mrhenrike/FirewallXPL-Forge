"""Managed thread pool with metrics for FirewallXPL-Forge.

Wraps concurrent.futures.ThreadPoolExecutor with task counting,
error tracking, and graceful shutdown.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("firewallxpl.concurrency.thread_pool")


class ManagedThreadPool:
    """Thread pool with built-in metrics and controlled lifecycle."""

    def __init__(self, max_workers: int = 8, name: str = "fxf-pool") -> None:
        self.max_workers: int = max_workers
        self.name: str = name
        self._executor: Optional[ThreadPoolExecutor] = None
        self._lock: threading.Lock = threading.Lock()
        self._submitted: int = 0
        self._completed: int = 0
        self._errors: int = 0
        self._futures: List[Future] = []

    def start(self) -> None:
        """Start the thread pool."""
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(
                    max_workers=self.max_workers,
                    thread_name_prefix=self.name,
                )

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """Submit a task to the pool."""
        if self._executor is None:
            self.start()
        future = self._executor.submit(fn, *args, **kwargs)
        with self._lock:
            self._submitted += 1
            self._futures.append(future)
        future.add_done_callback(self._on_complete)
        return future

    def _on_complete(self, future: Future) -> None:
        with self._lock:
            self._completed += 1
            if future.exception() is not None:
                self._errors += 1

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the pool gracefully."""
        if self._executor:
            self._executor.shutdown(wait=wait, cancel_futures=not wait)
            self._executor = None

    @property
    def metrics(self) -> Dict[str, int]:
        """Return pool metrics."""
        with self._lock:
            return {
                "max_workers": self.max_workers,
                "submitted": self._submitted,
                "completed": self._completed,
                "errors": self._errors,
                "pending": self._submitted - self._completed,
            }

    def __enter__(self) -> "ManagedThreadPool":
        self.start()
        return self

    def __exit__(self, *args: Any) -> None:
        self.shutdown(wait=True)
