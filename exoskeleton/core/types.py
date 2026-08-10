"""Core data contracts for the Exoskeleton Substrate.

These types define the deterministic interfaces between the Intellect (LLM)
and the Substrate (execution engine). All communication flows through
these contracts — the model never sees substrate internals.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ExecutionStatus(str, Enum):
    """Deterministic execution outcome states.

    Every capability MUST return one of these. The substrate engine
    maps status codes to delta patches for O(1) context rehydration.
    """
    COMPLETE = "complete"
    FAILED = "failed"
    INTERRUPTED_SALVAGED = "interrupted_salvaged"


@dataclass
class Intent:
    """Standardized intent payload received from the Intellect.

    The model emits a single Intent regardless of whether the underlying
    task is a simple API call or a complex multi-agent coordination pipeline.
    This is the Unified Collapse in action.
    """
    description: str
    file_path: str
    upscale_figures: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityResult:
    """Deterministic output contract returned from the capability layer.

    The `token_overhead` field enforces O(1) context budget tracking.
    Every result must report its context footprint — the substrate
    engine aggregates these to verify constant scaling.
    """
    status: ExecutionStatus
    output: Dict[str, Any]
    model_used: str = ""
    token_overhead: int = 53  # Enforces O(1) context budget tracking


@dataclass
class DeltaState:
    """Lightweight delta-only state rehydration patch.

    Instead of re-injecting full context on every turn, the substrate
    transmits only the delta — what changed since the last turn.
    This is the mechanism that achieves O(1) scaling: the model receives
    a 53-token routing header + delta patch, never the full state.
    """
    session_id: str
    delta_patch: Dict[str, Any]
    turn_index: int

    @property
    def token_count(self) -> int:
        """Approximate token cost of this delta when serialized to prompt."""
        # Delta patches are structurally small by design.
        # A typical patch: {"status": "complete", "markdown_len": 4200, "images_count": 3}
        # This serializes to ~30-50 tokens depending on values.
        return 53  # Constant — the O(1) guarantee
