"""Substrate-owned Interaction Quantum.

Transport, lineage, temporal and execution state only. Cognitive state belongs
to Cybernetic-Ava007 and crosses this boundary through A2A references.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import hashlib
import json


@dataclass(frozen=True)
class QuantumLineage:
    quantum_id: str
    source_did: str
    parent_quanta: tuple[str, ...] = ()

    @property
    def signature(self) -> str:
        body = {"quantum_id": self.quantum_id, "source_did": self.source_did,
                "parent_quanta": sorted(self.parent_quanta)}
        return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class QuantumExecution:
    capability: Optional[str] = None
    status: str = "pending"
    result_ref: Optional[str] = None
    artifact_ref: Optional[str] = None


@dataclass
class InteractionQuantum:
    """Atomic substrate event; cognition is deliberately excluded."""
    timestamp: str
    source_did: str
    payload: dict[str, Any] = field(default_factory=dict)
    parent_quanta: list[str] = field(default_factory=list)
    execution: Optional[QuantumExecution] = None
    quantum_id: str = ""
    version: str = "3.0"
    temporal_tween: Optional[dict[str, Any]] = None

    def compute_hash(self) -> str:
        body = {"timestamp": self.timestamp, "source_did": self.source_did,
                "payload": self.payload, "parent_quanta": sorted(self.parent_quanta),
                "execution": self.execution.__dict__ if self.execution else None,
                "temporal_tween": self.temporal_tween, "version": self.version}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def seal(self) -> "InteractionQuantum":
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        self.quantum_id = self.compute_hash()
        return self

    @property
    def lineage(self) -> QuantumLineage:
        return QuantumLineage(self.quantum_id, self.source_did, tuple(self.parent_quanta))

    @property
    def lineage_signature(self) -> str:
        return self.lineage.signature

    def to_dict(self) -> dict[str, Any]:
        data = {"quantum_id": self.quantum_id, "timestamp": self.timestamp,
                "source_did": self.source_did, "parent_quanta": self.parent_quanta,
                "payload": self.payload,
                "execution": self.execution.__dict__ if self.execution else None,
                "version": self.version}
        if self.temporal_tween is not None:
            data["temporal_tween"] = self.temporal_tween
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InteractionQuantum":
        execution = data.get("execution")
        tween = data.get("temporal_tween")
        if tween is None:
            tween = data.get("payload", {}).get("temporal_tween")
        return cls(
            timestamp=data.get("timestamp", ""),
            source_did=data.get("source_did", ""),
            payload=data.get("payload", {}),
            parent_quanta=list(data.get("parent_quanta", [])),
            execution=QuantumExecution(**{k: v for k, v in execution.items()
                                          if k in QuantumExecution.__dataclass_fields__}) if execution else None,
            quantum_id=data.get("quantum_id", ""),
            version=data.get("version", "3.0"),
            temporal_tween=tween,
        )

    @classmethod
    def from_jsonl(cls, line: str) -> "InteractionQuantum":
        return cls.from_dict(json.loads(line.strip()))

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=False)
