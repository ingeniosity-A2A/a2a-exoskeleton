#!/usr/bin/env python3
"""
REV.IKE ZERO-COPY STREAMING ENGINE (Exoskeleton Core)
=====================================================
Sequential generator pipeline for edge execution (S26 Ultra / mobile CPU).
Keeps RSS flat and streams into L0–L3 + refs_offload.

Source: attachment rev-ike-zero-copy-engine.py + benchmark report (50k records).
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
import tracemalloc
from typing import Any, Generator, Optional

try:
    import psutil
except ImportError:  # optional on minimal hosts
    psutil = None  # type: ignore


class RevIkeZeroCopyPipeline:
    def __init__(self, output_dir: str = "/workspace/scratch/exoskeleton_vault"):
        self.output_dir = output_dir
        self.l0_dir = os.path.join(output_dir, "L0_Trace")
        self.l1_dir = os.path.join(output_dir, "L1_Atoms")
        self.l2_dir = os.path.join(output_dir, "L2_Scenarios")
        self.l3_dir = os.path.join(output_dir, "L3_Persona")
        self.refs_dir = os.path.join(output_dir, "refs_offload")

        self._ensure_directories()
        self.db_path = os.path.join(self.output_dir, "local_memory.db")
        self._init_sqlite_schema()

    def _ensure_directories(self) -> None:
        for path in [self.l0_dir, self.l1_dir, self.l2_dir, self.l3_dir, self.refs_dir]:
            os.makedirs(path, exist_ok=True)

    def _init_sqlite_schema(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_records (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                content TEXT NOT NULL,
                memory_type TEXT DEFAULT 'episodic',
                importance REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_agent_type ON memory_records(agent_id, memory_type)"
        )
        conn.commit()
        conn.close()

    def generate_simulated_stream(
        self, total_records: int = 50000
    ) -> Generator[dict[str, Any], None, None]:
        for i in range(total_records):
            yield {
                "record_id": f"atom-uuid-{i:06d}",
                "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
                "agent_id": "builder-agent-s26u",
                "timestamp": time.time(),
                "content": (
                    f"CodePen 2.0 block build execution #{i}: "
                    "Compiled SCSS module and validated AST tree."
                ),
                "payload_ref": f"refs/offload_log_{i // 1000}.md",
                "memory_tier": "L1_Atom",
                "forged_stage": "F2_Governed",
            }

    def execute_zero_copy_ingestion(
        self, total_records: int = 50000
    ) -> dict[str, Any]:
        process = psutil.Process(os.getpid()) if psutil else None
        tracemalloc.start()

        start_time = time.time()
        initial_rss = (
            process.memory_info().rss / (1024 * 1024) if process else 0.0
        )

        l0_file = open(
            os.path.join(self.l0_dir, "raw_session_trace.log"), "w", encoding="utf-8"
        )
        l1_file = open(
            os.path.join(self.l1_dir, "episodic_fact_atoms.jsonl"),
            "w",
            encoding="utf-8",
        )
        ref_file = open(
            os.path.join(self.refs_dir, "context_offload_archive.md"),
            "w",
            encoding="utf-8",
        )

        records_processed = 0
        peak_rss = initial_rss

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        conn.execute("BEGIN TRANSACTION")

        for record in self.generate_simulated_stream(total_records):
            records_processed += 1
            l0_file.write(
                f"[{record['timestamp']}] TRACE {record['record_id']} - {record['content']}\n"
            )
            l1_file.write(json.dumps(record) + "\n")
            ref_file.write(
                f"## Node {record['record_id']}\nContent: {record['content']}\n\n"
            )
            cursor.execute(
                "INSERT INTO memory_records (id, tenant_id, agent_id, content, memory_type) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    record["record_id"],
                    record["tenant_id"],
                    record["agent_id"],
                    record["content"],
                    "L1_Atom",
                ),
            )
            if records_processed % 5000 == 0:
                conn.commit()
                conn.execute("BEGIN TRANSACTION")
                if process:
                    current_rss = process.memory_info().rss / (1024 * 1024)
                    if current_rss > peak_rss:
                        peak_rss = current_rss

        conn.commit()
        conn.close()
        l0_file.close()
        l1_file.close()
        ref_file.close()

        elapsed_time = time.time() - start_time
        final_rss = process.memory_info().rss / (1024 * 1024) if process else 0.0
        rss_delta = max(0.00, final_rss - initial_rss)
        _current_heap, peak_heap = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        throughput = records_processed / elapsed_time if elapsed_time > 0 else 0

        return {
            "total_records": records_processed,
            "elapsed_seconds": round(elapsed_time, 3),
            "throughput_rec_sec": round(throughput, 2),
            "initial_rss_mb": round(initial_rss, 2),
            "peak_rss_mb": round(peak_rss, 2),
            "final_rss_mb": round(final_rss, 2),
            "rss_delta_mb": round(rss_delta, 2),
            "peak_python_heap_mb": round(peak_heap / (1024 * 1024), 3),
            "l0_file_size_mb": round(
                os.path.getsize(os.path.join(self.l0_dir, "raw_session_trace.log"))
                / (1024 * 1024),
                2,
            ),
            "l1_file_size_mb": round(
                os.path.getsize(
                    os.path.join(self.l1_dir, "episodic_fact_atoms.jsonl")
                )
                / (1024 * 1024),
                2,
            ),
            "refs_file_size_mb": round(
                os.path.getsize(
                    os.path.join(self.refs_dir, "context_offload_archive.md")
                )
                / (1024 * 1024),
                2,
            ),
        }


if __name__ == "__main__":
    pipeline = RevIkeZeroCopyPipeline()
    report = pipeline.execute_zero_copy_ingestion(10000)
    print(json.dumps(report, indent=2))
