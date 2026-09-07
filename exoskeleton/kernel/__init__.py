"""GSAP-Inspired Functional Kernel — non-graphical compute primitives.

The kernel translation of GSAP 3 engine mechanics into substrate compute
(see wiki/architecture/instant-injection-fluid-learning.md):

* ``instant.py``        — gsap.set()  → atomic zero-duration state override
* ``morph.py``          — MorphSVG     → structural point interpolation
* ``stagger.py``        — array stagger→ native offset execution windows
* ``playhead.py``       — timeline.seek→ deterministic state scoring
* ``ingestion.py``      — Sovereign Ingestion Engine (Arrow zero-copy)
* ``mercury_bridge.py`` — Mercury 2 dLLM stream → Arrow compaction

Substrate runtime only: no module here interprets or persists cognitive
state (see ARCHITECTURE-BOUNDARY.md).
"""

from exoskeleton.kernel.instant import (
    InstantInjectionKernel,
    InstantReceipt,
    ReadSlot,
)
from exoskeleton.kernel.morph import MorphKernel, MorphPlan
from exoskeleton.kernel.stagger import StaggerKernel, StaggerResult
from exoskeleton.kernel.playhead import MasterPlayhead, PlayheadClock, Producer
from exoskeleton.kernel.ingestion import SovereignIngestionEngine, IngestReport
from exoskeleton.kernel.mercury_bridge import (
    Mercury2ArrowBridge,
    BlockRevision,
    SCHEMA as MERCURY_BLOCK_SCHEMA,
)

__all__ = [
    "InstantInjectionKernel",
    "InstantReceipt",
    "ReadSlot",
    "MorphKernel",
    "MorphPlan",
    "StaggerKernel",
    "StaggerResult",
    "MasterPlayhead",
    "PlayheadClock",
    "Producer",
    "SovereignIngestionEngine",
    "IngestReport",
    "Mercury2ArrowBridge",
    "BlockRevision",
    "MERCURY_BLOCK_SCHEMA",
]
