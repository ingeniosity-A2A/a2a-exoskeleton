"""StaggerKernel — Delays and Sequential Execution (the "Stagger" Ability).

The kernel translation of GSAP's native array staggers and delay logic:
feed the kernel a massive dataset and declare a progressive delay — the
system offsets the calculation window for each index by milliseconds or
cycles **natively at the execution layer**. No manual loop management,
no thread-ID math, no wait states.

Use frames: progressive wave equations, scheduled queue-draining
mechanisms, rolling database updates.

Distribution profiles mirror GSAP's ``stagger``:

* ``each``   — index * i * interval (the classic progressive wave)
* ``center`` — offsets expand outward from the middle of the array
* ``edge``   — offsets expand outward from the first element
* ``random`` — uniform random offsets within the total spread
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List, Optional, Sequence


@dataclass(frozen=True)
class StaggerResult:
    """One item's execution record: its declared offset and measured timing."""

    index: int
    declared_start_ms: float     # offset window declared by the stagger
    measured_start_ms: float     # when execution actually began
    result: Any = None
    error: str | None = None

    @property
    def drift_ms(self) -> float:
        return round(self.measured_start_ms - self.declared_start_ms, 3)


DISTRIBUTIONS = ("each", "center", "edge", "random")


class StaggerKernel:
    """Native per-index offset execution windows over asyncio."""

    def __init__(self, tolerance_ms: float = 5.0):
        self.tolerance_ms = tolerance_ms

    def offsets(
        self,
        count: int,
        interval_ms: float,
        distribution: str = "each",
        rng: Optional[random.Random] = None,
    ) -> List[float]:
        """Declared start offset (ms) for each index — pure scheduling math."""
        if distribution not in DISTRIBUTIONS:
            raise ValueError(f"distribution must be one of {DISTRIBUTIONS}")
        if distribution == "each":
            return [i * interval_ms for i in range(count)]
        if distribution == "center":
            mid = (count - 1) / 2.0
            return [abs(i - mid) * interval_ms for i in range(count)]
        if distribution == "edge":
            return [i * interval_ms for i in range(count)]  # wave from edge 0
        # random
        rng = rng or random.Random()
        spread = count * interval_ms
        return [rng.random() * spread for _ in range(count)]

    async def stagger(
        self,
        items: Sequence[Any],
        fn: Callable[[Any], Any | Awaitable[Any]],
        interval_ms: float = 10.0,
        distribution: str = "each",
        rng: Optional[random.Random] = None,
    ) -> List[StaggerResult]:
        """Execute ``fn(item)`` for every item with a per-index offset window.

        The offsets are a declared property of the wave shape — callers
        never write scheduling loops. Async work is non-blocking: each
        item's window opens at its offset and the tasks overlap naturally.
        """
        starts = self.offsets(len(items), interval_ms, distribution, rng)
        t0 = time.perf_counter()
        results: List[Optional[StaggerResult]] = [None] * len(items)

        async def _run(i: int, item: Any) -> None:
            declared = starts[i]
            delay = declared / 1000.0 - (time.perf_counter() - t0)
            if delay > 0:
                await asyncio.sleep(delay)
            measured = (time.perf_counter() - t0) * 1000.0
            try:
                out = fn(item)
                if asyncio.iscoroutine(out):
                    out = await out
                results[i] = StaggerResult(i, declared, measured, out)
            except Exception as exc:  # partial-success tolerance
                results[i] = StaggerResult(i, declared, measured, error=str(exc))

        await asyncio.gather(*(_run(i, it) for i, it in enumerate(items)))
        return [r for r in results if r is not None]

    def wave(self, count: int, interval_ms: float, distribution: str = "each") -> dict:
        """Wave-equation declaration: the schedule without execution."""
        starts = self.offsets(count, interval_ms, distribution)
        return {
            "count": count,
            "interval_ms": interval_ms,
            "distribution": distribution,
            "total_spread_ms": max(starts) if starts else 0.0,
            "starts_ms": [round(s, 3) for s in starts],
        }
