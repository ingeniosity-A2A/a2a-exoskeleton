# Headless Cursor as System-1 muscle

Design reports describe spawning a headless AST agent (Cursor / Cline / Void Agent Mode) from an RLM-style planner.

## Boundary

| Role | Owner |
|------|--------|
| Plan intent, `spawn` *decision* | Cybernetic-Ava007 |
| `allocate` / `observe` / `reverse` lifecycle | **This repo** (Exoskeleton) |
| Run worker process, worktree, diff stream | **Ava007-Omni-OS** + Agent-X (`ast.worker`) |
| Persist F2 skill / unlock governance | Forged-Filing-Sys |
| GSAP lock-slide presentation | Omni UI surface |

Exoskeleton does **not** embed Cursor, host IPython harness state, or own DuckDB/RocksDB.

## Capability contract (sketch)

```yaml
id: ast.worker
allocate:
  isolation: git-worktree
  timeout_sec: 600
observe:
  progress: odometer   # UI hint only
release:
  on_failure: lifo_checkpoint_discard  # RAC
```

Full synthesis (with corrections to "Rune = Core OS"):  
https://github.com/ingeniosity-A2A/Ava007-Omni-OS/blob/main/docs/PRIME_AGENT_EXOSKELETON_SYNTHESIS.md
