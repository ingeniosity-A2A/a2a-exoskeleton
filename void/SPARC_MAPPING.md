# Void → SPARC Mapping — Complete

**Void** = local-first AI code editor (Electron + Monaco + React 19).  
No middleman backend. Direct provider or local model access.

## Layer Mapping

| SPARC Layer | Void Feature | Output Path |
|-------------|--------------|-------------|
| **Intake** | Direct providers (OpenAI, Anthropic, Gemini, Mistral, Groq) + local (Ollama/vLLM/LM Studio) + OpenAI-compatible endpoints + model provenance (`repo_id`, revision, commit) | `/intake/raw/`, `/intake/parsed/`, `sources/` |
| **Separation** | Agent Mode (full tools) + Gather Mode (read-only) + EditCodeService (streaming diffs) + VoidModelService | `/separated/primitives/*.yaml` |
| **Coordination** | Checkpoints for LLM changes + Lint detection + rollback timeline (revert one checkpoint without undoing later manual edits) | `/coordinated/graphs/`, `/coordinated/clusters/`, `/coordinated/unified/` |
| **Refactoring** | EditCodeService, VoidModelService, MCP Service + custom tool handlers → SQLite L1 Atom Store | `/refactored/modules/` |
| **Packaging** | TypeScript + React + Tailwind (scope-tailwind → tsup) + Zod schemas (`F3CuratedSkillSchema`) | `/packages/sparc-*/` |
| **File Location** | Modular `src/vs/workbench/contrib/void/` | `/repo/architecture/`, `/repo/execution/`, `/repo/training/`, `/repo/infrastructure/` |
| **Repo Training** | Provider pipeline (`IChatThreadService` → `ConvertToLLMMessageService` → `sendLLMMessage`) + Checkpoints as ground-truth anchors | `/repo/training/data/precompiled/`, `/repo/training/models/`, `/repo/training/checkpoints/` |
| **UI (BENTO-007)** | React 19 + Tailwind + scope-tailwind | Skill Registry, Model Vendor Panel, Checkpoint Timeline (F0→F1→F2→F3), MCP Tool Registry, Repo Training Dashboard |

## Why Void

1. Open source (Apache 2.0) — fully owned once forked.
2. Local-first — zero middleman.
3. Type-safe TypeScript + React + Tailwind.
4. Modular, well-documented codebase.
5. Provenance-aware (checkpoints, diffs, rollback).

## Integration Notes

- **Agent Mode** → Ava007 Agentic Evaluator Loops (Challenger / Solver / Verifier).
- **Gather Mode** → safe inspection before promotion.
- MCP handlers validate skill packages and write into L1 Atom Store / QAG-MemBrain.
- Checkpoint timeline = F0 → F1 → F2 → F3 forging lifecycle visual.
- turbovec index (forged-ai-filing-os) is queryable from Void via MCP tools.
