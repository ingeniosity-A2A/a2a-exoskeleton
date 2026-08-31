"""DegradationPolicy — thermal / memory / NPU fallback (honest, no magic)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Tier(str, Enum):
    FULL = "full"
    REDUCED = "reduced"
    MINIMAL = "minimal"
    SAFE = "safe"


@dataclass
class ResourceSample:
    thermal_c: float | None = None
    mem_available_mb: float | None = None
    npu_ok: bool = True


@dataclass
class DegradationPolicy:
    thermal_reduced_c: float = 42.0
    thermal_minimal_c: float = 48.0
    mem_reduced_mb: float = 512.0
    mem_minimal_mb: float = 256.0

    def evaluate(self, sample: ResourceSample) -> Tier:
        tier = Tier.FULL
        if sample.thermal_c is not None:
            if sample.thermal_c >= self.thermal_minimal_c:
                tier = Tier.MINIMAL
            elif sample.thermal_c >= self.thermal_reduced_c:
                tier = Tier.REDUCED
        if sample.mem_available_mb is not None:
            if sample.mem_available_mb <= self.mem_minimal_mb:
                tier = max(tier, Tier.MINIMAL, key=lambda t: list(Tier).index(t) if False else _rank(t))
                # explicit:
                if sample.mem_available_mb <= self.mem_minimal_mb:
                    tier = Tier.MINIMAL if _rank(Tier) < _rank(Tier.MINIMAL) else tier
                    tier = Tier.MINIMAL
                elif sample.mem_available_mb <= self.mem_reduced_mb and _rank(tier) < _rank(Tier.REDUCED):
                    tier = Tier.REDUCED
        if not sample.npu_ok and tier == Tier.FULL:
            tier = Tier.REDUCED
        if tier == Tier.MINIMAL and (sample.mem_available_mb or 999) < 128:
            return Tier.SAFE
        return tier


def _rank(t: Tier) -> int:
    return {Tier.FULL: 0, Tier.REDUCED: 1, Tier.MINIMAL: 2, Tier.SAFE: 3}[t]
