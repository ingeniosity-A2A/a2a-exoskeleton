"""UI authority contract — the Agent Browser controls all systems UI.

Owner directive (2026-09-07): the Agent Browser is the single UI authority
for every system in the organization, and that authority is homed HERE, in
the A2A Exoskeleton substrate (interface layer + firmware registry).

What this means operationally:

- Every UI surface — Agent-X consoles (platform, ESA, Help Assembly),
  Cybernetic-Ava007 surfaces, any future tenant — consumes UI authority.
  None of them may self-authorize UI changes.
- UI changes are made BY or THROUGH the Agent Browser (its surface, its
  edit-mode tooling, its uploaded shell attachments applied verbatim).
- The substrate routes authority; it does not host UI. Bento/ESA/Help
  shells stay in their own repos (keep-out rule unchanged). What lives
  here is the routing contract and the verified registry mount.
- "No verified hash → no authority" holds: the registry mount for the
  Agent Browser firmware carries the sha256 of its deployed skill
  artifact and is verified at mount time (see
  scripts/mount_agent_browser.py).
"""
from __future__ import annotations

from dataclasses import dataclass

UI_AUTHORITY_VERSION = "1.0.0"

#: skill_id of the sole UI authority (must match the firmware registry mount)
UI_AUTHORITY_SKILL = "agent-browser"


@dataclass
class UIAuthorityGrant:
    """One system's grant to consume UI authority (routing record only)."""

    system: str            # e.g. "Agent-X", "Cybernetic-Ava007", "esa-exoskeleton"
    surface: str           # e.g. "platform/ agent-browser interface routes"
    granted_by: str        # owner directive reference
    can_redesign: bool     # False everywhere except the Agent Browser itself


#: Systems that CONSUME UI authority. None of these may redesign framework
#: chrome; tenants additionally may not restyle the shell or other tenants.
#: NOTE: ESA and Help Assembly are SERVICES inside the Agent-X repo — they
#: are surfaces under Agent-X's grant, not systems of their own.
CONSUMERS: tuple[UIAuthorityGrant, ...] = (
    UIAuthorityGrant("Agent-X", "platform/ interface routes + ESA + Help Assembly services", "owner directive 2026-09-07", True),
    UIAuthorityGrant("Cybernetic-Ava007", "intellect display surfaces", "owner directive 2026-09-07", False),
)


def ui_authority_router() -> dict[str, str]:
    """Map system → where its UI authority comes from (routing table)."""
    return {grant.system: f"a2a-exoskeleton:{UI_AUTHORITY_SKILL}" for grant in CONSUMERS}
