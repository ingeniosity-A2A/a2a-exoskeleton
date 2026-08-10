---
description: "Dual-tier DuckDB architecture — embedded Intellect client for O(1) context projection, persistent Core-Membrane server for analytics, connected via zero-copy quack:// Arrow streaming."
icon: database
---

# Dual-Tier DuckDB Architecture

To support **zero-latency analytical querying** and **state persistence**, the Exoskeleton integrates a dual-tier DuckDB embedded-to-remote topology. Two DuckDB instances serve fundamentally different roles — one transient and local, one persistent and remote — connected by the **Quack Remote Protocol** over zero-copy Arrow IPC.

{% hint style="info" %}
**Why two DuckDB instances?** The Intellect layer needs **instant** in-memory SQL for context projection (sub-millisecond). The Core-Membrane needs **persistent** storage for session history, telemetry, and cross-agent analytics. Splitting them keeps each tier optimized for its access pattern.
{% endhint %}

## Architecture Overview

```mermaid
graph TD
    classDef intellect fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef master fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef capability fill:#78350f,stroke:#fbbf24,stroke-width:2px,color:#fff;
    classDef compute fill:#831843,stroke:#f472b6,stroke-width:2px,color:#fff;
    classDef db fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#fff;

    subgraph L1 ["1. INTELLECT LAYER (Client Node)"]
        A["User Goal / Intent"] --> B["Intellect Engine"]
        B <--> DUCK_INTEL["DuckDB Embedded Client (:memory:)<br/>- Local Context Projection<br/>- In-Memory Arrow Formatting"]
        B -->|"Emits Intent Payload"| C["O(1) Context Budget (~53 tokens)"]
    end

    subgraph PROTOCOL ["ZERO-COPY REMOTE PROTOCOL LAYER"]
        DUCK_INTEL <===|"quack:// Remote Protocol (Arrow Stream)"| ===> DUCK_MEMB
    end

    subgraph L2 ["2. SUBSTRATE ENGINE & CORE-MEMBRANE"]
        C --> D["SubstrateEngine Dispatcher"]
        D --> E["DeltaState Patch Manager"]
        subgraph MEMBRANE ["Core-Membrane Analytics Engine"]
            DUCK_MEMB["DuckDB Server Engine (quack:// endpoint)<br/>- Persistent L0-L3 Delta Analytics<br/>- JSON / Parquet Storage<br/>- Arrow Zero-Copy Buffer Target"]
        end
        E <--> DUCK_MEMB
    end

    subgraph L3 ["3. COMPOSED CAPABILITY LAYER"]
        D --> G["ProcessVisualDocumentCapability"]
        G --> STEP1["Marker PDF Extraction"]
        STEP1 --> STEP2["Parallel LTX-2.3 Upscaling"]
    end

    subgraph L4 ["4. ALGORITHMIC COMPUTE CORE"]
        SLIDE["SLIDE Sparse Engine"]
        LiteParse["LiteParse Rust Engine"]
    end

    STEP1 <--> LiteParse
    DUCK_MEMB <--> SLIDE

    class A,B,C intellect;
    class D,E master;
    class G,STEP1,STEP2 capability;
    class SLIDE,LiteParse compute;
    class DUCK_INTEL,DUCK_MEMB db;
```

## Tier 1: Intellect Layer (Embedded Client)

An **in-memory DuckDB** engine embedded directly inside the Intellect node. It handles ultra-low-latency local operations that must complete before the model's next turn:

| Function | Latency | Purpose |
| --- | --- | --- |
| Local Context Projection | < 0.1ms | SQL transforms delta patches into ~53-token routing headers |
| In-Memory Arrow Formatting | < 0.05ms | Formats structured data for substrate dispatch |
| Capability Cache | < 0.01ms | Tracks invocation stats (count, avg duration, last status) |

### Context Projection

The Intellect DuckDB never exposes raw data to the model. Instead, it **projects** a minimal O(1) summary:

{% code title="IntellectDuckClient.project_minimal_context()" language="python" %}
def project_minimal_context(self, session_id: str) -> Dict[str, Any]:
    """Project minimal O(1) state into the LLM context.
    Raw data stays in DuckDB Arrow buffers.
    """
    rel = self.conn.execute("""
        SELECT
            COUNT(*) AS total_keys,
            MAX(updated_at) AS last_updated
        FROM active_context_projection;
    """)
    row = rel.fetchone()
    return {
        "session_id": session_id,
        "total_context_keys": row[0] if row else 0,
        "duckdb_connected": self._attached,
    }
{% endcode %}

{% hint style="success" %}
**Key Insight:** The model receives a ~53-token routing header. The actual data (session history, capability outputs, telemetry) stays in DuckDB Arrow columnar buffers. The model queries it via SQL, not by reading it into the prompt.
{% endhint %}

## Tier 2: Core-Membrane Layer (Quack Server)

A **persistent DuckDB** instance operating at the Core-Membrane, accessible over `quack://` for zero-copy Arrow streaming. This is the analytical backbone of the Exoskeleton.

### Schema Design

| Table | Purpose | Key Columns |
| --- | --- | --- |
| `session_deltas` | O(1) state rehydration patches | `session_id`, `turn_index`, `status`, `delta_payload` (JSON) |
| `execution_telemetry` | Per-phase timing and metadata | `telemetry_id`, `phase`, `duration_ms` |
| `l0_raw_events` | Raw ingestion stream | `event_id`, `event_type`, `payload` (JSON) |

### Analytical Queries

The Core-Membrane enables post-hoc analytical queries across full session histories:

{% code title="Aggregate session statistics from the membrane" language="sql" %}
SELECT
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(*)                   AS total_deltas,
    AVG(token_overhead)        AS avg_tokens_per_turn,
    SUM(token_overhead)        AS total_tokens
FROM session_deltas;
{% endcode %}

## Zero-Copy Protocol Layer

```
+-----------------------------------------------------------------------------------+
|                            1. INTELLECT LAYER (Client)                            |
|  - Embedded DuckDB (In-Memory / Local Cache)                                      |
|  - Performs immediate SQL transformations & Arrow table projections               |
+-----------------------------------------------------------------------------------+
                                   ||
                                   ||  quack:// Remote Protocol (Zero-Copy Arrow Stream)
                                   \/
+-----------------------------------------------------------------------------------+
|                        2. CORE-MEMBRANE LAYER (Server)                            |
|  - DuckDB Core Server Engine (Persisted / quack:// Listener)                      |
|  - Stores long-term L0-L3 state deltas, execution telemetry, & cross-agent memory|
+-----------------------------------------------------------------------------------+
                                   ||
                                   \/
+-----------------------------------------------------------------------------------+
|                        3. SUBSTRATE EXOSKELETON ENGINE                            |
|  - Dispatches non-blocking async capability pipelines                             |
|  - Offloads delta updates back to Core-Membrane DuckDB Server                     |
+-----------------------------------------------------------------------------------+
```

{% tabs %}
{% tab title="Intellect Client" %}

**Role:** Transient, in-memory, model-adjacent

* Connects to Core-Membrane via `ATTACH 'quack://...' AS core_membrane`
* Projects minimal context into the LLM prompt
* Caches capability invocation stats locally
* Never stores persistent data — re-created each session

{% endtab %}
{% tab title="Core-Membrane Server" %}

**Role:** Persistent, analytical, cross-agent

* Stores session deltas with UPSERT semantics
* Ingests raw L0 telemetry events
* Enables aggregate analytics across all sessions
* Exposes `quack://` endpoint for Intellect attachment

{% endtab %}
{% tab title="Data Flow" %}

**Write path:** Intent → Substrate → Capability → DeltaState → Core-Membrane `INSERT`

**Read path:** Intellect → `ATTACH quack://` → SQL query → Arrow batch → Context projection

**Key property:** Data flows as Arrow columnar buffers. Zero serialization. Zero copies.

{% endtab %}
{% endtabs %}

## Repository Integration

The dual-tier DuckDB is implemented in `exoskeleton/db/`:

```
exoskeleton/db/
├── __init__.py
├── duck_intellect.py     # IntellectDuckClient (:memory:)
└── duck_membrane.py     # CoreMembraneDuckServer (persistent, quack://)
```

<details>

<summary>References</summary>

* DuckDB: An Analytical In-Process SQL Database System (Grosse et al., VLDB 2025)
* Quack Remote Protocol — DuckDB Server documentation
* Apache Arrow IPC: Zero-copy data interchange format
* [Big Lake Server — Core-Membrane](big-lake-server.md) — Persistent storage layer
* [Quack Remote Protocol](quack-protocol.md) — Distributed A2A intelligence

</details>