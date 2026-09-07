"""MorphKernel — Vector Point Interpolation (the "Morph" Ability).

The kernel translation of MorphSVG point interpolation: data matrices,
numerical arrays, and multi-dimensional tensors are treated exactly like
SVG path nodes. When Matrix A has 500 data points and Matrix B has 1,200,
the kernel does **not** throw a dimensional error — it resolves the
mismatch on the fly via normalized-index point matching:

1. Both structures are normalized onto a shared parametrization
   (unit arc-length position ``s`` in [0, 1]).
2. Each target point's position is matched to the interpolated source
   position at the same ``s`` (pseudo-point insertion / downsampling).
3. Coordinates are eased from source to target with a GSAP easing curve,
   preserving structural continuity across the whole morph.

Use frames: topological data analysis, morphing neural-network weights
during fine-tuning, fluid dynamics simulation state blending.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


# ----------------------------------------------------------------------
# GSAP easing family (subset — shared with the substrate TweenAtom curve set)
# ----------------------------------------------------------------------
def _ease(t: float, name: str) -> float:
    t = min(1.0, max(0.0, t))
    if name == "linear":
        return t
    if name == "power1.in":
        return t * t
    if name == "power2.in":
        return t * t * t
    if name == "power1.out":
        return t * (2 - t)
    if name == "power2.out":
        return 1 - (1 - t) ** 3
    if name in ("power1.inOut", "power2.inOut"):
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
    if name == "sine.inOut":
        return 0.5 - 0.5 * np.cos(np.pi * t)
    raise ValueError(f"Unknown easing '{name}'")


@dataclass(frozen=True)
class MorphPlan:
    """Declared pad/squeeze resolution between two structure shapes."""

    source_points: int
    target_points: int
    source_dim: int
    target_dim: int
    mode: str                 # "identity" | "upsample" | "downsample"
    dim_mode: str             # "identity" | "pad" | "truncate"
    pseudo_points: int        # inserted to satisfy target cardinality
    dropped_points: int       # merged away when downsampling

    @property
    def resolved(self) -> bool:
        return True  # a morph plan ALWAYS resolves — that is the contract


class MorphKernel:
    """Structural morph between mismatched structures with eased continuity."""

    def plan(self, source_shape: Tuple[int, ...], target_shape: Tuple[int, ...]) -> MorphPlan:
        """Declare how a mismatch will be resolved — without erroring."""
        sn, sd = int(source_shape[0]), int(source_shape[1]) if len(source_shape) > 1 else 1
        tn, td = int(target_shape[0]), int(target_shape[1]) if len(target_shape) > 1 else 1
        if sn == tn:
            mode = "identity"
        elif sn < tn:
            mode = "upsample"
        else:
            mode = "downsample"
        if sd == td:
            dim_mode = "identity"
        elif sd < td:
            dim_mode = "pad"
        else:
            dim_mode = "truncate"
        return MorphPlan(
            source_points=sn,
            target_points=tn,
            source_dim=sd,
            target_dim=td,
            mode=mode,
            dim_mode=dim_mode,
            pseudo_points=max(0, tn - sn),
            dropped_points=max(0, sn - tn),
        )

    def morph(
        self,
        source: np.ndarray,
        target: np.ndarray,
        progress: float,
        easing: str = "power1.inOut",
    ) -> np.ndarray:
        """Ease ``source`` into ``target`` at ``progress`` on the playhead.

        Returns an array with the TARGET's cardinality and dimensionality —
        structural continuity is maintained throughout: at progress 0 the
        output is source structure resampled onto the target parametrization;
        at progress 1 it is exactly ``target``.
        """
        a = np.atleast_2d(np.asarray(source, dtype=np.float64))
        b = np.atleast_2d(np.asarray(target, dtype=np.float64))
        e = _ease(progress, easing)

        # --- dimensionality resolution (pad / truncate) -------------------
        dim = b.shape[1]
        if a.shape[1] < dim:
            pad = np.zeros((a.shape[0], dim - a.shape[1]))
            a = np.hstack([a, pad])
        elif a.shape[1] > dim:
            a = a[:, :dim]

        # --- normalized-index point matching ------------------------------
        # Shared parametrization s in [0,1]: each structure is resampled onto
        # the target's point count. Upsampling inserts pseudo-points by linear
        # interpolation between neighbors; downsampling merges by striding.
        a_r = self._resample(a, b.shape[0])
        b_r = b

        # --- eased coordinate mapping --------------------------------------
        return (1.0 - e) * a_r + e * b_r

    @staticmethod
    def _resample(arr: np.ndarray, n_target: int) -> np.ndarray:
        """Resample ``arr`` onto ``n_target`` points via index correspondence.

        Position i of the output corresponds to normalized position
        ``s = i / (n_target - 1)`` of the source's own parametrization —
        the same contract MorphSVG uses to match differing path node counts.
        """
        n = arr.shape[0]
        if n == n_target:
            return arr.copy()
        s = np.linspace(0.0, 1.0, n_target)
        src = np.linspace(0.0, 1.0, n)
        out = np.empty((n_target, arr.shape[1]), dtype=np.float64)
        for d in range(arr.shape[1]):
            out[:, d] = np.interp(s, src, arr[:, d])
        return out

    def morph_weights(
        self,
        w_source: np.ndarray,
        w_target: np.ndarray,
        progress: float,
        easing: str = "power1.inOut",
    ) -> np.ndarray:
        """Morph neural-network weights during fine-tuning.

        Same contract as ``morph`` — supplied for intent clarity at call
        sites that tween adapter/parameter matrices.
        """
        return self.morph(w_source, w_target, progress, easing)
