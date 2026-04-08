"""GPU acceleration and hardware discovery for FirewallXPL-Forge.

Provides automatic hardware detection (CPU + GPU), multi-vendor GPU backend
abstraction (CUDA/ROCm/oneAPI/Metal/OpenCL/CPU), and compute mode management.

Author: André Henrique (@mrhenrike) | União Geek
"""

from firewallxpl.core.gpu.hw_discovery import HardwareDiscovery, CPUInfo, GPUInfo
from firewallxpl.core.gpu.device_manager import GPUDeviceManager

__all__ = ["HardwareDiscovery", "CPUInfo", "GPUInfo", "GPUDeviceManager"]
