"""A2A boundary references for the Exoskeleton substrate.

These contracts carry execution identity across the Intellect/substrate
boundary without carrying model reasoning or chain-of-thought. Skill identity
is referenced, not interpreted, by the substrate.
"""

from dataclasses import dataclass, field
from typing import Any


INTERFACE_VERSION = "0.2.0"


@dataclass(frozen=True)
class IntentRef:
    """Opaque reference to an Ava007-issued intent."""

    interface_version: str
    session_id: str
    intent_id: str
    capability: str
    skill_id: str = ""
    skill_version: str = ""
    source_did: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ObservationRef:
    """Normalized execution observation returned toward the Intellect."""

    interface_version: str
    session_id: str
    intent_id: str
    capability: str
    status: str
    result_ref: str = ""
    artifact_ref: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def sanitize_a2a_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Remove cognitive traces before substrate transport.

    This is a defensive boundary: legacy callers may still provide a
    cognitive_state object, but the Exoskeleton must never persist or forward
    it. An existing explicit correlation_ref/intent_id is retained.
    """
    blocked = {"cognitive_state", "reasoning", "chain_of_thought", "cot", "alternatives"}
    return {key: value for key, value in payload.items() if key not in blocked}
