"""A2A Exoskeleton Substrate.

O(1) context orchestration layer that isolates capability execution
from the model context. The LLM functions purely as an intent engine;
the substrate handles execution, parallel branching, and lazy materialization.
"""

__version__ = "1.0.0"
