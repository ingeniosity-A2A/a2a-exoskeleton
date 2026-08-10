---
description: "Unified Collapse — collapsing the distinction between tools and harnesses, achieving 30% to 95% productive thinking."
icon: puzzle-piece
---

# Integrated Capability Primitives

**Integrated Capability Primitives** (Unified Primitives) represent a fundamental architectural shift in how AI agents interact with tools and workflows. This is the centerpiece of the **Capability Layer (Layer 3)** within the Exoskeleton architecture.

## The Problem: Orchestration Waste

Current AI systems suffer from massive **orchestration overhead**. When a model needs to use a tool, it must:

1. Reason about which tool to select from a complex schema
2. Construct the correct parameter payload
3. Handle execution errors and retries
4. Parse and interpret the result
5. Decide what to do next based on the result

This "orchestration tax" consumes up to **70% of a model's productive thinking capacity**, leaving only 30% for actual domain reasoning.

## The Solution: Unified Collapse

The primary function of these primitives is to **collapse the distinction** between simple **tools** (single functions) and complex **harnesses** (multi-step workflows).

* **Identical Appearance**: Both a simple API call and a complex multi-agent coordination process appear **identical** to the model's reasoning core
* **Abstraction of Complexity**: The model interacts with the world by emitting a single, unified **"Intent" call** that remains constant, regardless of task complexity

### The Productivity Leap

By removing orchestration waste, the system moves a model from **30% to 95% productive thinking** — effectively producing **three times more productive output** from the same compute budget.

{% hint style="success" %}
**Before**: 30% productive / 70% orchestration
**After**: 95% productive / 5% system overhead
{% endhint %}

## Cybernetic Cures

For these primitives to work without polluting the model's context, they rely on four mechanisms:

### 1. Context Rehydration

The system keeps the model's "spine" lean by only providing the **specific context needed** for a particular turn. No accumulated state, no growing prompt windows.

### 2. Lazy Prompt Topology

Instructions are **modularized** and only "rehydrated" on-demand. This prevents "chest crushing" (prompt accumulation) that degrades performance near token limits. Each instruction module is loaded lazily, like a virtual memory page fault.

### 3. Substrate Parallelism

The architecture uses **speculative execution** and parallel "branch-merge" processing to hide the latency of complex tasks from the model. While the model thinks about the next step, the substrate is already executing potential futures in parallel.

### 4. Compartmentalization

Every capability is contained in an **isolated execution environment**, preventing interference between different tools or harnesses. A failing tool cannot corrupt the state of an unrelated workflow.

## Comparison: Traditional vs. Integrated

| Aspect | Traditional Primitives | Integrated Capability Primitives |
| --- | --- | --- |
| State | Stateless function calls | Durable, auditable **Tasks** |
| Complexity | Exposed to model | Abstracted behind Intent interface |
| Provenance | None | Full state history preserved |
| Collaboration | Requires exposing internal logic | Agents collaborate via Task contracts |
| Context impact | Accumulates (chest crushing) | Rehydrated on-demand (lean spine) |

## The Intent Registry

Both tools and harnesses are registered identically:

{% tabs %}
{% tab title="Simple Tool" %}

```typescript
// A simple DuckDB query — registered as an Intent
capabilityRegistry.set('duckdb_query', async (payload) => {
  const { sql } = payload as { sql: string };
  const result = await lakeClient.query(sql);
  return { success: true, data: result, provenance: track('duckdb_query') };
});
```

{% endtab %}
{% tab title="Complex Harness" %}

```typescript
// A full multi-agent pipeline — IDENTICAL interface
capabilityRegistry.set('full_arc_agi_solver', async (payload) => {
  const { task } = payload as { task: ARCAGITask };
  // Internally: 15+ steps, parallel branches, sub-agent coordination
  const result = await arcSolverPipeline.execute(task);
  return { success: true, data: result, provenance: track('arc_solver') };
});
```

{% endtab %}
{% endtabs %}

The model sees **no difference** between these two calls.

## Lazy Rehydration Example

{% stepper %}
{% step %}

### Module Request

The reasoning loop requests a context module by ID and current task parameters.

```typescript
const context = await topology.rehydrate('duckdb_query_guide', {
  currentTask: 'Analyze trajectory patterns',
  availableTables: ['experiences', 'hidden_states', 'skill_index'],
});
```

{% endstep %}
{% step %}

### On-Demand Load

The module is loaded lazily (like a page fault) and rendered with only the context needed for this specific turn.

{% endstep %}
{% step %}

### Evict After Use

After the turn completes, the module is evicted to keep the model's spine lean.

```typescript
topology.evict('duckdb_query_guide');
```

{% endstep %}
{% endstepper %}

<details>

<summary>References</summary>

* [1] Integrated Capability Primitives — Unified Primitives (ADK spec)
* [2] Productivity Leap: 30% → 95% productive thinking (ADK benchmark)
* [4] A2A Task Schema: Durable, auditable agent contracts
* [5] Google ADK Task Context: ToolContext.state shared dictionary

</details>
