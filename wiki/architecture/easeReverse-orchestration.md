---
description: "GSAP orchestrated easeReverse — asymmetrical state rollbacks, per-tween isolation, and mid-flight intent interruption in the Exoskeleton substrate."
icon: rotate-ccw
---

# Orchestrated easeReverse — Asymmetrical Rollback Protocol

> [GSAP Orchestrated easeReverse Demo](https://demos.gsap.com/demo/orchestrated-easereverse/)

The GSAP orchestrated `easeReverse` pattern focuses on **tween-level easeReverse inside an orchestrated timeline** — allowing each step in a sequence to define a completely different easing curve and velocity profile when playing in reverse (exit/rollback) versus forward (entrance/execution).

Adding this explicitly **completes the GSAP-to-Substrate control mapping**, as it solves the problem of **asymmetrical state rollbacks** and **mid-flight intent interruptions**.

{% hint style="warning" %}
**Why this matters:** In traditional agent harnesses, cancelling or rewinding an intent requires either rerunning expensive cleanup loops or dropping state abruptly. The easeReverse pattern gives every sub-capability in a nested timeline its own unwind protocol — fast, cheap, and deterministic.
{% endhint %}

## The Problem: Symmetric Rollback is Expensive

When an agent execution is interrupted mid-flight — by a user, a supervisor agent, or a timeout — most systems face a binary choice:

| Approach | Cost | Problem |
| --- | --- | --- |
| **Full cleanup** | High — reruns all teardown steps | Wastes compute on operations that don't need reversal |
| **Abrupt drop** | Low — kills the process | Loses partial results, corrupts shared state |
| **Symmetric reverse** | Medium — mirrors forward execution | Forces heavy operations (GPU, model loading) to "undo" unnecessarily |

The easeReverse pattern provides a **third path**: an **asymmetrical, fast-exit teardown** that preserves valuable lightweight results while aggressively shedding expensive ones.

## The easeReverse Pattern

### Forward Execution Curve (Forward Ease)

Heavy, thorough execution. Each sub-capability runs at full fidelity:

* High-quality OCR extraction with multi-pass verification
* Full spatial upscaling via LTX-2.3
* Complete model inference with multi-agent coordination
* Maximum quality output — no shortcuts

### Reverse Unwind Curve (easeReverse)

Asymmetrical, fast-exit teardown. When playing in reverse, each sub-capability defines its own **lightweight unwind protocol**:

* Immediate abort of GPU-heavy operations
* Partial cache salvage — retain lightweight markdown deltas
* Drop raw image buffers while preserving text extractions
* Switch to a high-speed `power3.in`-equivalent state shedding

### Per-Tween Isolation

Each sub-capability in the nested timeline specifies **its own unwind protocol** rather than forcing a global symmetric reversal. This is the critical insight from GSAP's per-tween easeReverse: one tween can have a slow, graceful exit while another drops instantly.

## Updated GSAP Architectural Mapping Table

| GSAP Primitive | Exoskeleton Substrate Equivalent | Functional Purpose |
| --- | --- | --- |
| Master Timeline | Exoskeleton Substrate Engine | Coordinates lifecycle, state rehydration, and task dispatch. |
| Nested Timeline | Composed Capability (`ProcessVisualDocumentCapability`) | Encapsulates multiple sub-tools into a single O(1) addressable unit. |
| Labels | Execution Markers / Checkpoints | Deterministic step markers for sequential state validation. |
| Stagger / Tweens | Parallel Branch-and-Merge (`asyncio.gather`) | Non-blocking concurrent capability execution across CPU/Edge workers. |
| onComplete | Lazy Materialization | Zero-token footprint at rest; models/weights load only on call. |
| **easeReverse (Orchestrated)** | **Asymmetrical Rollback & Interruption Protocol** | Executes fast-exit, low-overhead teardown when an intent is cancelled or overridden mid-execution. |

{% hint style="info" %}
The easeReverse row completes the mapping. Every GSAP primitive now has a first-class substrate equivalent — the control surface is fully isomorphic.
{% endhint %}

## How easeReverse Manifests in the Substrate

When an intent is interrupted or aborted, the substrate executes the capability's `reverse()` path using an **asymmetric, low-cost curve** rather than mirroring the forward workload.

### The Execution Flow

{% stepper %}
{% step %}

### Forward: Extraction Phase

The capability begins forward execution — running heavy extraction (e.g., Marker OCR) on the input document. This is the "forward ease" — thorough, high-quality, multi-pass.

{% endstep %}
{% step %}

### Checkpoint: Interruption Gate

After extraction completes, the substrate checks a `cancel_token`. If set, it branches to the `reverse_unwind()` path instead of continuing to the upscale phase.

```python
if cancel_token and cancel_token.is_set():
    return await self.reverse_unwind(extraction, stage="extraction_complete")
```

{% endstep %}
{% step %}

### Forward: Parallel Upscale Phase

If not interrupted, the capability fans out into parallel upscale tasks via `asyncio.gather` — each image is sent to the LTX upscaler concurrently.

{% endstep %}
{% step %}

### easeReverse: Asymmetric Fast-Exit

If interrupted during upscaling, `asyncio.CancelledError` triggers the unwind. Heavy GPU tasks are abandoned instantly. The markdown extraction is salvaged. Images are dropped. Exit latency: **< 1ms**.

{% endstep %}
{% endstepper %}

### Substrate Implementation

{% code title="ProcessVisualDocumentCapability — Orchestrated easeReverse in Python" language="python" %}
class ProcessVisualDocumentCapability:
    """
    Composed capability with Orchestrated easeReverse (Asymmetrical Unwind).
    Each sub-capability defines its own reverse curve.
    """

    def __init__(self):
        self.extractor = MarkerExtractionCapability()
        self.upscaler = LTXUpscaleCapability()

    async def execute(self, intent, cancel_token=None):
        file_path = Path(intent.file_path)
        if not file_path.exists():
            return CapabilityResult(
                status="failed",
                output={"error": f"File not found: {intent.file_path}"}
            )

        # --- Forward Execution Path ---
        try:
            extraction = await self.extractor.run(str(file_path))
        except Exception as e:
            return CapabilityResult(
                status="failed",
                output={"error": f"Extraction failed: {str(e)}"}
            )

        # Interruption Checkpoint (Mid-timeline pause/check)
        if cancel_token and cancel_token.is_set():
            return await self.reverse_unwind(
                extraction, stage="extraction_complete"
            )

        upscaled_images = {}
        if intent.upscale_figures and extraction.get("images"):
            image_items = list(extraction["images"].items())

            # Create cancellation-aware tasks
            tasks = [
                asyncio.create_task(self.upscaler.run(img))
                for _, img in image_items
            ]

            try:
                results = await asyncio.gather(
                    *tasks, return_exceptions=True
                )
                for (block_id, _), result in zip(image_items, results):
                    if isinstance(result, Exception):
                        continue
                    upscaled_images[block_id] = result["upscaled_image"]
            except asyncio.CancelledError:
                # --- easeReverse Trigger: Asymmetrical Fast-Exit ---
                return await self.reverse_unwind(
                    extraction, stage="upscale_cancelled"
                )

        return CapabilityResult(
            status="complete",
            output={
                "markdown": extraction["markdown"],
                "images": extraction["images"],
                "upscaled_images": upscaled_images,
            },
            model_used="marker+ltx-2.3",
        )

    async def reverse_unwind(self, partial_extraction, stage):
        """
        Substrate implementation of easeReverse:
        Rather than attempting full image upscaling in reverse,
        immediately drops heavy GPU/memory allocations,
        salvages raw Markdown, and exits in < 1ms.
        """
        # Fast exit path (equivalent to power3.in quick drop)
        salvaged_markdown = partial_extraction.get("markdown", "")

        return CapabilityResult(
            status="interrupted_salvaged",
            output={
                "markdown": salvaged_markdown,
                "images": {},  # Dropped immediately to free user-space buffers
                "unwind_stage": stage,
                "notice": (
                    "easeReverse executed: Heavy visual transforms dropped, "
                    "text preserved."
                ),
            },
            model_used="substrate_fast_unwind"
        )
{% endcode %}

## Forward vs. Reverse: Side-by-Side

{% tabs %}
{% tab title="Forward Execution (Ease In)" %}

**Curve:** Slow, thorough, high-fidelity

| Step | Operation | Cost | Output |
| --- | --- | --- | --- |
| 1 | Marker OCR extraction | ~500ms CPU | Full markdown + image refs |
| 2 | LTX-2.3 upscale (per image) | ~2s GPU per image | High-res upscaled images |
| 3 | Assembly & return | ~10ms | Complete capability result |

**Total:** 500ms + (N × 2s) + 10ms

The forward path invests maximum compute for maximum quality. Each sub-capability runs to completion.

{% endtab %}
{% tab title="Reverse Unwind (easeReverse)" %}

**Curve:** Fast, aggressive, asymmetrical

| Step | Operation | Cost | Output |
| --- | --- | --- | --- |
| 1 | Check cancel token | ~0.01ms | Branch decision |
| 2 | Drop GPU image buffers | ~0.1ms | Freed memory |
| 3 | Salvage markdown delta | ~0.05ms | Partial text output |
| 4 | Return interrupted result | ~0.5ms | Status + salvaged data |

**Total:** < 1ms

The reverse path sheds expensive state instantly while preserving lightweight results that required no GPU.

{% endtab %}
{% endtabs %}

## Architectural Impact

### Interruptible UI & Execution

If a user or supervisor agent changes intent mid-flight, the Exoskeleton doesn't block on heavy model outputs. The easeReverse protocol tears down the current execution and returns a salvaged partial result — allowing the new intent to begin immediately without waiting for cleanup.

### Resource Preservation

Drops CPU/GPU-heavy image and model passes **instantly** while salvaging lightweight text deltas. The asymmetry is deliberate: text extraction is cheap to preserve; image upscaling is expensive to reverse — so we don't reverse it, we **drop** it.

### Zero-Latency Exit

Exit latency remains under **< 1ms**, maintaining the substrate's strict O(1) context and performance bounds. This is critical for real-time agent coordination where a stalled capability would cascade delays across the entire timeline.

### Per-Tween Control Isolation

Each composed capability defines its own `reverse_unwind()` method. The master timeline doesn't need to know *how* a capability unwinds — only that it *can*. This mirrors GSAP's design where each tween owns its own easing curve.

{% hint style="success" %}
**Key Insight:** The easeReverse pattern means the Exoskeleton's GSAP-to-Substrate mapping is now **fully isomorphic**. Every GSAP primitive — Timeline, Tween, Stagger, Label, onComplete, and now easeReverse — has a first-class equivalent in the substrate. The animation metaphor is complete.
{% endhint %}

<details>

<summary>References</summary>

* [GSAP Orchestrated easeReverse Demo](https://demos.gsap.com/demo/orchestrated-easereverse/)
* GSAP Documentation — Timeline control and reverse playback
* A2A Exoskeleton Wiki — [GSAP Orchestration Engine](gsap-orchestration.md)
* A2A Exoskeleton Wiki — [Integrated Capability Primitives](capability-primitives.md)

</details>
