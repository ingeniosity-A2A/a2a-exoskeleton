# Forged limb of a2a-exoskeleton

**Status:** Merge in progress (2026-09-17)

Forged-AI-Filing-OS is the intelligence / filing layer of the **Exoskeleton substrate**.
It is **not** a second top-level OS.

## Source of truth (until full tree copy is complete)

| Item | Location |
|------|----------|
| Full package + forging pipeline | https://github.com/ingeniosity-A2A/forged-ai-filing-os |
| Canonical contract | `forged-ai-filing-os/docs/FORGED_FILE_STANDARD.md` (v1.2.0) |
| Package version | `2.8.0-exoskeleton-substrate` |
| This limb | `a2a-exoskeleton/forged/` (merge landing zone) |

## Hierarchy

```text
a2a-exoskeleton
  ├── main / exoskeleton/     ← runtime substrate
  ├── forged/                 ← THIS DIR — Forged filing merged here
  ├── void/                   ← curation workstation
  └── Ava007-Omni-OS (A2A)    ← edge / Omnibus / Agent Browser branch
```

## Install

Until the full package is vendored under this tree:

```bash
# Preferred long-term: single install from a2a-exoskeleton once merge completes
pip install -e .

# Interim: install forged package from sibling repo
pip install -e ../forged-ai-filing-os
python -m forged_ai_filing_os.main init
python -m forged_ai_filing_os.main validate
```

## Merge checklist

- [x] Hierarchy docs on a2a-exoskeleton + Omni-OS
- [x] `forged/` landing zone on Exoskeleton main
- [ ] Copy `forged_ai_filing_os/forging/*` into this tree
- [ ] Copy `docs/FORGED_FILE_STANDARD.md` + config YAML
- [ ] Wire `exoskeleton/capabilities` ↔ Forged Capability = Tools + Harness
- [ ] Point Omni Omnibus Agent Browser at Forged explorer contract
- [ ] Archive or thin-pointer standalone `forged-ai-filing-os` after verify

See root [CONSOLIDATION.md](../CONSOLIDATION.md).
