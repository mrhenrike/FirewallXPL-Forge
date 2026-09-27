"""Abstract base class for compute backends.

Defines unified interface for hash cracking, pattern matching, encoding,
and benchmarking across CPU/GPU hardware.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class ComputeBackend(ABC):
    """Unified compute abstraction — same API regardless of hardware."""

    name: str = "base"
    device_name: str = "Unknown"
    memory_mb: int = 0

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this backend is functional."""
        ...

    @abstractmethod
    def hash_batch(self, algo: str, candidates: List[bytes], target_hash: bytes) -> List[int]:
        """Hash candidates and return indices that match target_hash."""
        ...

    @abstractmethod
    def encode_batch(self, algo: str, payloads: List[bytes]) -> List[bytes]:
        """Encode payloads using specified algorithm."""
        ...

    @abstractmethod
    def regex_batch(self, pattern: str, texts: List[str]) -> List[bool]:
        """Match pattern against texts, return bool per text."""
        ...

    @abstractmethod
    def benchmark(self) -> float:
        """Return ops/s on standard workload."""
        ...
