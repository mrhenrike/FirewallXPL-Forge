"""GPU detection and honest performance expectations for FirewallXPL workflows.

Author: André Henrique (@mrhenrike) | União Geek — https://github.com/Uniao-Geek
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


def _nvidia_smi_query() -> Optional[str]:
    """Return first line of ``nvidia-smi`` query or None if unavailable."""
    binary = shutil.which("nvidia-smi")
    if not binary:
        return None
    try:
        out = subprocess.run(
            [binary, "-L"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if out.returncode != 0 or not (out.stdout or "").strip():
            return None
        return (out.stdout or "").strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError) as exc:
        logger.debug("nvidia-smi failed: %s", exc)
        return None


def torch_cuda_available() -> bool:
    """Return True if PyTorch reports a CUDA device."""
    try:
        import torch  # type: ignore

        return bool(torch.cuda.is_available())
    except ImportError:
        return False


def gpu_capability_summary() -> Tuple[bool, bool, List[str]]:
    """Summarize GPU-related capabilities for user messaging.

    Returns:
        Tuple of (nvidia_driver_visible, torch_cuda, advisory_lines).
    """
    lines: List[str] = []
    smi_line = _nvidia_smi_query()
    nvidia_ok = smi_line is not None
    if nvidia_ok:
        lines.append("Driver/GPU (nvidia-smi): {}".format(smi_line))
    else:
        lines.append("nvidia-smi: não encontrado ou sem GPU NVIDIA visível neste host.")

    cuda_torch = torch_cuda_available()
    if cuda_torch:
        lines.append("PyTorch: CUDA disponível (útil sobretudo para inferência/batch numérico, não para I/O HTTP).")
    else:
        lines.append(
            "PyTorch+CUDA: não disponível. O *advisor* usa vetores minúsculos; ganho com GPU é marginal. "
            "Para quebra de hash em massa (WPA/PMKID, etc.), use hashcat com `-d` / OpenCL."
        )

    lines.append(
        "Nota: módulos de rede (HTTP/SSH/SNMP, …) são, em geral, limitados por latência e não por FLOPS; "
        "GPU não acelera *requests* como acelera cargas criptográficas massivas."
    )
    return nvidia_ok, cuda_torch, lines
