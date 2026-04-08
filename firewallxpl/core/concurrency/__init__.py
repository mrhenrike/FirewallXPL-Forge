"""Concurrency engine for FirewallXPL-Forge.

Provides async I/O, thread/process pools, connection pooling, rate limiting,
and pipeline orchestration for multi-target scanning.

Author: André Henrique (@mrhenrike) | União Geek
"""

from firewallxpl.core.concurrency.async_engine import AsyncScanEngine
from firewallxpl.core.concurrency.thread_pool import ManagedThreadPool
from firewallxpl.core.concurrency.process_pool import ManagedProcessPool
from firewallxpl.core.concurrency.rate_limiter import TokenBucket
from firewallxpl.core.concurrency.pipeline import ScanPipeline

__all__ = [
    "AsyncScanEngine",
    "ManagedThreadPool",
    "ManagedProcessPool",
    "TokenBucket",
    "ScanPipeline",
]
