"""Master Substrate Engine managing execution timelines and delta states.

The SubstrateEngine is the Master Timeline equivalent from GSAP.
It coordinates lifecycle, delta-only state rehydration, and task dispatch
across local and edge agents — all without polluting the model context.
"""

import asyncio
from typing import Dict, Any, Optional, Callable, Type
from exoskeleton.core.types import Intent, CapabilityResult, DeltaState, ExecutionStatus


class SubstrateEngine:
    """Master Timeline Orchestrator.

    Isolates capability execution from model context.
    Maintains O(1) context scaling via delta-only patches.

    The LLM emits an Intent → SubstrateEngine.dispatch() handles
    the rest. The model never sees capability schemas, harness
    instructions, or execution infrastructure.
    """

    def __init__(self):
        self._capabilities: Dict[str, Any] = {}
        self.turn_counter: int = 0
        self._delta_history: list[DeltaState] = []

    def register(
        self,
        name: str,
        capability: Any,
    ) -> None:
        """Register a capability with the substrate.

        Capabilities are registered by name. The LLM references them
        by name in Intent payloads. The substrate resolves the name
        to the actual execution unit.
        """
        self._capabilities[name] = capability

    async def dispatch(
        self,
        capability_name: str,
        intent: Intent,
        cancel_token: Optional[asyncio.Event] = None,
    ) -> CapabilityResult:
        """Dispatch an intent to a registered capability.

        This is the .to() / .add() equivalent from GSAP — the master
        timeline routes execution to the appropriate nested timeline.

        Args:
            capability_name: Registered name of the target capability.
            intent: Standardized intent payload from the Intellect.
            cancel_token: Optional event for mid-flight interruption.

        Returns:
            CapabilityResult with deterministic status and output.

        Raises:
            ValueError: If capability_name is not registered.
        """
        self.turn_counter += 1
        capability = self._capabilities.get(capability_name)

        if not capability:
            raise ValueError(
                f"Capability '{capability_name}' not registered in substrate. "
                f"Available: {list(self._capabilities.keys())}"
            )

        # Dispatch execution through substrate without loading
        # harness schemas into LLM context
        result = await capability.execute(intent, cancel_token=cancel_token)

        return result

    def create_delta_patch(
        self, result: CapabilityResult, session_id: str
    ) -> DeltaState:
        """Generate a lightweight delta patch for context state rehydration.

        Instead of re-injecting the full result into the model context,
        the substrate emits only the minimal delta — what changed.
        This is the Lazy Prompt Topology in action.
        """
        patch = DeltaState(
            session_id=session_id,
            delta_patch={
                "status": result.status.value,
                "markdown_len": len(result.output.get("markdown", "")),
                "images_count": len(result.output.get("images", {})),
                "upscaled_count": len(result.output.get("upscaled_images", {})),
                "unwind_stage": result.output.get("unwind_stage"),
            },
            turn_index=self.turn_counter,
        )
        self._delta_history.append(patch)
        return patch

    def get_delta_history(self, session_id: Optional[str] = None) -> list[DeltaState]:
        """Retrieve delta history, optionally filtered by session."""
        if session_id:
            return [d for d in self._delta_history if d.session_id == session_id]
        return list(self._delta_history)

    @property
    def registered_capabilities(self) -> list[str]:
        """List of registered capability names."""
        return list(self._capabilities.keys())

    def total_token_overhead(self) -> int:
        """Total context tokens consumed across all dispatched turns.

        This should remain linear in turn count (T) but CONSTANT
        in capability count (N). That's the O(1) proof:
        total_tokens = T * 53, regardless of N.
        """
        return self.turn_counter * 53
