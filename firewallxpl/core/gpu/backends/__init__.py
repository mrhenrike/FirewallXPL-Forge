"""GPU compute backends for FirewallXPL-Forge.

Author: André Henrique (@mrhenrike) | União Geek
"""

from firewallxpl.core.gpu.backends.base import ComputeBackend
from firewallxpl.core.gpu.backends.cpu_backend import CPUBackend

__all__ = ["ComputeBackend", "CPUBackend"]
