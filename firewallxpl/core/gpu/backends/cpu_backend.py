"""CPU fallback compute backend — always available, zero extra dependencies.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import hashlib
import re
import time
from typing import List

from firewallxpl.core.gpu.backends.base import ComputeBackend


class CPUBackend(ComputeBackend):
    """Pure CPU compute backend using stdlib."""

    name: str = "cpu"
    device_name: str = "CPU"
    memory_mb: int = 0

    def is_available(self) -> bool:
        return True

    def hash_batch(self, algo: str, candidates: List[bytes], target_hash: bytes) -> List[int]:
        """Hash candidates on CPU and return matching indices."""
        matches = []
        for i, c in enumerate(candidates):
            h = hashlib.new(algo, c).digest()
            if h == target_hash:
                matches.append(i)
        return matches

    def encode_batch(self, algo: str, payloads: List[bytes]) -> List[bytes]:
        """Encode payloads on CPU."""
        import base64
        results = []
        for p in payloads:
            if algo == "base64":
                results.append(base64.b64encode(p))
            elif algo == "hex":
                results.append(p.hex().encode())
            else:
                results.append(p)
        return results

    def regex_batch(self, pattern: str, texts: List[str]) -> List[bool]:
        """Match regex pattern against texts on CPU."""
        compiled = re.compile(pattern)
        return [bool(compiled.search(t)) for t in texts]

    def benchmark(self) -> float:
        """Benchmark CPU with MD5 hashing."""
        data = b"FirewallXPL-Forge-Benchmark"
        start = time.perf_counter()
        for _ in range(100_000):
            hashlib.md5(data).digest()
        elapsed = time.perf_counter() - start
        return 100_000 / elapsed if elapsed > 0 else 0.0
