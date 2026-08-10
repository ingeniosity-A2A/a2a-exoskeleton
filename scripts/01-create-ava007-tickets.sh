#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-ingeniosity-A2A/Ava007}"
OUT="ava007-created-issues.txt"
: > "$OUT"

create_issue() {
  local title="$1"
  local labels="$2"
  local body="$3"

  local args=(issue create --repo "$REPO" --title "$title" --body "$body")

  IFS=',' read -ra label_arr <<< "$labels"
  for label in "${label_arr[@]}"; do
    label="$(echo "$label" | xargs)"
    args+=(--label "$label")
  done

  gh "${args[@]}" | tee -a "$OUT"
}

echo "Creating Ava007 / A2A Exoskeleton tickets..."

# -----------------------------------------------------------------------------
# Epic
# -----------------------------------------------------------------------------

EPIC_URL=$(create_issue \
  "Epic: A2A Exoskeleton Substrate" \
  "epic,architecture,ready-for-agent" \
  "$(cat <<'EOF'
This epic tracks implementation of the A2A Exoskeleton substrate for Ava007.

The Exoskeleton is an agentic substrate designed to remove dependence on heavy hardware matrix multiplication by shifting to software-native indexing, zero-copy memory transport, and O(1) context orchestration.

Core architectural principles:

- The LLM is an intent engine, not an execution dump.
- Structural execution is handled by the substrate.
- Capabilities are lazily materialized.
- Heavy work is offloaded from the main async loop.
- State is rehydrated through delta-only patches.
- Cancellations use orchestrated easeReverse unwind behavior.
- Context overhead must remain O(1), targeting approximately 53 tokens per turn.

Primary implementation areas:

- Core substrate contracts
- SubstrateEngine dispatcher
- Composed capabilities
- Marker extraction
- LTX-2.3 visual upscaling
- Algorithmic CPU-native compute interfaces
- Zero-copy transport interfaces
- Benchmark validation
- End-to-end demo
- Documentation and ADRs
EOF
)")

EPIC_NUMBER=$(basename "$EPIC_URL")
echo "Created epic: #$EPIC_NUMBER"
echo "$EPIC_URL" >> "$OUT"

# -----------------------------------------------------------------------------
# 1. Repository scaffold
# -----------------------------------------------------------------------------

create_issue \
  "Scaffold A2A Exoskeleton repository layout" \
  "infra,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Create the initial repository structure for the A2A Exoskeleton substrate.

Acceptance criteria:

- Repository contains the following packages:
  - exoskeleton/core
  - exoskeleton/capabilities
  - exoskeleton/compute
  - exoskeleton/transport
- Each package has an __init__.py file.
- pyproject.toml declares:
  - name: a2a-exoskeleton
  - version: 1.0.0
  - requires-python: >=3.10
  - dependencies for marker-pdf, pyarrow, tiktoken, torch, and diffusers
- README.md explains the Exoskeleton substrate at a high level.
- README.md links to docs/agents/domain.md when present.
- The package can be imported without executing heavy model loading.
EOF
)"

# -----------------------------------------------------------------------------
# 2. Core contracts
# -----------------------------------------------------------------------------

create_issue \
  "Implement core substrate contracts" \
  "substrate,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the core data contracts used by the Exoskeleton substrate.

Target file:

- exoskeleton/core/types.py

Acceptance criteria:

- Add ExecutionStatus enum with:
  - complete
  - failed
  - interrupted_salvaged
- Add Intent dataclass with:
  - description
  - file_path
  - upscale_figures
  - metadata
- Add CapabilityResult dataclass with:
  - status
  - output
  - model_used
  - token_overhead
- token_overhead should default to 53 to represent the O(1) context budget.
- Add DeltaState dataclass with:
  - session_id
  - delta_patch
  - turn_index
- Add unit tests validating instantiation and enum values.
EOF
)"

# -----------------------------------------------------------------------------
# 3. SubstrateEngine
# -----------------------------------------------------------------------------

create_issue \
  "Implement SubstrateEngine dispatcher" \
  "substrate,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the master timeline dispatcher for the Exoskeleton substrate.

Target file:

- exoskeleton/core/timeline.py

Acceptance criteria:

- Add SubstrateEngine class.
- Engine maintains a capability registry.
- Engine exposes a dispatch method accepting:
  - capability_name
  - intent
  - optional cancel_token
- dispatch increments a turn counter.
- dispatch raises ValueError when capability is not registered.
- dispatch forwards cancel_token to capability execution.
- Add create_delta_patch method returning a DeltaState.
- Delta patch includes:
  - status
  - markdown length
  - image count
  - turn index
- Add unit tests using a mock capability.
EOF
)"

# -----------------------------------------------------------------------------
# 4. Marker extraction
# -----------------------------------------------------------------------------

create_issue \
  "Implement MarkerExtractionCapability with lazy materialization" \
  "capability,compute,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the marker-pdf extraction primitive.

Target file:

- exoskeleton/capabilities/visual_doc.py

Acceptance criteria:

- Add MarkerExtractionCapability class.
- Heavy marker-pdf imports must not occur at module import time.
- Converter initialization must happen only through _ensure_loaded.
- run method must execute conversion through loop.run_in_executor.
- run method must return:
  - markdown
  - images
  - metadata
- Missing or unavailable marker dependencies should fail only when invoked.
- Add unit tests using mocked converter behavior.
EOF
)"

# -----------------------------------------------------------------------------
# 5. LTX upscale scaffold
# -----------------------------------------------------------------------------

create_issue \
  "Implement LTXUpscaleCapability lazy scaffold" \
  "capability,compute,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the LTX-2.3 spatial upscaling primitive scaffold.

Target file:

- exoskeleton/capabilities/visual_doc.py

Acceptance criteria:

- Add LTXUpscaleCapability class.
- Model loading must be lazy and deferred until execution.
- Class should expose MODEL_ID and device configuration.
- run method must execute through loop.run_in_executor.
- Initial implementation may return a placeholder upscaled image result.
- The capability must not import heavy diffusion dependencies at module import time.
- Add unit tests validating lazy loading and placeholder execution.
EOF
)"

# -----------------------------------------------------------------------------
# 6. Composed visual document capability
# -----------------------------------------------------------------------------

create_issue \
  "Implement ProcessVisualDocumentCapability forward execution path" \
  "capability,substrate,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the composed capability that combines document extraction and visual upscaling.

Target file:

- exoskeleton/capabilities/visual_doc.py

Acceptance criteria:

- Add ProcessVisualDocumentCapability class.
- Expose a single execute method accepting an Intent.
- Validate target file existence.
- Return failed CapabilityResult when file is missing.
- Execute Marker extraction first.
- Return failed CapabilityResult when extraction fails.
- When upscale_figures is true and images exist:
  - process images concurrently with asyncio.gather
  - tolerate individual upscaling exceptions
  - preserve extracted markdown even if some images fail
- Return complete CapabilityResult with:
  - markdown
  - images
  - upscaled_images
  - metadata
- model_used should be marker+ltx-2.3.
- Add unit tests for:
  - missing file
  - extraction failure
  - partial upscaling failure
  - successful completion
EOF
)"

# -----------------------------------------------------------------------------
# 7. easeReverse cancellation
# -----------------------------------------------------------------------------

create_issue \
  "Implement orchestrated easeReverse cancellation path" \
  "substrate,capability,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Implement the fast-exit cancellation behavior for composed capabilities.

Target file:

- exoskeleton/capabilities/visual_doc.py

Acceptance criteria:

- ProcessVisualDocumentCapability.execute accepts an optional cancel_token.
- If cancel_token is set after extraction:
  - return reverse_unwind result with stage extraction_phase
- If cancel_token is set after image processing gather:
  - return reverse_unwind result with stage upscale_phase
- If asyncio.CancelledError occurs:
  - return reverse_unwind result with stage gather_cancelled
- reverse_unwind must preserve salvaged markdown.
- reverse_unwind must clear or avoid returning heavy image buffers.
- Result status must be interrupted_salvaged.
- Output must include:
  - markdown
  - unwind_stage
  - notice
- Add unit tests covering each cancellation stage.
EOF
)"

# -----------------------------------------------------------------------------
# 8. Algorithmic compute interfaces
# -----------------------------------------------------------------------------

create_issue \
  "Add algorithmic CPU-native compute interfaces" \
  "compute,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Add interfaces for the no-GPU algorithmic intelligence stack.

Target file:

- exoskeleton/compute/algorithmic.py

Acceptance criteria:

- Add SLIDEEngine interface with train_sparse_step.
- SLIDEEngine should represent hash-table sparse updates rather than CUDA backpropagation.
- Add LiteParseEngine interface with parse_fast.
- LiteParseEngine should represent high-speed heuristic document parsing.
- Add SwiftShaderEngine or WARP rendering interface placeholder.
- Interfaces must not require GPU availability.
- Add unit tests returning deterministic placeholder results.
EOF
)"

# -----------------------------------------------------------------------------
# 9. Zero-copy transport
# -----------------------------------------------------------------------------

create_issue \
  "Add zero-copy transport interfaces" \
  "transport,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Add transport interfaces for zero-copy memory movement and edge streaming.

Target file:

- exoskeleton/transport/zero_copy.py

Acceptance criteria:

- Add ZeroCopyBufferStream interface.
- Include stream_to_edge method accepting buffer address and size.
- Add placeholder support for Arrow IPC style buffer contracts.
- Add placeholder support for sendfile style zero-copy transport where platform-appropriate.
- Implementation must not require actual network access in unit tests.
- Add unit tests using mocked buffer addresses and sizes.
EOF
)"

# -----------------------------------------------------------------------------
# 10. Benchmark harness
# -----------------------------------------------------------------------------

create_issue \
  "Build O(1) context benchmark harness" \
  "benchmark,testing,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Create a benchmark harness to validate Exoskeleton scaling characteristics.

Acceptance criteria:

- Add benchmark harness capable of registering N mock capabilities.
- Add support for executing T turns through SubstrateEngine.
- Measure or estimate:
  - token overhead per turn
  - total session tokens
  - wall-clock latency
- Validate that Exoskeleton mode targets approximately 53 tokens per turn.
- Produce a summary report in JSON or markdown.
- Benchmark must run without requiring GPU or network access.
- Include at least one test using N=100 and T=8.
EOF
)"

# -----------------------------------------------------------------------------
# 11. End-to-end demo
# -----------------------------------------------------------------------------

create_issue \
  "Add end-to-end demo and smoke tests" \
  "testing,substrate,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Add a runnable end-to-end demonstration of the Exoskeleton substrate.

Target file:

- main.py

Acceptance criteria:

- Demo creates a temporary sample document.
- Demo executes forward capability pipeline.
- Demo prints:
  - execution status
  - model pipeline
  - token overhead
  - delta patch
- Demo executes an easeReverse cancellation pass.
- Demo prints:
  - interrupted_salvaged status
  - unwind stage
  - salvage notice
- Temporary sample document is cleaned up after execution.
- Demo runs without requiring GPU or network access by default.
- Add pytest smoke test that imports main and validates basic execution.
EOF
)"

# -----------------------------------------------------------------------------
# 12. Documentation and ADRs
# -----------------------------------------------------------------------------

create_issue \
  "Add Exoskeleton domain docs and ADRs" \
  "docs,architecture,ready-for-agent" \
  "$(cat <<EOF
Parent epic: #$EPIC_NUMBER

Add repository documentation for the A2A Exoskeleton domain model.

Acceptance criteria:

- Add CONTEXT.md at repository root.
- CONTEXT.md defines:
  - Intellect layer
  - Substrate engine
  - Composed capability
  - Lazy materialization
  - DeltaState
  - easeReverse
- Add docs/adr directory.
- Add ADRs for:
  - LLM as intent engine
  - GSAP timeline substrate mapping
  - Lazy materialization
  - orchestrated easeReverse cancellation
  - zero-copy delta state transport
- Add docs/specs/a2a-exoskeleton-substrate.md containing the official architecture specification.
- Link docs/agents/domain.md to the new spec and ADRs.
EOF
)"

echo ""
echo "Ticket creation complete."
echo "Created issues written to: $OUT"
