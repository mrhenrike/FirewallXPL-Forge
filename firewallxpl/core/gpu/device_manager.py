"""GPU device manager — orchestrates compute backends using hardware discovery.

Provides compute mode selection (cpu/gpu/hybrid) and backend routing
based on detected hardware.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from firewallxpl.core.gpu.hw_discovery import HardwareDiscovery, HardwareProfile
from firewallxpl.core.gpu.backends.base import ComputeBackend
from firewallxpl.core.gpu.backends.cpu_backend import CPUBackend

logger = logging.getLogger("firewallxpl.gpu.device_manager")

VALID_COMPUTE_MODES = ("cpu", "gpu", "hybrid")


class GPUDeviceManager:
    """Orchestrates compute backends using hardware discovery data."""

    def __init__(
        self,
        discovery: Optional[HardwareDiscovery] = None,
        compute_mode: str = "cpu",
    ) -> None:
        self._discovery = discovery or HardwareDiscovery()
        self._compute_mode = compute_mode if compute_mode in VALID_COMPUTE_MODES else "cpu"
        self._backends: Dict[str, ComputeBackend] = {}
        self._cpu_backend = CPUBackend()
        self._profile: Optional[HardwareProfile] = None

    def initialize(self, force_rediscover: bool = False) -> None:
        """Initialize hardware discovery and load backends."""
        self._profile = self._discovery.discover(force=force_rediscover)
        self._backends["cpu"] = self._cpu_backend
        self._load_gpu_backends()

    def _load_gpu_backends(self) -> None:
        """Attempt to load GPU backends based on discovered hardware."""
        if not self._profile:
            return

        for gpu in self._profile.gpus:
            if not gpu.python_backend_ok:
                continue
            if gpu.compute_api == "cuda" and "cuda" not in self._backends:
                try:
                    from firewallxpl.core.gpu.backends.cuda_backend import CUDABackend
                    backend = CUDABackend(device_id=gpu.index)
                    if backend.is_available():
                        self._backends["cuda"] = backend
                except ImportError:
                    pass

    def set_compute_mode(self, mode: str) -> None:
        """Change compute mode at runtime."""
        if mode not in VALID_COMPUTE_MODES:
            raise ValueError(f"Invalid compute mode '{mode}'. Use: {VALID_COMPUTE_MODES}")
        if mode in ("gpu", "hybrid") and not self.has_gpu():
            if mode == "gpu":
                raise RuntimeError("No GPU backend available. Use 'cpu' or install GPU dependencies.")
            logger.warning("No GPU available — hybrid mode will use CPU only.")
        self._compute_mode = mode

    def get_backend(self, task: str = "general") -> ComputeBackend:
        """Return appropriate backend for the current mode and task type.

        In hybrid mode: GPU for 'hash'/'regex'/'encode', CPU for 'io'/'general'.
        """
        if self._compute_mode == "cpu":
            return self._cpu_backend
        if self._compute_mode == "gpu":
            return self._best_gpu() or self._cpu_backend
        # hybrid
        if task in ("hash", "regex", "encode", "matmul"):
            return self._best_gpu() or self._cpu_backend
        return self._cpu_backend

    def _best_gpu(self) -> Optional[ComputeBackend]:
        """Return the best available GPU backend."""
        for name in ("cuda", "rocm", "oneapi", "metal", "opencl"):
            if name in self._backends:
                return self._backends[name]
        return None

    def has_gpu(self) -> bool:
        """Check if any GPU backend is loaded."""
        return any(k != "cpu" for k in self._backends)

    @property
    def compute_mode(self) -> str:
        return self._compute_mode

    @property
    def available_backends(self) -> List[str]:
        return list(self._backends.keys())

    def show_hardware(self) -> List[str]:
        """Return summary lines for display."""
        if not self._profile:
            self.initialize()
        lines = self._discovery.summary_lines()
        lines.append(f"Compute mode: {self._compute_mode}")
        lines.append(f"Backends: {', '.join(self.available_backends)}")
        return lines
