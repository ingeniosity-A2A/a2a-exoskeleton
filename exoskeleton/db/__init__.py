"""Dual-Tier DuckDB Architecture.

Two-tier embedded-to-remote DuckDB topology for zero-latency
analytical querying and state persistence:

- IntellectDuckClient: Embedded in-memory client at the Intellect layer
- CoreMembraneDuckServer: Persistent analytical server at the Core-Membrane
"""

from exoskeleton.db.duck_intellect import IntellectDuckClient
from exoskeleton.db.duck_membrane import CoreMembraneDuckServer

__all__ = [
    "IntellectDuckClient",
    "CoreMembraneDuckServer",
]
