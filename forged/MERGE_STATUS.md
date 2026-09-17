# Forged → Exoskeleton merge status

**Date:** 2026-09-17  
**Authority:** ingeniosity-A2A / Ava007

## Decision

1. **Forged filing merges into `a2a-exoskeleton`** (this repo).
2. **`Ava007-Omni-OS` is the A2A / edge branch of Exoskeleton** (Omnibus hub, Agent Browser, bridge).
3. Standalone `forged-ai-filing-os` remains the **content source** until checklist complete.

## What is operational in source (`forged-ai-filing-os`)

- Forged File Standard v1.2.0 (F0→F3)
- `forging/` pipeline, detector, vendor, capabilities, stores, manifest
- Explorer canvas + GSAP semantic triggers
- DEV-locked cognitive modules listed in package `__init__.py` until present

## What is operational on Omni-OS (A2A branch)

- Enhanced `ava007_bridge.py` (Mercury T1 / vLLM T0 / reflex)
- Omnibus docs + Agent Browser ownership policy
- Partial `Omnibus/forged_ai_filing_os/` scaffold (align with merged Forged)

## Next code drops into `forged/`

Priority order:

1. `forging/standard.py` + `docs/FORGED_FILE_STANDARD.md`
2. `forging/pipeline.py` + `stores.py` + `capabilities.py`
3. `main.py` CLI entry
4. Explorer / Bento binding under Omni Agent Browser
