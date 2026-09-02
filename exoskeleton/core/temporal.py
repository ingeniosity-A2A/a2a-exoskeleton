"""GSAP-compatible temporal primitives for the Exoskeleton substrate.

GSAP is used here as a temporal execution/reconstruction mechanism. It does
not own cognition, intent classification, model routing, or skill intelligence.
Ava007 may supply an opaque intent/correlation reference through A2A; the
substrate only schedules and reconstructs the supplied temporal state.
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class TweenType(str, Enum):
    LINEAR = "linear"
    EASE = "ease"
    SPRING = "spring"


class Easing(str, Enum):
    LINEAR = "linear"
    EASE_IN = "ease-in"
    EASE_OUT = "ease-out"
    EASE_IN_OUT = "ease-in-out"
    POWER2_IN = "power2.in"
    POWER2_OUT = "power2.out"
    POWER2_INOUT = "power2.inOut"
    ELASTIC = "elastic"
    BOUNCE = "bounce"
    BACK = "back"


def _bounce_out(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    if t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    t -= 2.625 / 2.75
    return 7.5625 * t * t + 0.984375


EASING_FUNCTIONS: dict[str, Callable[[float], float]] = {
    "linear": lambda t: t,
    "ease-in": lambda t: t * t,
    "ease-out": lambda t: t * (2 - t),
    "ease-in-out": lambda t: 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t,
    "power2.in": lambda t: t * t,
    "power2.out": lambda t: t * (2 - t),
    "power2.inOut": lambda t: 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t,
    "elastic": lambda t: 0 if t == 0 else 1 if t == 1 else -(2 ** (10 * (t - 1))) * math.sin((t - 1.1) * 5 * math.pi),
    "bounce": lambda t: 1 - _bounce_out(1 - t),
    "back": lambda t: t * t * (2.70158 * t - 1.70158),
}


@dataclass
class TweenAtom:
    start: float = 0.0
    end: float = 1.0
    duration_ms: int = 100
    easing: str = "linear"
    delay_ms: int = 0

    def interpolate(self, elapsed_ms: float) -> float:
        if elapsed_ms < self.delay_ms:
            return self.start
        if self.duration_ms <= 0:
            return self.end
        t = max(0.0, min(1.0, (elapsed_ms - self.delay_ms) / self.duration_ms))
        eased_t = EASING_FUNCTIONS.get(self.easing, EASING_FUNCTIONS["linear"])(t)
        return self.start + (self.end - self.start) * eased_t

    def to_dict(self) -> dict:
        return {"start": self.start, "end": self.end, "duration_ms": self.duration_ms, "easing": self.easing, "delay_ms": self.delay_ms}

    @classmethod
    def from_dict(cls, data: dict) -> "TweenAtom":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class TweenTimeline:
    atoms: list[TweenAtom] = field(default_factory=list)
    total_duration_ms: int = 0

    def add(self, atom: TweenAtom) -> "TweenTimeline":
        self.atoms.append(atom)
        self.total_duration_ms = max(self.total_duration_ms, atom.delay_ms + atom.duration_ms)
        return self

    def evaluate(self, elapsed_ms: float) -> list[float]:
        return [atom.interpolate(elapsed_ms) for atom in self.atoms]

    def to_dict(self) -> dict:
        return {"atoms": [a.to_dict() for a in self.atoms], "total_duration_ms": self.total_duration_ms}


class TemporalOrchestrator:
    """Reconstruct temporal state from substrate quanta.

    ``correlation_ref`` is intentionally opaque. It may identify an Ava007
    intent without making the substrate responsible for interpreting it.
    """

    def __init__(self):
        self.timelines: dict[str, TweenTimeline] = {}
        self.quanta: list[dict] = []

    def ingest(self, quantum) -> None:
        q = quantum.to_dict() if hasattr(quantum, "to_dict") else quantum
        self.quanta.append(q)
        tween_data = q.get("temporal_tween") or q.get("payload", {}).get("temporal_tween", {})
        if not tween_data:
            return
        correlation_ref = (
            q.get("correlation_ref")
            or q.get("payload", {}).get("correlation_ref")
            or "default"
        )
        atom = TweenAtom(
            start=float(tween_data.get("start", 0.0)),
            end=float(tween_data.get("end", 1.0)),
            duration_ms=int(tween_data.get("duration_ms", 100)),
            easing=tween_data.get("ease_curve", tween_data.get("type", "linear")),
            delay_ms=int(tween_data.get("delay_ms", 0)),
        )
        self.timelines.setdefault(str(correlation_ref), TweenTimeline()).add(atom)

    def reconstruct(self, elapsed_ms: float) -> dict[str, float]:
        return {
            ref: (values[-1] if values else 0.0)
            for ref, timeline in self.timelines.items()
            for values in [timeline.evaluate(elapsed_ms)]
        }
