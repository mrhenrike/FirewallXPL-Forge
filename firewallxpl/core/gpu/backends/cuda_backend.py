"""NVIDIA CUDA compute backend via PyTorch.

Requires: pip install firewallxpl[gpu-nvidia] (torch + cupy)

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import logging
from typing import List

from firewallxpl.core.gpu.backends.base import ComputeBackend

logger = logging.getLogger("firewallxpl.gpu.backends.cuda")


class CUDABackend(ComputeBackend):
    """NVIDIA CUDA GPU backend."""

    name: str = "cuda"
    device_name: str = "NVIDIA GPU"
    memory_mb: int = 0

    def __init__(self, device_id: int = 0) -> None:
        self._device_id = device_id
        self._torch = None

    def is_available(self) -> bool:
        try:
            import torch
            if torch.cuda.is_available():
                self._torch = torch
                self.device_name = torch.cuda.get_device_name(self._device_id)
                props = torch.cuda.get_device_properties(self._device_id)
                self.memory_mb = props.total_memory // (1024 * 1024)
                return True
        except (ImportError, RuntimeError):
            pass
        return False

    def hash_batch(self, algo: str, candidates: List[bytes], target_hash: bytes) -> List[int]:
        from firewallxpl.core.gpu.backends.cpu_backend import CPUBackend
        return CPUBackend().hash_batch(algo, candidates, target_hash)

    def encode_batch(self, algo: str, payloads: List[bytes]) -> List[bytes]:
        from firewallxpl.core.gpu.backends.cpu_backend import CPUBackend
        return CPUBackend().encode_batch(algo, payloads)

    def regex_batch(self, pattern: str, texts: List[str]) -> List[bool]:
        from firewallxpl.core.gpu.backends.cpu_backend import CPUBackend
        return CPUBackend().regex_batch(pattern, texts)

    def benchmark(self) -> float:
        if not self._torch:
            return 0.0
        import time
        torch = self._torch
        device = torch.device(f"cuda:{self._device_id}")
        a = torch.randn(1024, 1024, device=device)
        torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(100):
            torch.mm(a, a)
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        return (100 * 1024 * 1024 * 1024) / elapsed if elapsed > 0 else 0.0
