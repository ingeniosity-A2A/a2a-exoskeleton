# a2a-exoskeleton organization map

**Role:** Layer-2 runtime substrate only (non-cognitive) — one of three official repos.

```text
a2a-exoskeleton/
├─ exoskeleton/
│   ├─ core/           # timeline, types
│   ├─ db/             # dual-tier Duck
│   ├─ transport/      # zero-copy / Arrow path
│   ├─ compute/        # algorithmic helpers
│   └─ capabilities/   # capability *contracts* (not Agent-X skills)
├─ wiki/               # architecture docs (GSAP orchestration notes, Duck, …)
├─ main.py · pyproject.toml
├─ scripts/            # ops (prefer no monorepo Ava tickets)
└─ OFFICIAL-THREE-REPO.md · ORGANIZATION.md
```

## Organization status

| Area | Status |
|------|--------|
| Role vs Cybernetic-Ava007 / Agent-X | **Locked** |
| Substrate packages present | **Organized** |
| Rust zip dump removed | **Done** |
| Wiki architecture docs | **Present** |
| Arrow Flight production path | **Fill next** |
| Firmware registry + hash mount | **Fill next** |
| DegradationPolicy / honest mmap benches | **Fill next** |
| SemVer interface package for other two repos | **Fill next** |

## Done enough to move forward

Structure and ownership match Agent-X organization standard. Remaining work is **substrate fill**, not re-org.

**Never here:** Ava persona/intellect, Bento/ESA consoles, skill packages (Agent-X), manifesto quiz.

Rotational: specialized exoskeletons (ESA, Help) attach via contracts; this repo is the shared substrate.
