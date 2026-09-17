# Harness Flaw vs Forged + Exoskeleton Defense

## The Harness Flaw

Traditional agent frameworks pack and unpack data continuously: binary DB rows, code structures, and memory traces are converted into multi-kilobyte **JSON strings** for the LLM. That **token tax** turns microsecond memory access into seconds of latency and inflates API cost.

## Does Forged solve this *before* it hits the Exoskeleton?

**Partially — by boundary and classification, not by replacing the runtime kernel.**

| Layer | What it does about token tax |
|-------|------------------------------|
| **Tekton Core** (IDE) | Curation happens *before* promotion; humans/agents choose what enters the vault. Does not implement Arrow Flight. |
| **Forged** | **Prevents wasteful promotion.** F0→F3 lifecycle, detector, quarantine, RocksDB Skills vs DuckDB Intelligence, vendor isolation, Capability = Tools + Harness. Stops *garbage and duplicate text* from becoming the hot path. Does **not** by itself keep live cognitive state in Arrow buffers. |
| **Exoskeleton** | **Runtime defense.** Cognitive state and telemetry live in **contiguous Apache Arrow** columnar buffers; **Arrow Flight** + **DuckDB** query/mutate **in place** with binary zero-copy pointers. Eliminates most serialize/deserialize on the inferential path. |

### Division of labor

```text
Tekton Core          ← curate / edit (reduce what is asked)
        ↓
Forged filing        ← govern / classify / store (F0–F3, no blind JSON dumps as source of truth)
        ↓
Exoskeleton kernel   ← execute on Arrow + Flight + DuckDB (zero-copy hot path)
        ↓
LLM (when needed)    ← receives *minimal* projected text, not the whole membrane as JSON
```

- **Forged** answers: *Should this become governed intelligence, and in what form?*  
  It reduces token tax **upstream** by not treating every artifact as chat context.
- **Exoskeleton** answers: *How does the running system touch state without packing it?*  
  It is the **Exoskeleton Defense** against the harness flaw on the hot path.

Forged alone does **not** fully solve the harness flaw if the runtime still round-trips Arrow/Duck state through JSON into the LLM on every step. The substrate (this repo’s `exoskeleton/transport`, `exoskeleton/db`) is required for the 90% data-movement claim.

## Exoskeleton Defense (canonical)

Cognitive state and system telemetry reside in contiguous **Apache Arrow** columnar memory. Using **Apache Arrow Flight** and **DuckDB** (Quack / in-process analytical path), the inferential kernel and execution engines query and mutate state **in place** via binary zero-copy pointers. That converts access from text accumulation to direct memory access and is the primary latency/cost defense at runtime.

## Practical rule

1. Curate in **Tekton Core**.  
2. Forge only what must be governed (**Forged**).  
3. Keep live state in **Exoskeleton** Arrow/Duck membranes.  
4. Project **thin** views to the LLM only when language is required — never rehydrate the full membrane as JSON by default.
