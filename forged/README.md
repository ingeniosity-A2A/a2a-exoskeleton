# Forged-Filing-Sys

**Canonical Exoskeleton limb** for filing, artifact lifecycle (F0→F3), manifests, stores, and explorer contracts.

**Product name:** Forged-Filing-Sys (formerly Forged-AI-Filing-OS).  
**Historical source repo:** `ingeniosity-A2A/forged-ai-filing-os` (no new feature development there).

## Owns

- Forged File Standard
- Identify → normalize → version → validate → store → manifest → index → expose → retrieve
- RocksDB Skills control plane / DuckDB Intelligence stores (as filing surfaces)
- Explorer / BENTO binding contracts

## Does NOT own

- Cognitive authority (Cybernetic-Ava007)
- Refactoring Intelligence engine (Ava007 ingestion)
- Skill *firmware* definitions (Ava007 `skills/`)
- Edge Omnibus second implementation (Omni-OS is integration pointer only)

## Pipeline

```text
Cybernetic-Ava007  →  Intelligence IR (stream / Arrow)
        ↓
  Forged-Filing-Sys contract (F0→F3)
        ↓
  a2a-exoskeleton runtime
        ↓
  Agent-X / sandbox
```

See root `CONSOLIDATION.md` and historical repo `RENAME.md`.
