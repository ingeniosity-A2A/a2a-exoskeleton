# Intelligence IR from Astra Curator

**Source client:** `Cybernetic-Ava007/curation/astra/astra_curator.py`  
**Gateway:** Vercel AI Gateway → GPT-6 Astra (free-tier credits)  
**This limb:** Forged-Filing-Sys records artifacts; does not call Astra.

## Flow

```text
Astra Curator (dry schema / intelligence_ir kind)
        ↓ structured output
Intelligence IR contract
        ↓
Forged F0 → F1 → F2 → F3
```

Minimal IR fields expected from `--kind intelligence_ir`:

- artifact_id, source, semantic_findings
- refactoring_plan, capability_delta, confidence
- dependencies, validation

Promote only after curation validation in Cybernetic-Ava007 — never auto-write Astra output into F3 without a human or policy gate.
