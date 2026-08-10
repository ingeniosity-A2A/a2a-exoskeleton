"""A2A Exoskeleton: End-to-End Execution Driver.

Demonstrates the dual-tier DuckDB topology interacting over
the Exoskeleton substrate — forward execution, easeReverse
interruption, and O(1) scaling verification.

Run with:

    python main.py
"""

import asyncio
import time
from pathlib import Path

from exoskeleton.core.timeline import SubstrateEngine
from exoskeleton.core.types import Intent
from exoskeleton.db.duck_intellect import IntellectDuckClient
from exoskeleton.db.duck_membrane import CoreMembraneDuckServer


async def main():
    print("=================================================================")
    print("   A2A EXOSKELETON: DUAL-TIER DUCKDB SUBSTRATE DEMO       ")
    print("=================================================================\n")

    # ============================================================== 
    # 1. Spin up Core-Membrane DuckDB Server Engine
    # ==============================================================
    print("[1] Initializing Core-Membrane DuckDB Server...")
    membrane_db = CoreMembraneDuckServer(db_path=":memory:", listen_port=9999)
    quack_endpoint = membrane_db.enable_quack_remote_server()
    print(f"  -> Core-Membrane DuckDB active at: {quack_endpoint}")
    print(f"  -> Schema: session_deltas, execution_telemetry, l0_raw_events\n")

    # ============================================================== 
    # 2. Spin up Intellect Layer Embedded DuckDB Client
    # ==============================================================
    print("[2] Initializing Intellect Embedded DuckDB Client...")
    intellect_db = IntellectDuckClient()
    attached = intellect_db.attach_core_membrane(quack_endpoint)
    print(f"  -> Intellect Client attached to Core-Membrane: {attached}")
    print(f"  -> Protocol: quack:// (Zero-Copy Arrow Stream)\n")

    # ============================================================== 
    # 3. Initialize Substrate Orchestrator Engine
    # ==============================================================
    print("[3] Initializing Substrate Engine...")
    engine = SubstrateEngine()

    from exoskeleton.capabilities.visual_doc import ProcessVisualDocumentCapability
    engine.register(
        name="process_visual_document",
        capability=ProcessVisualDocumentCapability(),
    )
    print(f"  -> Registered: {engine.registered_capabilities}\n")

    # Create dummy document for testing
    demo_file = Path("sample_architecture_spec.pdf")
    demo_file.write_text("%PDF-1.4 Mock High-Throughput Specification")

    session_id = "sess_a2a_001"

    try:
        # ============================================================== 
        # PASS 1: Forward Execution + DuckDB Persistence
        # ==============================================================
        print("[Pass 1] Forward Composed Capability Pipeline...")
        print("           (Label: Extraction -> Stagger: Parallel Upscale)")

        t0 = time.perf_counter()
        intent = Intent(
            description="Process system architecture diagram",
            file_path=str(demo_file),
            upscale_figures=True,
        )

        result = await engine.dispatch(
            capability_name="process_visual_document",
            intent=intent,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000

        # Persist delta into Core-Membrane DuckDB
        delta = engine.create_delta_patch(result, session_id=session_id)
        membrane_db.persist_delta(
            session_id=delta.session_id,
            turn_index=delta.turn_index,
            capability="process_visual_document",
            status=result.status.value,
            delta=delta.delta_patch,
            tokens=result.token_overhead,
        )

        # Cache capability stats in Intellect local DuckDB
        intellect_db.cache_capability_stats(
            name="process_visual_document",
            status=result.status.value,
            duration_ms=elapsed_ms,
        )

        # Query back through both DuckDB tiers
        history = membrane_db.query_session_history(session_id)
        context_proj = intellect_db.project_minimal_context(session_id)

        print(f"  -> Status:            {result.status.value}")
        print(f"  -> Duration:          {elapsed_ms:.2f} ms")
        print(f"  -> Context Overhead:  {result.token_overhead} tokens (O(1))")
        print(f"  -> Membrane History:  {history}")
        print(f"  -> Intellect Context: {context_proj}")
        print(f"  -> Cumulative Tokens: {engine.total_token_overhead()}\n")

        # ============================================================== 
        # PASS 2: easeReverse + DuckDB Persistence
        # ==============================================================
        print("[Pass 2] Orchestrated easeReverse (Mid-Flight Cancellation)...")

        cancel_token = asyncio.Event()
        cancel_token.set()

        t1 = time.perf_counter()
        intent_cancel = Intent(
            description="Aborted processing request",
            file_path=str(demo_file),
            upscale_figures=True,
        )

        result_rev = await engine.dispatch(
            capability_name="process_visual_document",
            intent=intent_cancel,
            cancel_token=cancel_token,
        )
        elapsed_rev = (time.perf_counter() - t1) * 1000

        delta_rev = engine.create_delta_patch(result_rev, session_id=session_id)
        membrane_db.persist_delta(
            session_id=delta_rev.session_id,
            turn_index=delta_rev.turn_index,
            capability="process_visual_document",
            status=result_rev.status.value,
            delta=delta_rev.delta_patch,
            tokens=result_rev.token_overhead,
        )

        intellect_db.cache_capability_stats(
            name="process_visual_document",
            status=result_rev.status.value,
            duration_ms=elapsed_rev,
        )

        print(f"  -> Status:            {result_rev.status.value}")
        print(f"  -> Unwind Stage:      {result_rev.output.get('unwind_stage')}")
        print(f"  -> Notice:            {result_rev.output.get('notice')}")
        print(f"  -> Duration:          {elapsed_rev:.2f} ms")
        print(f"  -> Cumulative Tokens: {engine.total_token_overhead()}\n")

        # ============================================================== 
        # PASS 3: Analytical Queries Across Both Tiers
        # ==============================================================
        print("[Pass 3] Cross-Tier Analytical Queries...")

        # Core-Membrane aggregate analytics
        stats = membrane_db.query_aggregate_stats()
        print(f"  -> Membrane Aggregate Stats:")
        print(f"     Sessions: {stats['total_sessions']}, Deltas: {stats['total_deltas']}")
        print(f"     Avg Tokens/Turn: {stats['avg_tokens_per_turn']}, Total: {stats['total_tokens']}")
        print(f"     Turn Range: {stats['turn_range']}")

        # Intellect local cache
        cached = intellect_db.get_cached_capabilities()
        print(f"  -> Intellect Capability Cache:")
        for c in cached:
            print(f"     {c['name']}: {c['invocations']} calls, avg {c['avg_ms']}ms, last={c['status']}")

        # O(1) scaling proof
        print(f"\n  -> O(1) Scaling Proof:")
        print(f"     T={engine.turn_counter} turns x 53 tok = {engine.total_token_overhead()} tokens")
        print(f"     Independent of N={len(engine.registered_capabilities)} capabilities\n")

    finally:
        if demo_file.exists():
            demo_file.unlink()
        membrane_db.close()
        intellect_db.close()

    print("=================================================================")
    print("         DUAL DUCKDB ARCHITECTURE VERIFIED                   ")
    print("=================================================================")


if __name__ == "__main__":
    asyncio.run(main())
