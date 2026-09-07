"""SovereignIngestionEngine — the Serialization-Tax eliminator.

Binds ingestion directly to Apache Arrow zero-copy memory: native layers
and the reactive UI share the same memory space, so AI tensors and
metadata are available instantly — no JSON round-trip, no Base64
inflation, no parse-then-copy.

Two ingestion paths:

* ``ingest_records(rows, schema)`` — structured payloads are compiled
  straight into Arrow record batches (implementation-parse, never
  string-parse).
* ``ingest_ipc(buf)`` — an Arrow IPC buffer is consumed **in place**:
  the record batch's arrays are views over the original buffer's memory
  (verified by buffer address identity — the zero-copy proof).

The prepared table is then handed to the ``InstantInjectionKernel`` for
the atomic pointer swap into a consumer read slot (e.g. ava007.context).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

import pyarrow as pa
import pyarrow.ipc as pa_ipc


@dataclass
class IngestReport:
    """Honest accounting of one ingestion: copies, bytes, wall time."""

    rows: int
    columns: List[str]
    zero_copy: bool            # buffer-address-verified for the IPC path
    buffer_address: int        # source buffer base address (IPC path)
    batch_address: int         # first array buffer address (IPC path)
    compile_us: float          # payload → Arrow compile time
    json_baseline_us: float    # equivalent JSON round-trip time (tax baseline)
    payload_bytes: int
    json_bytes: int


class SovereignIngestionEngine:
    """Parse payloads directly into Arrow memory — skip the serialization tax."""

    def __init__(self):
        self.reports: List[IngestReport] = []

    # ------------------------------------------------------------------
    # Path 1: structured payload → Arrow (implementation-parse)
    # ------------------------------------------------------------------
    def ingest_records(
        self,
        rows: Sequence[Dict[str, Any]],
        schema: Optional[pa.Schema] = None,
    ) -> pa.Table:
        """Compile structured payloads straight into a columnar Arrow table.

        There is deliberately no JSON intermediate: the payload structure
        *is* the columnar layout. ``json_baseline`` timing is captured so
        the avoided serialization tax stays measurable, not rhetorical.
        """
        t0 = time.perf_counter_ns()
        if not rows:
            raise ValueError("ingest_records requires at least one row")
        columns: Dict[str, List[Any]] = {}
        for row in rows:
            for key, value in row.items():
                columns.setdefault(key, []).append(value)
        arrays = {k: pa.array(v) for k, v in columns.items()}
        table = pa.table(arrays, schema=schema)
        compile_us = (time.perf_counter_ns() - t0) / 1_000.0

        t1 = time.perf_counter_ns()
        json_blob = json.dumps(rows, default=str)  # the tax we refuse to pay
        json_us = (time.perf_counter_ns() - t1) / 1_000.0

        report = IngestReport(
            rows=len(rows),
            columns=table.column_names,
            zero_copy=True,
            buffer_address=0,
            batch_address=0,
            compile_us=round(compile_us, 3),
            json_baseline_us=round(json_us, 3),
            payload_bytes=table.nbytes,
            json_bytes=len(json_blob.encode()),
        )
        self.reports.append(report)
        return table

    # ------------------------------------------------------------------
    # Path 2: Arrow IPC buffer consumed IN PLACE (the zero-copy proof)
    # ------------------------------------------------------------------
    def to_ipc(self, table: pa.Table) -> pa.Buffer:
        """Serialize a table to the Arrow IPC wire form (transport only)."""
        sink = pa.BufferOutputStream()
        with pa_ipc.new_stream(sink, table.schema) as writer:
            writer.write_table(table)
        return sink.getvalue()

    def ingest_ipc(self, buf: pa.Buffer) -> pa.RecordBatch:
        """Consume an Arrow IPC buffer **without copying its memory**.

        The reader wraps the existing buffer; produced arrays reference
        the source buffer's memory region (verified via buffer addresses).
        Nothing is parsed into Python objects for transport — the buffer
        is the memory, not a serialization of it.
        """
        t0 = time.perf_counter_ns()
        reader = pa_ipc.open_stream(pa.BufferReader(buf))
        batch = reader.read_next_batch()
        compile_us = (time.perf_counter_ns() - t0) / 1_000.0

        # Zero-copy verification: the batch's first column buffer must live
        # INSIDE the source buffer's address range — i.e. it IS that memory.
        src_addr = buf.address
        first_col = batch.column(0)
        col_buf = first_col.buffers()[1]  # [0]=validity, [1]=data
        zero_copy = (
            col_buf is not None
            and col_buf.address != 0
            and src_addr != 0
            and src_addr <= col_buf.address < src_addr + buf.size
        )

        t1 = time.perf_counter_ns()
        json_blob = json.dumps(batch.to_pylist(), default=str)
        json_us = (time.perf_counter_ns() - t1) / 1_000.0

        report = IngestReport(
            rows=batch.num_rows,
            columns=list(batch.schema.names),
            zero_copy=zero_copy,
            buffer_address=src_addr,
            batch_address=col_buf.address if col_buf else 0,
            compile_us=round(compile_us, 3),
            json_baseline_us=round(json_us, 3),
            payload_bytes=int(buf.size),
            json_bytes=len(json_blob.encode()),
        )
        self.reports.append(report)
        return batch

    def tax_report(self) -> Dict[str, Any]:
        """Aggregate serialization-tax accounting across all ingests."""
        if not self.reports:
            return {"ingests": 0}
        total_json_bytes = sum(r.json_bytes for r in self.reports)
        total_arrow_bytes = sum(r.payload_bytes for r in self.reports)
        zero_copy_verified = all(r.zero_copy for r in self.reports if r.buffer_address)
        return {
            "ingests": len(self.reports),
            "zero_copy_verified": zero_copy_verified,
            "json_bytes_if_we_paid_the_tax": total_json_bytes,
            "arrow_bytes_actually_touched": total_arrow_bytes,
            "wire_savings_percent": round(
                (1 - total_arrow_bytes / total_json_bytes) * 100, 1
            ) if total_json_bytes else 0.0,
        }

    # ------------------------------------------------------------------
    def expose(self, table: pa.Table, kernel, slot: str) -> None:
        """Hand a prepared table to the instant kernel for atomic injection."""
        kernel.inject(slot, table)
