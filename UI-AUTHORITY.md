# UI AUTHORITY — A2A Exoskeleton

Status: binding. Owner directive, 2026-09-07.

## The directive

**The Agent Browser controls all systems UI, and is located here — in the
A2A Exoskeleton.**

The Agent Browser is the single UI authority for every system in the
organization. It does not borrow authority from the surfaces it controls;
the surfaces consume authority from it, routed through this substrate.

## Where the authority physically lives

| Piece | Location |
|-------|----------|
| Authority routing contract | `exoskeleton/interface/ui_authority.py` (this repo, interface layer) |
| Verified registry mount | `exoskeleton/firmware/manifests/agent-browser.json` → mounted via `exoskeleton/firmware/registry.py` |
| Mount proof (hash check) | `scripts/mount_agent_browser.py` |
| Skill artifact (the controlled firmware) | `Agent-X:skills/agent-browser/SKILL.md` (Agent-X remains the capability/execution surface) |
| UI surfaces under its control | Agent-X `platform/` interface routes, ESA + Help Assembly consoles, Cybernetic-Ava007 display surfaces |

## Rules

1. **One authority.** No system, tenant, or console may self-authorize UI
   changes. UI work is done BY or THROUGH the Agent Browser (its surface,
   its Edit Mode tooling, its uploaded shell attachments applied verbatim).
2. **No verified hash → no authority.** The registry mount carries the
   sha256 of the deployed skill artifact and is verified at mount time.
   A mismatched artifact is refused — fail closed, no exceptions.
3. **The substrate routes; it does not host UI.** Bento/ESA/Help shells
   stay in their own repos (keep-out rule unchanged). What lives here is
   the contract, the registry entry, and the routing.
4. **Attachments are law.** Uploaded shell attachments (v6/UI8, BentoUi-v8)
   are applied verbatim and never redesigned. The Agent Browser implements
   them; it does not reinterpret them.
5. **Consumers table is closed.** Systems consuming UI authority are
   listed in `exoskeleton/interface/ui_authority.py::CONSUMERS`. New
   consumers require an explicit owner decision.

## Verify the mount

```bash
PYTHONPATH=. python3 scripts/mount_agent_browser.py \
  --artifact /path/to/Agent-X/skills/agent-browser/SKILL.md
```

Expected: `mounted: agent-browser`, `authority: ui`,
`routing: ui.authority.all-systems -> agent-browser`.
