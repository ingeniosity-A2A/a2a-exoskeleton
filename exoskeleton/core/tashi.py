"""Tashi DAG substrate primitive.

Tashi tracks lineage, ordering, tips, roots, and gossip of InteractionQuantum
objects. It does not inspect or interpret cognitive state. Intent meaning is
an Ava007 concern and must not become a DAG query primitive.
"""

import os
import time
from typing import Optional, Callable

from .quantum import InteractionQuantum


class TashiVertex:
    def __init__(self, quantum: InteractionQuantum):
        self.quantum = quantum
        self.quantum_id = quantum.quantum_id
        self.parents = list(quantum.parent_quanta)
        self.children: list[str] = []
        self.depth = 0
        self.arrival_time = time.time()
        self.gossip_count = 0

    def to_dict(self) -> dict:
        return {
            "quantum_id": self.quantum_id,
            "parents": self.parents,
            "children": self.children,
            "depth": self.depth,
            "arrival_time": self.arrival_time,
            "gossip_count": self.gossip_count,
        }


class TashiDAG:
    """Leaderless lineage DAG for substrate-owned InteractionQuanta."""

    def __init__(self, storage_path: Optional[str] = None):
        self.vertices: dict[str, TashiVertex] = {}
        self.tips: set[str] = set()
        self.roots: set[str] = set()
        self.storage_path = storage_path
        self._on_add_callbacks: list[Callable] = []
        if storage_path and os.path.exists(storage_path):
            self._load()

    def add(self, quantum: InteractionQuantum) -> bool:
        qid = quantum.quantum_id
        if qid in self.vertices:
            return False
        vertex = TashiVertex(quantum)
        if not quantum.parent_quanta:
            self.roots.add(qid)
            vertex.depth = 0
        else:
            max_depth = -1
            for parent_id in quantum.parent_quanta:
                if parent_id in self.vertices:
                    parent = self.vertices[parent_id]
                    parent.children.append(qid)
                    self.tips.discard(parent_id)
                    max_depth = max(max_depth, parent.depth)
            vertex.depth = max_depth + 1
        self.vertices[qid] = vertex
        self.tips.add(qid)
        for callback in self._on_add_callbacks:
            try:
                callback(quantum, vertex)
            except Exception:
                pass
        if self.storage_path:
            self._save()
        return True

    def get(self, quantum_id: str) -> Optional[InteractionQuantum]:
        vertex = self.vertices.get(quantum_id)
        return vertex.quantum if vertex else None

    def get_vertex(self, quantum_id: str) -> Optional[TashiVertex]:
        return self.vertices.get(quantum_id)

    def get_lineage(self, quantum_id: str, max_depth: int = 100) -> list[InteractionQuantum]:
        visited: set[str] = set()
        lineage: list[InteractionQuantum] = []

        def walk(qid: str, depth: int):
            if qid in visited or depth > max_depth or qid not in self.vertices:
                return
            visited.add(qid)
            vertex = self.vertices[qid]
            for parent_id in vertex.parents:
                walk(parent_id, depth + 1)
            lineage.append(vertex.quantum)

        walk(quantum_id, 0)
        return lineage

    def get_children(self, quantum_id: str) -> list[InteractionQuantum]:
        vertex = self.vertices.get(quantum_id)
        if not vertex:
            return []
        return [self.vertices[cid].quantum for cid in vertex.children if cid in self.vertices]

    def get_tips(self) -> list[InteractionQuantum]:
        return [self.vertices[qid].quantum for qid in self.tips if qid in self.vertices]

    def get_roots(self) -> list[InteractionQuantum]:
        return [self.vertices[qid].quantum for qid in self.roots if qid in self.vertices]

    def depth(self) -> int:
        return max((v.depth for v in self.vertices.values()), default=0)

    def size(self) -> int:
        return len(self.vertices)

    def on_add(self, callback: Callable):
        self._on_add_callbacks.append(callback)

    def gossip_export(self, since_timestamp: float = 0) -> list[dict]:
        exported = []
        for vertex in self.vertices.values():
            if vertex.arrival_time > since_timestamp:
                exported.append(vertex.quantum.to_dict())
                vertex.gossip_count += 1
        return exported

    def gossip_import(self, quanta_data: list[dict]) -> int:
        added = 0
        for data in quanta_data:
            if self.add(InteractionQuantum.from_dict(data)):
                added += 1
        return added

    def merge(self, other: "TashiDAG") -> int:
        added = 0
        for vertex in other.vertices.values():
            if self.add(vertex.quantum):
                added += 1
        return added

    def query_by_source(self, source_did: str) -> list[InteractionQuantum]:
        return [v.quantum for v in self.vertices.values() if v.quantum.source_did == source_did]

    def query_by_timerange(self, start: str, end: str) -> list[InteractionQuantum]:
        return [v.quantum for v in self.vertices.values() if start <= v.quantum.timestamp <= end]

    def _save(self):
        if not self.storage_path:
            return
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path, "w") as handle:
            for vertex in self.vertices.values():
                handle.write(vertex.quantum.to_jsonl() + "\n")

    def _load(self):
        if not self.storage_path or not os.path.exists(self.storage_path):
            return
        with open(self.storage_path) as handle:
            for line in handle:
                if line.strip():
                    try:
                        self.add(InteractionQuantum.from_jsonl(line))
                    except Exception:
                        continue

    def stats(self) -> dict:
        sources: dict[str, int] = {}
        for vertex in self.vertices.values():
            sources[vertex.quantum.source_did] = sources.get(vertex.quantum.source_did, 0) + 1
        return {
            "vertices": len(self.vertices),
            "tips": len(self.tips),
            "roots": len(self.roots),
            "depth": self.depth(),
            "sources": sources,
        }

    def __repr__(self) -> str:
        return f"TashiDAG(vertices={len(self.vertices)}, tips={len(self.tips)}, depth={self.depth()})"
