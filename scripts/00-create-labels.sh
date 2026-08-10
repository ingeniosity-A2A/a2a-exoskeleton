#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-ingeniosity-A2A/Ava007}"

upsert_label() {
  local name="$1"
  local color="$2"
  local desc="$3"

  if gh label create "$name" --repo "$REPO" --color "$color" --description "$desc" 2>/dev/null; then
    echo "Created label: $name"
  else
    gh label edit "$name" --repo "$REPO" --color "$color" --description "$desc"
    echo "Updated label: $name"
  fi
}

# Canonical Matt Pocock triage labels
upsert_label "needs-triage" "D93F0B" "New issue, unclassified"
upsert_label "needs-info" "FBC6A1" "Blocked waiting for user or system input"
upsert_label "ready-for-agent" "0E8A16" "Fully specified, ready for AI or automated execution"
upsert_label "ready-for-human" "1D76DB" "Requires human intervention or review"
upsert_label "wontfix" "CCCCCC" "Invalid, duplicate, or out-of-scope issue"

# Ava007 / Exoskeleton domain labels
upsert_label "epic" "5319E7" "Large initiative"
upsert_label "architecture" "0052CC" "Structural design and system architecture"
upsert_label "substrate" "006B75" "Exoskeleton core substrate engine"
upsert_label "capability" "F9D0C4" "Composed capability implementation"
upsert_label "compute" "B60205" "CPU-native algorithmic compute layer"
upsert_label "transport" "164E63" "Zero-copy transport and edge membrane"
upsert_label "testing" "0E8A16" "Tests, validation, and smoke coverage"
upsert_label "benchmark" "FBC6A1" "Performance and scaling validation"
upsert_label "docs" "0075CA" "Documentation, ADRs, and domain context"
upsert_label "infra" "C5DEF5" "Repository scaffolding, packaging, and CI"

echo "Label bootstrap complete for $REPO"
