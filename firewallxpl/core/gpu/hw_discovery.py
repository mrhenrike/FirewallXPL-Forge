"""Automatic hardware discovery — CPU and GPU(s) probe with caching.

Detects CPU model/cores/RAM and all available GPU(s) with driver info,
compute API, and Python backend availability. Caches results for 24h.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import json
import logging
import os
import platform
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger("firewallxpl.gpu.hw_discovery")

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False


@dataclass
class CPUInfo:
    """Detected CPU information."""
    model: str = "Unknown"
    cores_physical: int = 1
    cores_logical: int = 1
    freq_mhz: int = 0
    ram_total_mb: int = 0
    ram_available_mb: int = 0
    arch: str = "unknown"


@dataclass
class GPUInfo:
    """Detected GPU information."""
    index: int = 0
    model: str = "Unknown"
    vendor: str = "unknown"
    vram_mb: int = 0
    driver_version: str = ""
    compute_api: str = ""
    compute_version: str = ""
    python_backend_ok: bool = False
    python_backend_lib: str = ""
    benchmark_ops_s: float = 0.0


@dataclass
class HardwareProfile:
    """Complete hardware profile."""
    cpu: CPUInfo = field(default_factory=CPUInfo)
    gpus: List[GPUInfo] = field(default_factory=list)
    timestamp: float = 0.0


class HardwareDiscovery:
    """Probes system hardware and caches results."""

    DEFAULT_CACHE_TTL_HOURS: int = 24

    def __init__(self, cache_path: Optional[str] = None, cache_ttl_hours: int = 24) -> None:
        self._cache_path: Optional[Path] = Path(cache_path) if cache_path else None
        self._cache_ttl: int = cache_ttl_hours * 3600
        self._profile: Optional[HardwareProfile] = None

    def discover(self, force: bool = False) -> HardwareProfile:
        """Run full hardware discovery or load from cache."""
        if not force and self._profile:
            return self._profile

        if not force and self._cache_path:
            cached = self._load_cache()
            if cached:
                self._profile = cached
                return cached

        profile = HardwareProfile(timestamp=time.time())
        profile.cpu = self._probe_cpu()
        profile.gpus = self._probe_gpus()
        self._profile = profile

        if self._cache_path:
            self._save_cache(profile)

        return profile

    def _probe_cpu(self) -> CPUInfo:
        """Detect CPU information via psutil + platform."""
        info = CPUInfo(arch=platform.machine() or "unknown")

        if _HAS_PSUTIL:
            info.cores_physical = psutil.cpu_count(logical=False) or 1
            info.cores_logical = psutil.cpu_count(logical=True) or 1
            freq = psutil.cpu_freq()
            if freq:
                info.freq_mhz = int(freq.current)
            mem = psutil.virtual_memory()
            info.ram_total_mb = int(mem.total / (1024 * 1024))
            info.ram_available_mb = int(mem.available / (1024 * 1024))

        info.model = platform.processor() or "Unknown"
        return info

    def _probe_gpus(self) -> List[GPUInfo]:
        """Detect all available GPUs via multiple backends."""
        gpus: List[GPUInfo] = []
        gpus.extend(self._probe_nvidia())
        gpus.extend(self._probe_amd())
        gpus.extend(self._probe_intel())
        gpus.extend(self._probe_apple_metal())
        for i, g in enumerate(gpus):
            g.index = i
        return gpus

    def _probe_nvidia(self) -> List[GPUInfo]:
        """Detect NVIDIA GPUs via nvidia-smi + torch.cuda."""
        gpus: List[GPUInfo] = []
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10,
            )
            if out.returncode == 0:
                for line in out.stdout.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 3:
                        gpu = GPUInfo(
                            model=parts[0],
                            vendor="nvidia",
                            vram_mb=int(float(parts[1])),
                            driver_version=parts[2],
                            compute_api="cuda",
                        )
                        gpus.append(gpu)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        try:
            import torch
            if torch.cuda.is_available():
                for i, g in enumerate(gpus):
                    g.python_backend_ok = True
                    g.python_backend_lib = f"torch {torch.__version__}"
                    cap = torch.cuda.get_device_capability(min(i, torch.cuda.device_count() - 1))
                    g.compute_version = f"CUDA {cap[0]}.{cap[1]}"
                if not gpus:
                    for i in range(torch.cuda.device_count()):
                        gpus.append(GPUInfo(
                            model=torch.cuda.get_device_name(i),
                            vendor="nvidia", compute_api="cuda",
                            python_backend_ok=True,
                            python_backend_lib=f"torch {torch.__version__}",
                        ))
        except ImportError:
            pass

        return gpus

    def _probe_amd(self) -> List[GPUInfo]:
        """Detect AMD GPUs via rocm-smi."""
        gpus: List[GPUInfo] = []
        try:
            out = subprocess.run(
                ["rocm-smi", "--showproductname", "--csv"],
                capture_output=True, text=True, timeout=10,
            )
            if out.returncode == 0 and "card" in out.stdout.lower():
                gpus.append(GPUInfo(vendor="amd", compute_api="rocm", model="AMD GPU (ROCm)"))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        try:
            import torch
            if hasattr(torch.version, "hip") and torch.version.hip:
                for g in gpus:
                    g.python_backend_ok = True
                    g.python_backend_lib = f"torch {torch.__version__} (ROCm)"
                    g.compute_version = f"ROCm/HIP {torch.version.hip}"
        except (ImportError, AttributeError):
            pass

        return gpus

    def _probe_intel(self) -> List[GPUInfo]:
        """Detect Intel GPUs via oneAPI/XPU."""
        gpus: List[GPUInfo] = []
        try:
            import torch
            if hasattr(torch, "xpu") and torch.xpu.is_available():
                for i in range(torch.xpu.device_count()):
                    gpus.append(GPUInfo(
                        model=torch.xpu.get_device_name(i),
                        vendor="intel", compute_api="oneapi",
                        python_backend_ok=True,
                        python_backend_lib=f"torch {torch.__version__} (XPU)",
                    ))
        except (ImportError, AttributeError):
            pass
        return gpus

    def _probe_apple_metal(self) -> List[GPUInfo]:
        """Detect Apple Metal (MPS) on macOS."""
        gpus: List[GPUInfo] = []
        if platform.system() != "Darwin":
            return gpus
        try:
            import torch
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                gpus.append(GPUInfo(
                    model=f"Apple {platform.processor()} (Metal)",
                    vendor="apple", compute_api="metal",
                    python_backend_ok=True,
                    python_backend_lib=f"torch {torch.__version__} (MPS)",
                ))
        except (ImportError, AttributeError):
            pass
        return gpus

    def available_backends(self) -> List[str]:
        """Return list of available compute backend names."""
        if not self._profile:
            self.discover()
        backends = ["cpu"]
        for g in self._profile.gpus:
            if g.python_backend_ok and g.compute_api not in backends:
                backends.append(g.compute_api)
        return backends

    def summary_lines(self) -> List[str]:
        """Return human-readable summary lines for banner display."""
        if not self._profile:
            self.discover()
        p = self._profile
        lines = [
            f"CPU: {p.cpu.model} ({p.cpu.cores_physical}c/{p.cpu.cores_logical}t) "
            f"RAM: {p.cpu.ram_total_mb}MB",
        ]
        if p.gpus:
            for g in p.gpus:
                status = "OK" if g.python_backend_ok else "no Python backend"
                lines.append(
                    f"GPU#{g.index}: {g.model} ({g.compute_api}) "
                    f"VRAM: {g.vram_mb}MB [{status}]"
                )
        else:
            lines.append("GPU: none detected (CPU-only mode)")
        return lines

    def _load_cache(self) -> Optional[HardwareProfile]:
        """Load cached profile if not expired."""
        if not self._cache_path or not self._cache_path.exists():
            return None
        try:
            data = json.loads(self._cache_path.read_text(encoding="utf-8"))
            ts = data.get("timestamp", 0)
            if time.time() - ts > self._cache_ttl:
                return None
            cpu = CPUInfo(**data.get("cpu", {}))
            gpus = [GPUInfo(**g) for g in data.get("gpus", [])]
            return HardwareProfile(cpu=cpu, gpus=gpus, timestamp=ts)
        except Exception as exc:
            logger.warning("Cache load failed: %s", exc)
            return None

    def _save_cache(self, profile: HardwareProfile) -> None:
        """Save profile to cache file."""
        if not self._cache_path:
            return
        try:
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "cpu": asdict(profile.cpu),
                "gpus": [asdict(g) for g in profile.gpus],
                "timestamp": profile.timestamp,
            }
            self._cache_path.write_text(
                json.dumps(data, indent=2), encoding="utf-8"
            )
        except Exception as exc:
            logger.warning("Cache save failed: %s", exc)
