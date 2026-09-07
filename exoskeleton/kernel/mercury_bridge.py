"""Mercury2ArrowBridge — dLLM block revisions streamed into Arrow memory.

Mercury 2 is a diffusion LLM (dLLM): instead of predicting tokens
sequentially, it operates like *an editor revising a full draft in
parallel*. Inside the Exoskeleton it performs non-blocking stream
filtering, structural JSON transformation, tool-call routing, and
real-time buffer updates at 1,000+ tokens/sec.

This bridge streams each parallel block revision into Arrow columnar
memory **as it arrives** — compaction overlaps ingestion instead of
following it. ``compact()`` resolves each block to its latest revision
and produces the clean-context table that ``InstantInjectionKernel.inject()``
publishes into the ava007 read slot.

Non-blocking by construction: revisions land in a deque buffer; the
standard processing clock never waits on the bridge.
"""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict, Optional

import pyarrow as pa


@dataclass(frozen=True)
class BlockRevision:
    """One Mercury 2 parallel draft revision for a block."""

    block_id: int
    revision: int
    text: str
    role: str = "draft"          # draft | tool_call | system
    ts_ns: int = 0


SCHEMA = pa.schema(
    [
        ("block_id", pa.int64()),
        ("revision", pa.int64()),
        ("text", pa.string()),
        ("role", pa.string()),
        ("ts_ns", pa.int64()),
    ]
)


class Mercury2ArrowBridge:
    """Stream Mercury 2 dLLM block output directly into Arrow segments."""

    def __init__(self, max_buffer: int = 100_000):
        self._buffer: Deque[BlockRevision] = deque(maxlen=max_buffer)
        self._ingested = 0
        self._t0 = time.perf_counter()

    # ------------------------------------------------------------------
    def ingest_block(self, block: Dict[str, Any]) -> int:
        """One dLLM revision → buffer. Non-blocking, O(1) append.

        Accepts a dict shaped like ``{"block_id", "revision", "text",
        "role"}`` — the native Mercury 2 block-output shape — and queues
        it for columnar compaction. Returns the buffer depth.
        """
        rev = BlockRevision(
            block_id=int(block["block_id"]),
            revision=int(block.get("revision", 0)),
            text=str(block.get("text", "")),
            role=str(block.get("role", "draft")),
            ts_ns=time.perf_counter_ns(),
        )
        self._buffer.append(rev)
        self._ingested += 1
        return len(self._buffer)

    def compact(self, drop_intermediate: bool = True) -> pa.Table:
        """Resolve the buffer into a clean-context Arrow table.

        Each block collapses to its LATEST revision (the diffusion editor's
        final draft for that block), ordered by block ID — the stable
        reading order ava007 consumes. Intermediate revisions are dropped
        from the compacted view; the buffer itself is drained.
        """
        latest: Dict[int, BlockRevision] = {}
        for rev in self._buffer:
            if rev.block_id not in latest or rev.revision >= latest[rev.block_id].revision:
                latest[rev.block_id] = rev
        ordered = [latest[k] for k in sorted(latest)]
        table = pa.table(
            {
                "block_id": pa.array([r.block_id for r in ordered], pa.int64()),
                "revision": pa.array([r.revision for r in ordered], pa.int64()),
                "text": pa.array([r.text for r in ordered], pa.string()),
                "role": pa.array([r.role for r in ordered], pa.string()),
                "ts_ns": pa.array([r.ts_ns for r in ordered], pa.int64()),
            },
            schema=SCHEMA,
        )
        if drop_intermediate:
            self._buffer.clear()
        return table

    # ------------------------------------------------------------------
    def stats(self) -> Dict[str, Any]:
        elapsed = time.perf_counter() - self._t0
        return {
            "ingested_revisions": self._ingested,
            "buffer_depth": len(self._buffer),
            "elapsed_s": round(elapsed, 3),
            "blocks_per_s": round(self._ingested / elapsed, 1) if elapsed else 0.0,
        }

    def reset(self) -> None:
        self._buffer.clear()
        self._ingested = 0
        self._t0 = time.perf_counter()
