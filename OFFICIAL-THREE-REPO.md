# Official three-repo architecture

**a2a-exoskeleton** = Layer-2 substrate only (non-cognitive).

| Repo | Role |
|------|------|
| Cybernetic-Ava007 | Intellect |
| **a2a-exoskeleton** | Runtime substrate |
| Agent-X | Capabilities + consoles (Bento UI upgrade) |

Archive: **QAG-MemBrain**

## KEEP

- `exoskeleton/core/` (timeline, types)
- `exoskeleton/db/` (dual-tier Duck)
- `exoskeleton/transport/` (zero-copy)
- `exoskeleton/capabilities/` (contracts)
- `wiki/` architecture docs
- `pyproject.toml`, `main.py`

## REMOVE → QAG

- Binary dumps / rust zips (removed)
- Ticket scripts that assume old Ava007 monorepo identity
- Any cognitive / persona code

## MISSING (fill)

- [ ] Arrow Flight server/client + honest benches
- [ ] Firmware skill registry + hash verify + mount
- [ ] DegradationPolicy (thermal / memory / NPU)
- [ ] mmap hot-swap docs (honest timings)
- [ ] SemVer interface package for Cybernetic + Agent-X
- [ ] Port useful Ava007 `exoskeleton/` modules without UI
