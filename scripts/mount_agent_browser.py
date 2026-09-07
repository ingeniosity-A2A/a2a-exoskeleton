#!/usr/bin/env python3
"""Mount the Agent Browser firmware into the registry — with hash proof.

Owner directive (2026-09-07): the Agent Browser controls all systems UI
and is located in this repo (A2A Exoskeleton). The registry mount below is
the machine-checkable form of that directive:

    No skill → no capability. No verified hash → no authority.

Usage:
    python3 scripts/mount_agent_browser.py --artifact /path/to/skills/agent-browser/SKILL.md

The default artifact path assumes the three official repos are checked out
side by side (../Agent-X/skills/agent-browser/SKILL.md).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exoskeleton.firmware import FirmwareRegistry

MANIFEST = Path(__file__).resolve().parent.parent / "exoskeleton" / "firmware" / "manifests" / "agent-browser.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "Agent-X" / "skills" / "agent-browser" / "SKILL.md",
        help="path to the deployed agent-browser SKILL.md artifact",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = FirmwareRegistry()

    if not args.artifact.exists():
        print(f"artifact not found: {args.artifact}")
        print("pass --artifact /path/to/skills/agent-browser/SKILL.md")
        return 2

    mounted = registry.mount(manifest, artifact=args.artifact)
    print(f"mounted   : {mounted.skill_id} v{mounted.version}")
    print(f"authority : {mounted.authority}")
    print(f"provides  : {', '.join(mounted.provides)}")
    print(f"hash      : sha256 verified against {args.artifact}")

    router = registry.list_provides()
    assert router.get("ui.authority.all-systems") == "agent-browser"
    print("routing   : ui.authority.all-systems -> agent-browser (sole UI authority, all systems)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
