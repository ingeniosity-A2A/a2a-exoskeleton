"""Composed capabilities and base contracts.

Capabilities are Nested Timelines — they encapsulate multiple
sub-tools into a single O(1) addressable unit.

- base: BaseCapability abstract class with lazy materialization
- visual_doc: ProcessVisualDocumentCapability (Marker + LTX-2.3)
"""

from exoskeleton.capabilities.base import BaseCapability
from exoskeleton.capabilities.visual_doc import (
    ProcessVisualDocumentCapability,
    MarkerExtractionCapability,
    LTXUpscaleCapability,
)

__all__ = [
    "BaseCapability",
    "ProcessVisualDocumentCapability",
    "MarkerExtractionCapability",
    "LTXUpscaleCapability",
]
