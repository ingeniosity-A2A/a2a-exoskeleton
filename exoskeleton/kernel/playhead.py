"""MasterPlayhead — Deterministic State Scoring (the Time-Scrubbing Ability).

The kernel translation of GSAP's precision timeline ticker: a strict,
microsecond-accurate linear global duration clock. All mathematical
pathways registered with the playhead are **deterministic functions of
the master playhead position** — so any state, at any literal point in
time, is resolved by *evaluation*, not by replaying from the beginning
and not by pulling bulky stored checkpoints.

``kernel.seek(0.425)`` returns the exact array states, structural morphs,
and point configurations across the entire dataset at 42.5% — instantly.

This is the substrate-side realization of timeline scrubbing: the playhead
*is* the ground truth; the state store stays flat.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class Producer:
    """A deterministic state producer: ``f(position) -> state``.

    ``position`` is normalized playhead progress in [0, 1]. Producers MUST
    be pure — same position, same state — which is what makes seek()
    resolve state without replay and without checkpoints.
    """

    name: str
    fn: Callable[[float], Any]
    weight: float = 1.0


@dataclass
class PlayheadClock:
    """Microsecond-accurate linear global duration clock."""

    duration_s: float = 60.0
    rate: float = 1.0
    _playing: bool = False
    _t0_perf: float = 0.0
    _t0_pos: float = 0.0

    def play(self) -> "PlayheadClock":
        if not self._playing:
            self._t0_perf = time.perf_counter()
            self._playing = True
        return self

    def pause(self) -> "PlayheadClock":
        if self._playing:
            self._t0_pos = self.position()
            self._playing = False
        return self

    def reverse(self) -> "PlayheadClock":
        self.rate = -abs(self.rate)
        if self._playing:
            self._t0_pos = self.position()
            self._t0_perf = time.perf_counter()
        return self

    def position(self) -> float:
        """Absolute playhead position in [0, 1]."""
        if not self._playing:
            return self._t0_pos
        elapsed = (time.perf_counter() - self._t0_perf) * self.rate
        pos = self._t0_pos + elapsed / self.duration_s
        return min(1.0, max(0.0, pos))

    def seek(self, position: float) -> "PlayheadClock":
        pos = min(1.0, max(0.0, position))
        self._t0_pos = pos
        if self._playing:
            self._t0_perf = time.perf_counter()
        return self


class MasterPlayhead:
    """Global deterministic clock with seek()-based state resolution."""

    def __init__(self, duration_s: float = 60.0):
        self.clock = PlayheadClock(duration_s=duration_s)
        self._producers: Dict[str, Producer] = {}
        self.seek_log: List[Dict[str, Any]] = []

    def register(self, name: str, fn: Callable[[float], Any], weight: float = 1.0) -> None:
        """Register a pure state producer ``f(position) -> state``."""
        self._producers[name] = Producer(name=name, fn=fn, weight=weight)

    # ------------------------------------------------------------------
    # State resolution by evaluation — the whole point
    # ------------------------------------------------------------------
    def seek(self, position: float) -> Dict[str, Any]:
        """Resolve the exact global state at ``position`` (progress in [0,1]).

        Evaluates every registered producer at the requested playhead
        position. Nothing is replayed; nothing is read from a checkpoint
        store — the past is *computed*.
        """
        t0 = time.perf_counter_ns()
        pos = min(1.0, max(0.0, float(position)))
        state = {name: p.fn(pos) for name, p in self._producers.items()}
        elapsed_us = (time.perf_counter_ns() - t0) / 1_000.0
        record = {
            "position": pos,
            "producers": len(state),
            "resolve_us": round(elapsed_us, 3),
            "state_hash": self._hash_state(state),
        }
        self.seek_log.append(record)
        self.clock.seek(pos)
        return {"position": pos, "state": state, "meta": record}

    def resolve_time(self, seconds: float) -> Dict[str, Any]:
        """Seek by absolute time instead of normalized progress."""
        return self.seek(seconds / self.clock.duration_s)

    @staticmethod
    def _hash_state(state: Dict[str, Any]) -> str:
        h = hashlib.sha256()
        for key in sorted(state):
            h.update(key.encode())
            h.update(repr(state[key]).encode())
        return h.hexdigest()[:16]

    # ------------------------------------------------------------------
    def play(self) -> "MasterPlayhead":
        self.clock.play()
        return self

    def pause(self) -> "MasterPlayhead":
        self.clock.pause()
        return self

    def reverse(self) -> "MasterPlayhead":
        self.clock.reverse()
        return self

    @property
    def position(self) -> float:
        return self.clock.position()

    def stats(self) -> Dict[str, Any]:
        return {
            "producers": list(self._producers),
            "duration_s": self.clock.duration_s,
            "rate": self.clock.rate,
            "position": self.position,
            "seeks": len(self.seek_log),
        }
