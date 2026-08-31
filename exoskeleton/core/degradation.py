"""DegradationPolicy — thermal / memory / NPU fallback (honest, no magic)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Tier(str, Enum):
    FULL = "full"
    REDUCED = "reduced"
    MINIMAL = "minimal"
    SAFE = "safe"


_RANK = {Tier.FULL: 0, Tier.REDUCED: 1, Tier.MINIMAL: 2, Tier.SAFE: 3}


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
    mem_safe_mb: float = 128.0

    def evaluate(self, sample: ResourceSample) -> Tier:
        tier = Tier.FULL

        if sample.thermal_c is not None:
            if sample.thermal_c >= self.thermal_minimal_c:
                tier = Tier.MINIMAL
            elif sample.thermal_c >= self.thermal_reduced_c:
                tier = Tier.REDUCED

        if sample.mem_available_mb is not None:
            if sample.mem_available_mb <= self.mem_safe_mb:
                return Tier.SAFE
            if sample.mem_available_mb <= self.mem_minimal_mb:
                if _RANK[tier] < _RANK[Tier.MINIMAL]:
                    tier = Tier.MINIMAL
            elif sample.mem_available_mb <= self.mem_reduced_mb:
                if _RANK[tier] < _RANK[Tier.REDUCED]:
                    tier = Tier.REDUCED

        if not sample.npu_ok and tier == Tier.FULL:
            tier = Tier.REDUCED

        return tier
