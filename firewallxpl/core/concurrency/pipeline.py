"""Async scan pipeline for FirewallXPL-Forge.

Implements a staged pipeline: Discovery -> Fingerprint -> Prioritize -> Check -> Exploit -> Report.
Each stage feeds results to the next without waiting for all to complete.

Author: André Henrique (@mrhenrike) | União Geek
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("firewallxpl.concurrency.pipeline")


class PipelineStage(Enum):
    """Named stages in the scan pipeline."""
    DISCOVERY = "discovery"
    FINGERPRINT = "fingerprint"
    PRIORITIZE = "prioritize"
    CHECK = "check"
    EXPLOIT = "exploit"
    REPORT = "report"


@dataclass
class PipelineItem:
    """Data flowing through the pipeline."""
    target: str
    stage: PipelineStage = PipelineStage.DISCOVERY
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


class ScanPipeline:
    """Async pipeline that processes items through sequential stages.

    Each stage is a callable that receives a PipelineItem and returns
    a modified PipelineItem (or None to drop it).
    """

    def __init__(self) -> None:
        self._stages: Dict[PipelineStage, Callable] = {}
        self._results: List[PipelineItem] = []
        self._buffer_size: int = 100

    def register_stage(
        self, stage: PipelineStage, handler: Callable[..., Any]
    ) -> None:
        """Register a handler for a pipeline stage."""
        self._stages[stage] = handler

    async def process_item(self, item: PipelineItem) -> Optional[PipelineItem]:
        """Process a single item through all registered stages."""
        stage_order = [
            PipelineStage.DISCOVERY,
            PipelineStage.FINGERPRINT,
            PipelineStage.PRIORITIZE,
            PipelineStage.CHECK,
            PipelineStage.EXPLOIT,
            PipelineStage.REPORT,
        ]
        for stage in stage_order:
            if stage not in self._stages:
                continue
            handler = self._stages[stage]
            try:
                item.stage = stage
                if asyncio.iscoroutinefunction(handler):
                    item = await handler(item)
                else:
                    item = handler(item)
                if item is None:
                    return None
            except Exception as exc:
                item.errors.append(f"{stage.value}: {exc}")
                logger.error("Pipeline %s failed for %s: %s", stage.value, item.target, exc)
        return item

    async def run(self, targets: List[str], concurrency: int = 10) -> List[PipelineItem]:
        """Run pipeline for all targets with controlled concurrency."""
        semaphore = asyncio.Semaphore(concurrency)
        results: List[PipelineItem] = []

        async def _process(target: str) -> None:
            async with semaphore:
                item = PipelineItem(target=target)
                result = await self.process_item(item)
                if result:
                    results.append(result)

        tasks = [_process(t) for t in targets]
        await asyncio.gather(*tasks, return_exceptions=True)
        self._results = results
        return results

    def run_sync(self, targets: List[str], concurrency: int = 10) -> List[PipelineItem]:
        """Synchronous wrapper for run()."""
        return asyncio.run(self.run(targets, concurrency))

    @property
    def results(self) -> List[PipelineItem]:
        return list(self._results)
