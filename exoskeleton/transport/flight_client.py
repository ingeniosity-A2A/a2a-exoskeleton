"""Arrow Flight client stub — zero-copy oriented pulls from substrate."""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)

try:
    import pyarrow as pa
    import pyarrow.flight as flight
except ImportError:  # pragma: no cover
    pa = None  # type: ignore
    flight = None  # type: ignore


class SubstrateFlightClient:
    def __init__(self, location: str = "grpc://127.0.0.1:8815") -> None:
        if flight is None:
            raise RuntimeError("pyarrow not installed")
        self.location = location
        self._client = flight.FlightClient(location)

    def get_table(self, ticket: bytes) -> Any:
        reader = self._client.do_get(flight.Ticket(ticket))
        return reader.read_all()

    def health(self) -> bool:
        try:
            self._client.list_flights()
            return True
        except Exception as exc:  # noqa: BLE001
            log.warning("Flight health failed: %s", exc)
            return False
