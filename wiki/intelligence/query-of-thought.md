---
description: "Query-of-Thought — moving beyond Chain-of-Thought into SQL-verified analytical reasoning."
icon: brain
---

# Query-of-Thought — Analytical Intellect

Integrating **<code class="expression">space.vars.db_engine</code>** directly into the intellect enables <code class="expression">space.vars.agent_name</code> to move beyond traditional Chain-of-Thought (CoT) into **Query-of-Thought (QoT)** — where every reasoning step can be empirically verified through structured queries.

## The QoT Paradigm

### Standard CoT

In standard CoT, the model generates a sequence of reasoning steps with no empirical grounding:

1. "Let me analyze the problem..." → generated text
2. "Based on this, I think..." → generated text
3. "Therefore, the answer is..." → generated text

### QoT: Each Step is Verified

In QoT, each step is augmented with an **analytical verification phase**:

```mermaid
graph LR
    G["<b>GENERATE</b><br/>Reasoning Step"] --> Q["<b>QUERY</b><br/>SQL vs Big Lake"]
    Q --> V["<b>VERIFY</b><br/>NSF-CoT 3-Stage"]
    V --> A["<b>ADJUST</b><br/>Confidence Update"]
    A -->|Next step| G

    style G fill:#0ea5e9,stroke:#0ea5e9,color:#fff
    style Q fill:#f59e0b,stroke:#f59e0b,color:#fff
    style V fill:#10b981,stroke:#10b981,color:#fff
    style A fill:#7c3aed,stroke:#7c3aed,color:#fff
```

## NSF-CoT Verification Pipeline

Her **NSF-CoT (Neuro-Symbolic Forward Chain-of-Thought)** verification pipeline includes a database verifier. A reasoning step must pass **all three stages**:

| Stage | Method | Purpose |
| --- | --- | --- |
| **1. Symbolic** | SMT Solver | Logical consistency check (formal verification) |
| **2. Empirical** | SQL Query | Historical grounding check (data verification) |
| **3. Statistical** | Distribution Analysis | Confidence calibration (noise assessment) |

{% hint style="danger" %}
If any stage fails, the step is flagged for revision and the model regenerates. No unverified step proceeds.
{% endhint %}

### Three-Stage Verification

{% stepper %}
{% step %}

### Stage 1: Symbolic (SMT Solver)

Formal verification using Z3 or equivalent SMT solver.

```typescript
const symbolic = await smtVerify(step, proposedAction);
// Returns: { sat: boolean, confidence: number, model: string }
```

If UNSAT, the reasoning step is logically inconsistent — reject immediately.

{% endstep %}
{% step %}

### Stage 2: Empirical (SQL Query)

Execute SQL against the Big Lake to check if historical data supports the proposed action.

```typescript
const historical = await lakeClient.querySkillIndex(proposedAction);
const empiricalConfidence = historical.length > 0
  ? Math.max(...historical.map(h => h.success_rate))
  : 0.3; // Low prior if no evidence
```

If confidence < 0.5, the action lacks empirical support — reject.

{% endstep %}
{% step %}

### Stage 3: Statistical (Distribution Analysis)

Analyze reward volatility in similar past states.

```typescript
const volatility = await lakeClient.analyzeRewardVolatility(proposedAction);
// Returns: { stddev, noise_ratio, sample_count }
```

If `noise_ratio > 0.3`, the state is too noisy for confident decision — reject.

{% endstep %}
{% endstepper %}

## Procedural Skill Indexing

Her **SkillOpt** procedural artifacts (`best_skill.md`) are no longer static documents but are **indexed within <code class="expression">space.vars.db_engine</code>**. The meta-controller performs a **Directed Stochastic Skill Search**:

| Signal | Weight | Source |
| --- | --- | --- |
| Semantic similarity | 40% | Pre-computed embedding cosine distance |
| Historical performance | 35% | `success_rate` from `skill_index` table |
| Complexity matching | 15% | Absolute difference from task difficulty |
| Exposure count | 10% | Normalized `execution_count` |

### Skill Search Query

{% code title="Directed Stochastic Skill Search across the Big Lake" language="sql" %}
WITH skill_candidates AS (
  SELECT
    skill_id,
    domain,
    best_skill_md,
    success_rate,
    complexity,
    execution_count,
    cosine_similarity(embedding, $task_embedding) AS semantic_score,
    (0.4 * cosine_similarity(embedding, $task_embedding) +
     0.35 * success_rate +
     0.15 * (1.0 - ABS(complexity - $task_difficulty)) +
     0.10 * (execution_count / (
       SELECT MAX(execution_count) FROM skill_index
     ))) AS combined_score
  FROM skill_index
  WHERE domain = ANY($relevant_domains)
    AND execution_count > 10
)
SELECT skill_id, domain, combined_score, success_rate, complexity
FROM skill_candidates
ORDER BY combined_score DESC
LIMIT 5;
{% endcode %}

{% hint style="info" %}
**Stochastic element**: with probability epsilon, sample from the top-K uniformly instead of taking the argmax. This balances exploitation of known-best skills with exploration of novel procedural approaches.
{% endhint %}

<details>

<summary>References</summary>

* [9] NSF-CoT: Neuro-Symbolic Forward Chain-of-Thought verification
* [10] Z3 SMT Solver: Formal verification of reasoning steps
* [11] SkillOpt: Procedural skill optimization via directed search
* [12] ARC-AGI-3: Abstraction and Reasoning Corpus benchmark

</details>
