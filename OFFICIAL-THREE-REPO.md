# Official three-repo architecture

**a2a-exoskeleton** = Layer-2 substrate only (non-cognitive). Arrow / Duck / timeline / firmware mount.

| Repo | Role |
|------|------|
| Cybernetic-Ava007 | Intellect |
| **a2a-exoskeleton** | Runtime substrate |
| Agent-X | Capabilities + consoles |

Archive: **QAG-MemBrain**

## KEEP

- `exoskeleton/core/` (timeline, types)
- `exoskeleton/db/` (dual-tier Duck)
- `exoskeleton/transport/` (zero-copy)
- `exoskeleton/capabilities/base.py` (capability contract)
- `wiki/` architecture + dual-tier Duck + GSAP orchestration docs
- `pyproject.toml`, `main.py` entry when substrate-only

## REMOVE → QAG-MemBrain (`archive/from-a2a-exoskeleton/`)

| Path | Why |
|------|-----|
| `ava007-agent-exoskeleton-rust.zip` | Binary dump — archive, not source of truth |
| Ticket scripts that assume monorepo Ava007 identity | Process debt |
| Any cognitive / BTR / persona code if added | Intellect repo only |

## MISSING (fill from Ava007 `exoskeleton/` + Core-Membrain)

- [ ] Full core modules from Ava007 exoskeleton (agent_registry, membrane, security, signal, reflex) **without** dragging intellect UI
- [ ] Arrow Flight server/client (honest benches, no invented 809× claims)
- [ ] Firmware skill registry + hash verify + mount path
- [ ] DegradationPolicy (thermal / memory / NPU fallback)
- [ ] mmap hot-swap with honest ~20ms cold / ~1μs hot docs
- [ ] README stating three-repo boundary + rotational exo attachment
- [ ] Interface package consumed by Cybernetic + Agent-X (SemVer)
