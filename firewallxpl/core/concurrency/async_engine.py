"""Async scan engine using asyncio for I/O-bound module execution.

Orchestrates concurrent module execution with semaphore-based concurrency control,
rate limiting, and multi-target support via asyncio.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Optional

from firewallxpl.core.concurrency.rate_limiter import TokenBucket

logger = logging.getLogger("firewallxpl.concurrency.async_engine")


@dataclass
class ScanResult:
    """Result from a single module execution against a target."""
    target: str
    module_name: str
    status: str  # "vulnerable", "not_vulnerable", "error", "timeout", "inconclusive"
    details: str = ""
    port: int = 0
    protocol: str = ""
    creds: Optional[List[tuple]] = None


class AsyncScanEngine:
    """Orchestrates async module execution with semaphore-based concurrency."""

    def __init__(
        self,
        max_concurrent: int = 50,
        rate_limit: float = 0.0,
        timeout_per_module: float = 20.0,
    ) -> None:
        """Initialize async engine.

        Args:
            max_concurrent: Maximum simultaneous coroutines.
            rate_limit: Minimum seconds between requests (0 = unlimited).
            timeout_per_module: Per-module timeout in seconds.
        """
        self.max_concurrent: int = max_concurrent
        self.timeout_per_module: float = timeout_per_module
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._rate_limiter: Optional[TokenBucket] = None
        if rate_limit > 0:
            self._rate_limiter = TokenBucket(rate_limit)
        self._results: List[ScanResult] = []

    async def run_module(
        self,
        module_fn: Callable[..., Any],
        target: str,
        module_name: str,
        **kwargs: Any,
    ) -> ScanResult:
        """Execute a single module with concurrency and rate control."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)

        async with self._semaphore:
            if self._rate_limiter:
                await self._rate_limiter.acquire_async()
            try:
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, module_fn, target, **kwargs),
                    timeout=self.timeout_per_module,
                )
                return ScanResult(
                    target=target,
                    module_name=module_name,
                    status="vulnerable" if result is True else "not_vulnerable",
                )
            except asyncio.TimeoutError:
                logger.warning("Module %s timed out on %s", module_name, target)
                return ScanResult(
                    target=target, module_name=module_name, status="timeout"
                )
            except Exception as exc:
                logger.error("Module %s error on %s: %s", module_name, target, exc)
                return ScanResult(
                    target=target,
                    module_name=module_name,
                    status="error",
                    details=str(exc),
                )

    async def run_batch(
        self,
        modules: List[Dict[str, Any]],
        targets: List[str],
    ) -> List[ScanResult]:
        """Execute all modules against all targets concurrently.

        Args:
            modules: List of dicts with 'fn' (callable) and 'name' (str).
            targets: List of target IP/hostname strings.

        Returns:
            Aggregated list of ScanResult.
        """
        tasks = []
        for target in targets:
            for mod in modules:
                tasks.append(
                    self.run_module(mod["fn"], target, mod["name"])
                )
        self._results = await asyncio.gather(*tasks)
        return list(self._results)

    def run_sync(
        self,
        modules: List[Dict[str, Any]],
        targets: List[str],
    ) -> List[ScanResult]:
        """Synchronous wrapper for run_batch."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.run_batch(modules, targets))
                    return future.result()
        except RuntimeError:
            pass
        return asyncio.run(self.run_batch(modules, targets))
