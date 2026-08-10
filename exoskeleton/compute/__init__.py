"""Algorithmic No-GPU Intelligence Stack.

Replaces brute-force matrix multiplication with algorithmic intelligence:

- SLIDEEngine: Hash-table sparse updates replacing CUDA backprop
- LiteParseEngine: Heuristic structural projection replacing token-by-token parsing
- SwiftShaderInterface: SIMD vectorized rendering replacing hardware rasterization
"""

from exoskeleton.compute.algorithmic import (
    SLIDEEngine,
    LiteParseEngine,
    SwiftShaderInterface,
)

__all__ = [
    "SLIDEEngine",
    "LiteParseEngine",
    "SwiftShaderInterface",
]
