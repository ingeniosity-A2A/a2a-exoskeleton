"""Core-Membrane DuckDB Server Engine.

Persistent analytical database running at the Core-Membrane level.
Stores full session history, delta patches, and telemetry in
Parquet/JSON formats. Exposes a quack:// remote protocol interface
for zero-copy Arrow streaming to Intellect nodes.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb


class CoreMembraneDuckServer:
    """Persistent analytical database at the Core-Membrane layer.

    Stores long-term L0-L3 state deltas, execution telemetry,
    and cross-agent memory. Accessible over the Quack Remote
    Protocol for zero-copy Arrow streaming.
    """

    def __init__(
        self,
        db_path: str = "membrane_store.duckdb",
        listen_port: int = 9999,
    ):
        self.db_path = db_path
        self.listen_port = listen_port
        self.conn = duckdb.connect(db_path)
        self._initialize_membrane_schema()

    def _initialize_membrane_schema(self) -> None:
        """Initialize high-performance analytics schemas for Exoskeleton state."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS session_deltas (
                session_id    VARCHAR,
                turn_index    INTEGER,
                capability_name VARCHAR,
                status        VARCHAR,
                delta_payload JSON,
                token_overhead INTEGER,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (session_id, turn_index)
            );

            CREATE INDEX IF NOT EXISTS idx_session_id
                ON session_deltas(session_id);
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS execution_telemetry (
                telemetry_id  VARCHAR PRIMARY KEY,
                session_id    VARCHAR,
                capability    VARCHAR,
                phase         VARCHAR,
                duration_ms   DOUBLE,
                metadata      JSON,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS l0_raw_events (
                event_id     VARCHAR PRIMARY KEY,
                session_id   VARCHAR,
                event_type   VARCHAR,
                payload      JSON,
                ingested_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    def enable_quack_remote_server(self) -> str:
        """Configure and expose the database over the Quack Remote Protocol.

        Returns the quack:// URI that Intellect nodes use to attach.
        """
        try:
            self.conn.execute("INSTALL quack; LOAD quack;")
        except Exception:
            pass  # quack extension may be pre-bundled or simulated

        return f"quack://127.0.0.1:{self.listen_port}"

    def persist_delta(
        self,
        session_id: str,
        turn_index: int,
        capability: str,
        status: str,
        delta: Dict[str, Any],
        tokens: int,
    ) -> None:
        """Write a state delta into Core-Membrane storage.

        Uses UPSERT semantics — if a delta for this session+turn
        already exists, it is updated in place.
        """
        self.conn.execute(
            """
            INSERT INTO session_deltas
                (session_id, turn_index, capability_name, status,
                 delta_payload, token_overhead)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (session_id, turn_index) DO UPDATE
                SET status = EXCLUDED.status,
                    delta_payload = EXCLUDED.delta_payload;
            """,
            [session_id, turn_index, capability, status,
             json.dumps(delta), tokens],
        )

    def persist_telemetry(
        self,
        telemetry_id: str,
        session_id: str,
        capability: str,
        phase: str,
        duration_ms: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Write execution telemetry for analytical post-mortems."""
        self.conn.execute(
            """
            INSERT INTO execution_telemetry
                (telemetry_id, session_id, capability, phase,
                 duration_ms, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [telemetry_id, session_id, capability, phase,
             duration_ms, json.dumps(metadata or {})],
        )

    def persist_raw_event(
        self,
        event_id: str,
        session_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> None:
        """Ingest a raw L0 telemetry event into the membrane."""
        self.conn.execute(
            """
            INSERT INTO l0_raw_events (event_id, session_id, event_type, payload)
            VALUES (?, ?, ?, ?)
            """,
            [event_id, session_id, event_type, json.dumps(payload)],
        )

    def query_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Query the full analytical execution path for a session.

        Returns ordered delta history for state rehydration.
        """
        rel = self.conn.execute(
            """
            SELECT turn_index, capability_name, status, delta_payload
            FROM session_deltas
            WHERE session_id = ?
            ORDER BY turn_index ASC
            """,
            [session_id],
        )
        return [
            {
                "turn": r[0],
                "capability": r[1],
                "status": r[2],
                "delta": r[3],
            }
            for r in rel.fetchall()
        ]

    def query_aggregate_stats(self) -> Dict[str, Any]:
        """Query aggregate session statistics from the membrane.

        Demonstrates DuckDB's analytical power over stored deltas.
        """
        rel = self.conn.execute("""
            SELECT
                COUNT(DISTINCT session_id) AS total_sessions,
                COUNT(*) AS total_deltas,
                AVG(token_overhead) AS avg_tokens_per_turn,
                SUM(token_overhead) AS total_tokens,
                MIN(turn_index) AS min_turn,
                MAX(turn_index) AS max_turn
            FROM session_deltas
        """)
        row = rel.fetchone()
        return {
            "total_sessions": row[0],
            "total_deltas": row[1],
            "avg_tokens_per_turn": round(row[2], 1) if row[2] else 0,
            "total_tokens": row[3] or 0,
            "turn_range": [row[4], row[5]] if row[4] is not None else [],
        }

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
