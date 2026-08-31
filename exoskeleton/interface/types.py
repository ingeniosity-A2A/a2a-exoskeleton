"""Mirror of Cybernetic-Ava007 exoskeleton-interface (SemVer lockstep)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

INTERFACE_VERSION = "0.1.0"


@dataclass
class IntentMessage:
    interface_version: str
    session_id: str
    intent_id: str
    objective: str
    constraints: dict[str, Any]
    timestamp_ns: int


@dataclass
class ObservationMessage:
    interface_version: str
    session_id: str
    intent_id: str
    status: str
    result: dict[str, Any]
    timestamp_ns: int
