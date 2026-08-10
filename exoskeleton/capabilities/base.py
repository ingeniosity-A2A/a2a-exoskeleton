"""Base Capability Contract with Lazy Materialization.

Every capability in the Exoskeleton MUST implement this contract.
The BaseCapability provides the lazy materialization pattern —
model artifacts load only when the capability is invoked,
maintaining zero context footprint at rest.

This is the GSAP onComplete callback equivalent: capabilities
remain completely unmaterialized until explicitly called.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import asyncio

from exoskeleton.core.types import CapabilityResult, ExecutionStatus, Intent


class BaseCapability(ABC):
    """Abstract base for all Exoskeleton capabilities.

    Capabilities are the Nested Timeline equivalent from GSAP.
    Each encapsulates one or more sub-tools into a single,
    O(1) addressable unit that the model interacts with
    via a single Intent.
    """

    def __init__(self):
        self._materialized: bool = False

    @abstractmethod
    def _ensure_loaded(self) -> None:
        """Load model artifacts and heavy resources.

        Called lazily on first invocation. Subclasses MUST
        implement this to perform expensive initialization
        (model loading, GPU allocation, etc.) only once.
        """
        ...

    @property
    def is_materialized(self) -> bool:
        """Whether the capability has loaded its heavy resources."""
        return self._materialized

    @abstractmethod
    async def execute(
        self,
        intent: Intent,
        cancel_token: Optional[asyncio.Event] = None,
    ) -> CapabilityResult:
        """Execute the capability against an intent.

        Args:
            intent: Standardized payload from the Intellect.
            cancel_token: Optional event for mid-flight interruption.

        Returns:
            Deterministic CapabilityResult with status and output.
        """
        ...

    @abstractmethod
    async def reverse_unwind(
        self, partial_state: Dict[str, Any], stage: str
    ) -> CapabilityResult:
        """GSAP easeReverse: Asymmetrical fast-exit teardown.

        When an intent is interrupted or cancelled mid-execution,
        this method sheds heavy resources instantly while
        salvaging lightweight partial results.

        The reverse curve is ALWAYS asymmetric — it never mirrors
        the forward workload. Heavy GPU/model passes are dropped;
        lightweight text deltas are preserved.

        Args:
            partial_state: Any partial results from forward execution.
            stage: Which execution phase the interruption occurred at.

        Returns:
            INTERRUPTED_SALVAGED result with preserved lightweight data.
        """
        ...

    def _mark_materialized(self) -> None:
        """Mark this capability as having loaded its resources."""
        self._materialized = True

    async def _offload_to_executor(self, fn, *args) -> Any:
        """Run a synchronous function off the main async event loop.

        This prevents CPU/GPU-heavy operations from blocking
        the substrate's non-blocking orchestration loop.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, fn, *args)
