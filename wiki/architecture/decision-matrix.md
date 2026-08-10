---
description: "The Inject/Build/Decline Decision Matrix — a tri-state architectural gate for evaluating every addition or enhancement to the A2A Exoskeleton substrate."
icon: shield-check
---

# The Inject / Build / Decline Decision Matrix

Every proposed addition to the A2A Exoskeleton must pass through a **tri-state architectural gate** before entering the substrate. This matrix prevents the framework from accumulating the very bloat it was designed to eliminate — O(N) context expansion, prompt pollution, and redundant orchestration layers.

The three verdicts are not subjective preferences. They are **structural consequences** determined by where a proposed component deploys within the 4-layer stack and whether it preserves or violates the O(1) context invariant.

{% hint style="warning" %}
**This is not a style guide.** Each verdict is derived from the substrate's performance contracts. A component that "HURTS" will measurably degrade context scaling. A component that is "NOT NEEDED" is already superseded by an existing substrate mechanism. A component that "ENHANCES" must compose into the O(1) primitive layer without increasing per-turn token overhead.
{% endhint %}

## The Meta-Harness Case Study

The Decision Matrix was formalized from a critical design question: **Should the Exoskeleton include a meta-harness?** The answer depends entirely on *where* the harness deploys.

### 1. Why a Prompt-Level Meta-Harness HURTS

Wrapping the Intellect (LLM) in a meta-harness that injects routing logic, tool schemas, and orchestration rules directly into the prompt context **actively degrades** the framework. This is the most dangerous deployment layer because it corrupts the substrate's primary performance invariant.

* **Context Collapse (O(N) Token Expansion):** As capability volume (N) scales, a meta-harness forces the model to hold all harness schemas and state loops in its context window. At N=100, over 99% of context space is consumed by structural harness bloat rather than productive task reasoning. The substrate's 53-token/turn contract collapses to thousands of tokens per turn — exactly the Matrix-Force dependency the Exoskeleton was built to break.

* **Inflated Latency:** Evaluating meta-harness instructions inside the model context forces sequential LLM re-prompting cycles. Every routing decision that could have been resolved in microseconds by the SubstrateEngine now requires a full inference pass, driving perceived latency from sub-second execution up to tens of seconds.

* **Pollutes Attention:** Heavy meta-instructions cause prompt crowding, triggering high error rates and attention drift on complex multi-turn tasks. The model's limited attention budget is split between actual reasoning and parsing harness control flow — a zero-sum trade that always degrades reasoning quality.

### 2. Why an External Meta-Harness is NOT NEEDED

The Exoskeleton Substrate natively replaces the responsibilities of a traditional meta-harness **without loading any instructions into the LLM context window**. This is not an optimization — it is an architectural substitution. Each traditional meta-harness responsibility maps to an existing substrate component:

* **Native Substrate Orchestration:** The `SubstrateEngine` handles task dispatching, parallel branching, step sequencing, and cancellation (`easeReverse`) off-thread in pure Python/Rust/WASM. No prompt instructions required — the engine is the orchestrator, not the LLM.

* **Dual DuckDB State Transport:** State tracking and session history are stored as binary deltas in the DuckDB Core-Membrane (`quack://`) and projected via an embedded in-memory Intellect client. The LLM does not need a meta-harness to carry history strings across turns — the substrate transports state below the context layer entirely.

* **O(1) Context Budget:** State rehydration occurs through lightweight 53-token delta patches rather than prompt-level harness wrappers. The substrate guarantees that adding more capabilities does not increase per-turn token cost — a property that would be impossible if a meta-harness sat in the prompt.

### 3. How "The Harness That Becomes a Tool" ENHANCES (Section 6.5)

The Exoskeleton does not eliminate harness logic entirely; instead, it **demotes the harness from a system-wrapper into an internal capability primitive** using the GSAP Nested Timeline pattern. This is the only deployment layer where harness logic receives an **ENHANCES** verdict:

* **Encapsulated Multi-Step Workflows:** Complex workflows (e.g., `MarkerExtractionCapability` + `LTXUpscaleCapability`) are wrapped inside a single executable harness like `ProcessVisualDocumentCapability`. The composition happens at the substrate layer, not the prompt layer.

* **Zero Prompt Tax:** To the Intellect, the entire multi-step harness looks like a single addressable tool call. The internal complexity — parallel branches, sub-step sequencing, error isolation — is invisible to the LLM. The model emits one intent; the substrate handles the rest.

* **Local Sub-Sequence Execution:** The internal harness manages `asyncio.gather` parallel branches and fast-exit `easeReverse` unwinds entirely outside the context window. Even if a composed capability contains 10 sub-steps, the token overhead remains 53.

## The Paradigm Decision Matrix

| Deployment Layer | Architectural Impact | Substrate Verdict | Rationale |
| --- | --- | --- | --- |
| **LLM Context Window** (Prompt Wrapper) | HURTS | **DECLINE** | Causes O(N) context collapse, prompt pollution, and high token costs. Violates the 53-token/turn invariant. |
| **External Orchestration Framework** | NOT NEEDED | **DECLINE** | Fully superseded by the SubstrateEngine and dual DuckDB state pipeline. Adding an external layer introduces redundant routing. |
| **Substrate Capability Primitive** (Section 6.5) | ENHANCES | **INJECT / BUILD** | Transforms complex multi-step pipelines into single O(1) addressable tools. Preserves the 53-token contract. |

## Applying the Matrix: General Decision Rules

The meta-harness case study yields a **generalizable decision framework**. For any proposed component — not just harnesses — evaluate against these three deployment layers:

{% stepper %}
{% step %}

### Step 1: Identify the Deployment Layer

Determine where the proposed component would execute. Does it inject into the LLM prompt? Does it wrap the substrate externally? Or does it compose into the substrate as an internal primitive?

{% endstep %}
{% step %}

### Step 2: Measure the Token Impact

If the component adds tokens to the per-turn context budget, it deploys at Layer 4 (LLM Context Window) and must be **DECLINED** — regardless of its functional value. The substrate's O(1) invariant is non-negotiable.

{% endstep %}
{% step %}

### Step 3: Check for Substrate Supersession

If the component duplicates functionality already handled by the SubstrateEngine, DuckDB, Arrow IPC, or another substrate primitive, it must be **DECLINED** as redundant. External wrappers that re-implement substrate behavior add latency without adding capability.

{% endstep %}
{% step %}

### Step 4: Verify O(1) Composition

If the component composes into the substrate as a capability primitive — encapsulating complexity behind a single intent interface with zero prompt tax — it receives an **INJECT / BUILD** verdict. The component must prove it preserves the 53-token/turn contract at any capability count N.

{% endstep %}
{% endstepper %}

## Extended Decision Matrix

Beyond the meta-harness case, the matrix applies to every architectural proposal:

| Proposed Component | Deployment Layer | Token Impact | Substrate Supersession | Verdict |
| --- | --- | --- | --- | --- |
| Meta-harness in prompt | LLM Context | O(N) expansion | N/A | **DECLINE** |
| External orchestration framework | External Wrapper | None | Yes — SubstrateEngine | **DECLINE** |
| Composed capability harness | Substrate Primitive | 0 (O(1)) | No | **INJECT / BUILD** |
| Raw tool schema injection | LLM Context | O(N) schemas | Yes — Lazy Materialization | **DECLINE** |
| Full context re-injection | LLM Context | O(N) per turn | Yes — DeltaState patches | **DECLINE** |
| GPU-required capability | Substrate Primitive | 0 (O(1)) | No (if lazy-loaded) | **INJECT / BUILD** |
| Synchronous blocking tool | Substrate Primitive | 0 but blocks | Partial — async required | **BUILD with async** |
| Centralized state string in prompt | LLM Context | O(N) growth | Yes — DuckDB + quack:// | **DECLINE** |
| Per-capability reverse handler | Substrate Primitive | 0 (O(1)) | No | **INJECT / BUILD** |
| Model-agnostic routing layer | External Wrapper | None | Yes — SubstrateEngine dispatch | **DECLINE** |

## Architectural Consequences

### The DECLINE Verdict Protects the Invariant

Every DECLINE decision preserves the substrate's core performance contract: **53 tokens per turn regardless of N**. This is not conservatism — it is structural discipline. The Matrix-Force dependence that the Exoskeleton breaks is precisely the tendency to load more into the prompt than the substrate can handle. The Decision Matrix is the enforcement mechanism.

### The INJECT / BUILD Verdict Requires Proof of O(1)

An ENHANCES verdict is not free. Any component that receives INJECT / BUILD must demonstrate:

* **Zero prompt tax** — the LLM sees only an intent name, not internal structure
* **Encapsulated execution** — all sub-steps run inside the substrate, not in the context window
* **Lazy materialization** — model artifacts, GPU weights, or heavy resources load only on first invocation
* **easeReverse support** — the capability must define an asymmetrical unwind protocol for interruption

### The Matrix is Recursive

The Decision Matrix applies to itself. If a proposed enhancement to the matrix would inject rules into the LLM prompt, it must be DECLINED. The matrix exists as substrate-level architectural governance — not as prompt-level instructions for the Intellect.

{% hint style="success" %}
**The Decision Matrix completes the Exoskeleton's self-governing architecture.** The substrate already handles execution (SubstrateEngine), state (DuckDB), transport (Arrow IPC), and rollback (easeReverse). The Decision Matrix handles **architectural evolution** — ensuring every addition preserves the properties that make the substrate work.
{% endhint %}

## Relationship to Other Architectural Decisions

| Concept | How the Matrix Governs It |
| --- | --- |
| **Lazy Materialization** | ENHANCES — zero footprint at rest, O(1) on invoke. The matrix confirms this is a valid substrate primitive. |
| **DeltaState Patches** | ENHANCES — replaces full context re-injection. The matrix would DECLINE any proposal to switch back to full re-injection. |
| **Dual-Tier DuckDB** | ENHANCES — state transport below the context layer. The matrix would DECLINE any proposal to move state into the prompt. |
| **easeReverse Rollback** | ENHANCES — per-capability asymmetrical unwind. The matrix would DECLINE any proposal for a centralized rollback manager in the prompt. |
| **GSAP Orchestration** | ENHANCES — off-thread timeline coordination. The matrix would DECLINE any proposal to move orchestration rules into the LLM context. |

<details>

<summary>References</summary>

* [1] GSAP Orchestrated easeReverse — Per-tween asymmetrical rollback control
* [2] Agent57: Outperforming the Atari 100K Benchmark (Badia et al., 2020)
* [3] DuckDB Quack Remote Protocol — Zero-copy Arrow streaming
* [4] A2A Exoskeleton Wiki — [GSAP Orchestration Engine](gsap-orchestration.md)
* [5] A2A Exoskeleton Wiki — [Orchestrated easeReverse](easeReverse-orchestration.md)
* [6] A2A Exoskeleton Wiki — [No-GPU Intelligence Stack](no-gpu-intelligence-stack.md)

</details>
