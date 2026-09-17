# GSAP Kernel / TEK — Location Index

**Canonical name evolution (from Ava007 worklog):**  
GSAP Kernel → **TEK (Temporal Execution Kernel)** — GSAP is the engine; TEK is the architectural name.

## Where it lives now

| Location | What |
|----------|------|
| **`forged-ai-filing-os/components/bento/gsap_semantic_trigger.ts`** | **Primary live code** — expand timeline → SemanticExplorer / turbovec search; F0–F3 stage slides; split-text; odometer; upload ripple |
| **`forged-ai-filing-os/components/bento/SemanticExplorer.tsx`** | UI that TEK timelines drive |
| **`Ava007/bento-ui8-master-skills-set-gsap.md`** | Skill doc — Bento + GSAP patterns (archived monorepo; still readable) |
| **`QAG-MemBrain`** | Product identity: *Quantum Atom GSAP Memory Brain* — temporal memory layer; GSAP as audit/timeline across interactions |
| **`Core-Membrain/memory/temporal/`** | Temporal / GSAP memory hooks (absorbed path → QAG-MemBrain `memory/core-membrain/`) |
| **`Ava007-Omni-OS`** | Edge description includes GSAP (modem/telemetry bridge) |
| **gitbook-ingest worklog (now `wiki/gitbook-ingest/`)** | History: `src/lib/gsap-kernel/` → renamed `src/lib/tek/`; TEKPanel; ADR-009 |

## What was in Ava007 (historical)

From worklog Task 4–5 (before archive):

```text
src/lib/gsap-kernel/   →  renamed src/lib/tek/
  types.ts
  timeline-factory.ts   # KernelTimeline, six-phase cascade
  plugins.ts
  index.ts
src/components/GSAPKernelPanel.tsx  →  TEKPanel.tsx
ADR-009: GSAP Kernel as Temporal Execution Engine
```

Those paths lived on the **Ava007** monorepo (now ARCHIVED). Recover from git history there if full TEK source is needed; do not re-home TEK inside Cybernetic-Ava007 Intellect.

## Correct homes going forward

| Concern | Repo |
|---------|------|
| Bento / SemanticExplorer timelines | **forged-ai-filing-os** (already) |
| Temporal memory / GSAP audit layer | **QAG-MemBrain** |
| Edge timeline triggers | **Ava007-Omni-OS** |
| IDE-side animation of edits/checkpoints | **void/** (optional later) |
| Cognitive loop timing | **Cybernetic-Ava007** `cybernetic/` — not GSAP DOM timelines |

## Free buff

You already have Freebuff consolidation capacity and Intellect-side loops.  
**Do not** merge Void Agent into Ava007 to “gain” an agent — that would fight Freebuff and the three-repo boundary.
