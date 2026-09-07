"""instant() — High-Density Zero-Duration Operations.

The kernel translation of ``gsap.set()``: forces target state updates in
exactly zero seconds with zero frame delay. Instead of incrementally
computing a delta layer (schedule -> queue -> write), the
InstantInjectionKernel dumps target states natively into memory registers
simultaneously — a global, absolute hardware state-clapper.

Two operations:

* ``set(shards, state)``    — vectorized simultaneous write across virtual
  shards, out-of-band with the standard processing clock. Bumps the global
  clap ID.
* ``inject(slot, table)``   — atomic pointer swap into a consumer read slot
  (e.g. the ava007 context slot). O(1): the reference is replaced under a
  single lock; the consumer never observes a partially-built state.

This module is substrate runtime: it never interprets or persists
cognitive state. Slots carry opaque payloads.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Sequence

import numpy as np


@dataclass(frozen=True)
class InstantReceipt:
    """Proof-of-clap returned by every zero-duration operation.

    ``frame_delay_ms`` is 0.0 by construction — a ``set()``/``inject()``
    completes within the calling frame — and is *also* measured so the
    claim stays honest under benchmarking.
    """

    operation: str            # "set" | "inject"
    clap_id: int              # global monotonically increasing beat
    targets: int              # shards written or slot swapped
    frame_delay_ms: float     # 0.0 by construction
    wall_us: float            # measured wall-clock microseconds (honesty)
    payload_bytes: int = 0


@dataclass
class ReadSlot:
    """A clap-verified consumer slot (e.g. ``ava007.context``).

    Holds an opaque payload reference plus the clap ID at which it was
    swapped in. Reads are lock-guarded only for the pointer fetch; the
    payload itself is immutable once published.
    """

    name: str
    _payload: Any = None
    _clap_id: int = -1
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def read(self) -> Any:
        with self._lock:
            return self._payload

    def swap(self, payload: Any, clap_id: int) -> None:
        """Atomic pointer swap — the O(1) state override."""
        with self._lock:
            self._payload = payload
            self._clap_id = clap_id

    @property
    def clap_id(self) -> int:
        with self._lock:
            return self._clap_id

    @property
    def is_live(self) -> bool:
        return self.read() is not None


class InstantInjectionKernel:
    """Global atomic state-clapper across virtual shards and read slots.

    The Exoskeleton uses this for instant intelligence injection: when a
    newly prepared context state (compacted stream, hot-swapped adapter)
    is ready, it enters service via ``inject()`` — the consumer's context
    shifts without dropping frames, thread locks, or array re-indexing.
    """

    def __init__(self, slot_count: int = 512, state_dim: int = 0):
        self._clap_counter = 0
        self._lock = threading.Lock()
        # Shard register file: fixed-shape row-major registers for O(1) writes.
        self._register_shape = (slot_count, state_dim if state_dim > 0 else 1)
        self._registers = np.zeros(self._register_shape, dtype=np.float64)
        self._register_live = np.zeros(slot_count, dtype=bool)
        self._slots: Dict[str, ReadSlot] = {}
        self._last_receipt: InstantReceipt | None = None
        self.history: List[InstantReceipt] = []

    # ------------------------------------------------------------------
    # gsap.set() equivalent
    # ------------------------------------------------------------------
    def set(self, shards: Iterable[int], state: Any) -> InstantReceipt:
        """Immediate, atomic state override across target shard registers.

        All targets are written *simultaneously* via one vectorized
        assignment — no per-shard loop, no delta layer, no scheduling.
        """
        t0 = time.perf_counter_ns()
        idx = np.fromiter(shards, dtype=np.int64)
        payload = np.asarray(state, dtype=np.float64)
        if payload.ndim == 1:
            payload = np.broadcast_to(payload, (idx.size, payload.shape[0]))
        with self._lock:
            self._registers[idx] = payload
            self._register_live[idx] = True
            self._clap_counter += 1
            clap = self._clap_counter
        wall_us = (time.perf_counter_ns() - t0) / 1_000.0
        receipt = InstantReceipt(
            operation="set",
            clap_id=clap,
            targets=int(idx.size),
            frame_delay_ms=0.0,
            wall_us=round(wall_us, 3),
            payload_bytes=int(payload.nbytes),
        )
        self._last_receipt = receipt
        self.history.append(receipt)
        return receipt

    def reset_shards(self, shards: Sequence[int]) -> InstantReceipt:
        """Ultra-fast reset switch — zero registers out-of-band."""
        return self.set(shards, np.zeros(self._register_shape[1]))

    # ------------------------------------------------------------------
    # Atomic pointer swap into consumer read slots
    # ------------------------------------------------------------------
    def slot(self, name: str) -> ReadSlot:
        with self._lock:
            if name not in self._slots:
                self._slots[name] = ReadSlot(name=name)
            return self._slots[name]

    def inject(self, slot: str | ReadSlot, table: Any) -> InstantReceipt:
        """Atomic pointer swap: publish a prepared state into a read slot.

        The consumer (ava007) reads pre-compacted, fully-resolved state —
        never a partially-updated one. The swap is O(1) in payload size:
        a reference replacement, not a copy.
        """
        t0 = time.perf_counter_ns()
        target = slot if isinstance(slot, ReadSlot) else self.slot(slot)
        with self._lock:
            self._clap_counter += 1
            clap = self._clap_counter
        target.swap(table, clap)
        wall_us = (time.perf_counter_ns() - t0) / 1_000.0
        nbytes = getattr(table, "nbytes", 0)
        receipt = InstantReceipt(
            operation="inject",
            clap_id=clap,
            targets=1,
            frame_delay_ms=0.0,
            wall_us=round(wall_us, 3),
            payload_bytes=int(nbytes) if nbytes else 0,
        )
        self._last_receipt = receipt
        self.history.append(receipt)
        return receipt

    def read(self, slot: str | ReadSlot) -> Any:
        target = slot if isinstance(slot, ReadSlot) else self.slot(slot)
        return target.read()

    # ------------------------------------------------------------------
    @property
    def clap_id(self) -> int:
        return self._clap_counter

    @property
    def last_receipt(self) -> InstantReceipt | None:
        return self._last_receipt

    def stats(self) -> Dict[str, Any]:
        sets = [r for r in self.history if r.operation == "set"]
        injects = [r for r in self.history if r.operation == "inject"]
        return {
            "clap_id": self._clap_counter,
            "registers": int(self._register_shape[0]),
            "live_registers": int(self._register_live.sum()),
            "slots": {name: s.clap_id for name, s in self._slots.items()},
            "set_ops": len(sets),
            "inject_ops": len(injects),
            "max_set_wall_us": max((r.wall_us for r in sets), default=0.0),
            "max_inject_wall_us": max((r.wall_us for r in injects), default=0.0),
            "frame_delay_ms": 0.0,
        }
