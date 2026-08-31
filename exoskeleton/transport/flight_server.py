"""Arrow Flight RPC server stub — substrate highway (faster than JSON for bulk).

Requires: pyarrow

  pip install 'pyarrow>=14'

Honest note: this is a structural stub. Bench with real RecordBatches before
claiming throughput numbers.
"""
from __future__ import annotations

import logging
from typing import Iterator

log = logging.getLogger(__name__)

try:
    import pyarrow as pa
    import pyarrow.flight as flight
except ImportError:  # pragma: no cover
    pa = None  # type: ignore
    flight = None  # type: ignore


class SubstrateFlightServer:
    """Minimal Flight server wrapper."""

    def __init__(self, location: str = "grpc://0.0.0.0:8815") -> None:
        if flight is None:
            raise RuntimeError("pyarrow not installed")
        self.location = location
        self._server: flight.FlightServerBase | None = None

    def serve_blocking(self) -> None:
        class _Srv(flight.FlightServerBase):
            def do_get(self, context, ticket):  # type: ignore[no-untyped-def]
                # Placeholder empty table — replace with registry / timeline batches
                table = pa.table({"event_id": pa.array([], type=pa.string())})
                return flight.RecordBatchStream(table)

        self._server = _Srv(self.location)
        log.info("Flight server listening on %s", self.location)
        self._server.serve()


def descriptor_for_capability(capability: str) -> bytes:
    return capability.encode("utf-8")
