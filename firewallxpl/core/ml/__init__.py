"""Optional attack advisor (lightweight ML/heuristics + GPU hints).

Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""

from firewallxpl.core.ml.advisor import AttackAdvisor, AdvisorContext
from firewallxpl.core.ml.gpu import gpu_capability_summary

__all__ = (
    "AttackAdvisor",
    "AdvisorContext",
    "gpu_capability_summary",
)
