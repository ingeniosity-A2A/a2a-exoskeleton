#!/usr/bin/env python3
"""
Ava007 Super Refactoring Intelligence System
============================================
Governed observe → measure → propose loop.

Does NOT:
  - redefine SubstrateEngine authority
  - auto-merge to main without gates
  - open Tier-C upgrades by default
  - invent a second brain / router

Does:
  - inventory repo + process health
  - score gaps against manifesto / Phase F baseline
  - emit structured RefactorProposal (TweenAtom-shaped)
  - optionally POST intent to Agent-X if reachable

Activation:
  PYTHONPATH=. python3 -m refactor.super_refactor
  PYTHONPATH=. python3 -m refactor.super_refactor --json
  PYTHONPATH=. python3 -m refactor.super_refactor --submit-agent-x

Source package: ava007-super-refactoring-1.zip
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
AGENT_X = os.environ.get("AGENT_X_URL", "http://127.0.0.1:8091").rstrip("/")
MEMBRAIN = os.environ.get("CORE_MEMBRAIN_URL", "http://127.0.0.1:8090").rstrip("/")
INTELLECT_API = os.environ.get("AVA007_INTELLIGENCE_API", "http://127.0.0.1:3000/api/intelligence").rstrip("/")
MAX_SOURCE_BYTES = 64_000

LOCKED = [
    "tier_c_dependency_inflation",
    "second_execution_authority",
    "model_as_ava_identity",
    "uncontrolled_self_modification",
]


@dataclass
class Finding:
    id: str
    severity: str
    area: str
    detail: str
    proposal: str


@dataclass
class RefactorReport:
    system: str = "ava007-super-refactor"
    version: str = "1.0.0"
    ts: float = field(default_factory=time.time)
    root: str = ""
    git_head: str = ""
    mode: str = "observe-measure-propose"
    services: Dict[str, Any] = field(default_factory=dict)
    inventory: Dict[str, Any] = field(default_factory=dict)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    tween_atom: Dict[str, Any] = field(default_factory=dict)
    next_actions: List[str] = field(default_factory=list)
    locked: List[str] = field(default_factory=lambda: list(LOCKED))


def _run(cmd: List[str], cwd: Optional[Path] = None) -> str:
    try:
        r = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip()
    except Exception as e:
        return f"ERR:{e}"


def _http_json(url: str, method: str = "GET", body: Optional[dict] = None) -> Optional[dict]:
    try:
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={"Content-Type": "application/json"} if body else {},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def observe() -> Dict[str, Any]:
    head = _run(["git", "rev-parse", "--short", "HEAD"])
    status = _run(["git", "status", "-sb"])
    paths = {
        "manifesto": (ROOT / "docs/MANIFESTO.md").exists(),
        "rev_ike": (ROOT / "engine/rev_ike.py").exists(),
        "super_refactor": (ROOT / "refactor/super_refactor.py").exists(),
    }
    return {"git_head": head, "git_status": status.splitlines()[:20], "paths": paths}


def probe_services() -> Dict[str, Any]:
    mb = _http_json(f"{MEMBRAIN}/health")
    ax = _http_json(f"{AGENT_X}/health")
    return {
        "core_membrain": {"url": MEMBRAIN, "up": mb is not None, "body": mb},
        "agent_x": {"url": AGENT_X, "up": ax is not None, "body": ax},
    }


def measure(inv: Dict[str, Any], svc: Dict[str, Any]) -> List[Finding]:
    f: List[Finding] = []
    paths = inv.get("paths") or {}
    if not paths.get("rev_ike"):
        f.append(Finding("rev_ike_missing", "gap", "engine", "engine/rev_ike.py missing", "Restore Rev.ike zero-copy pipeline"))
    else:
        f.append(Finding("rev_ike_present", "info", "engine", "Rev.ike present", "Keep zero-copy path authoritative"))
    if not svc.get("agent_x", {}).get("up"):
        f.append(Finding("agent_x_down", "gap", "runtime", "Agent-X not reachable", "Start Agent-X on :8091"))
    f.append(Finding("super_refactor_posture", "info", "intelligence",
                     "observe→measure→propose under manifesto", "No auto-merge; human accept required"))
    return f


def build_tween_atom(findings: List[Finding]) -> Dict[str, Any]:
    gaps = [x for x in findings if x.severity in ("gap", "block")]
    primary = gaps[0].id if gaps else "maintain_baseline"
    return {
        "AGENT": "AVA007", "MODE": "SYSTEM1", "INTENT": "SUPER_REFACTOR",
        "PRIMARY": primary, "GAPS": [g.id for g in gaps], "HEAL": "PROPOSE_ONLY",
        "AUTHORITY": "SubstrateEngine", "LOCKED": LOCKED, "HUMAN": "LOOP",
    }


def next_actions(findings: List[Finding], svc: Dict[str, Any]) -> List[str]:
    acts = []
    if not svc.get("agent_x", {}).get("up"):
        acts.append("Start Agent-X :8091")
    acts.append("Submit proposals only; require tests before merge")
    acts.append("Communicate via Agent-X POST /a2a/intent")
    return acts


def submit_agent_x(report: RefactorReport) -> Optional[dict]:
    _http_json(f"{AGENT_X}/a2a/register", "POST", {
        "agent_id": "super-refactor",
        "capabilities": ["refactor", "curation"],
        "version": "1.0.0",
    })
    intent = {
        "agent_id": "super-refactor",
        "intent": json.dumps({
            "type": "super_refactor_report",
            "tween_atom": report.tween_atom,
            "findings": [f["id"] for f in report.findings if f.get("severity") != "info"],
            "next": report.next_actions[:5],
        }),
        "version": "1.0.0",
    }
    return _http_json(f"{AGENT_X}/a2a/intent", "POST", intent)


def run(submit: bool = False, ingest_sources: bool = False) -> RefactorReport:
    inv = observe()
    svc = probe_services()
    findings = measure(inv, svc)
    report = RefactorReport(
        root=str(ROOT), git_head=inv.get("git_head") or "",
        services=svc, inventory=inv,
        findings=[asdict(x) for x in findings],
        tween_atom=build_tween_atom(findings),
        next_actions=next_actions(findings, svc),
    )
    if submit and svc.get("agent_x", {}).get("up"):
        report.services["submit"] = submit_agent_x(report)
    return report


def main() -> int:
    p = argparse.ArgumentParser(description="Ava007 Super Refactoring Intelligence")
    p.add_argument("--json", action="store_true")
    p.add_argument("--submit-agent-x", action="store_true")
    p.add_argument("--out", type=str, default="")
    args = p.parse_args()
    report = run(submit=args.submit_agent_x)
    payload = asdict(report)
    if args.out:
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("=== Ava007 Super Refactoring Intelligence ===")
        print(f"HEAD: {report.git_head}  mode: {report.mode}")
        for f in report.findings:
            print(f"  [{f['severity']}] {f['id']}: {f['detail']}")
        print(json.dumps(report.tween_atom, indent=2))
        print("ACTIVE: observe→measure→propose (HUMAN LOOP for accept)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
