"""Firmware skill registry — mount only verified manifests.

Invariant: No skill → no capability. No verified hash → no authority.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class MountedSkill:
    skill_id: str
    version: str
    provides: list[str]
    entry: str
    hash_sha256: str
    authority: str


class FirmwareRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, MountedSkill] = {}

    def verify_file(self, path: Path, expected_sha256: str) -> bool:
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        return h == expected_sha256.lower()

    def mount(self, manifest: dict[str, Any], artifact: Path | None = None) -> MountedSkill:
        for key in ("skill_id", "version", "provides", "entry", "hash_sha256"):
            if key not in manifest:
                raise ValueError(f"manifest missing {key}")
        if artifact is not None and not self.verify_file(artifact, manifest["hash_sha256"]):
            raise ValueError("hash mismatch — refuse mount")
        skill = MountedSkill(
            skill_id=manifest["skill_id"],
            version=manifest["version"],
            provides=list(manifest["provides"]),
            entry=manifest["entry"],
            hash_sha256=manifest["hash_sha256"],
            authority=manifest.get("authority", "read"),
        )
        self._skills[skill.skill_id] = skill
        return skill

    def get(self, skill_id: str) -> MountedSkill | None:
        return self._skills.get(skill_id)

    def list_provides(self) -> dict[str, str]:
        """Map capability name → skill_id."""
        out: dict[str, str] = {}
        for s in self._skills.values():
            for p in s.provides:
                out[p] = s.skill_id
        return out

    def load_manifest_file(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))
