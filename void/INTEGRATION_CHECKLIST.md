# Void Integration Checklist — Ava007 Curation Workstation

Void upstream is **deprecated/archived**. We treat it as a **reference fork base**, not a live dependency.

## Phase 1 — Reference Lock (done)

- [x] SPARC layer mapping documented
- [x] Hierarchy position fixed under a2a-exoskeleton
- [x] No-middleman / local-first rule recorded
- [x] Links to forged-ai-filing-os + fapo-ran + QAG-MemBrain

## Phase 2 — Fork Skeleton (next engineering work)

- [ ] Clone `voideditor/void` at last known good tag/commit
- [ ] Strip or freeze unused VS Code surfaces
- [ ] Keep: Agent Mode, Gather Mode, Checkpoints, MCP, provider pipeline, React 19 UI
- [ ] Rename product strings → Ava007 Curation Workstation / Omnibus
- [ ] Point default providers at OpenRouter + Hugging Face + local Ollama
- [ ] Wire MCP tools to:
  - turbovec search (forged-ai-filing-os)
  - L1 Atom Store / QAG-MemBrain deposit
  - CapabilityRegistry (`fapo-ran` / a2a-exoskeleton)

## Phase 3 — SPARC Binding

- [ ] Intake: register models with `repo_id` / revision / commit into `/intake/`
- [ ] Separation: Agent/Gather → emit YAML primitives under `/separated/primitives/`
- [ ] Coordination: checkpoint timeline drives F0→F3 promotion UI
- [ ] Refactoring: MCP handlers write `/refactored/modules/`
- [ ] Packaging: Zod `F3CuratedSkillSchema` + tsup pipeline → `/packages/sparc-*/`
- [ ] BENTO-007: glassmorphic panels (Skill Registry, Model Vendor, Checkpoint Timeline)

## Phase 4 — Hard Boundaries

- [ ] Void never becomes a second Intellect (Cybernetic-Ava007 only)
- [ ] Void never owns memory authority (QAG-MemBrain only)
- [ ] Void never owns radio/RAN (fapo-ran only)
- [ ] Void is the *curation shell*; execution stays in a2a-exoskeleton / Agent-X

## License

- Void additions: Apache 2.0
- VS Code base: MIT
- Ava007 adaptations: follow existing ingeniosity-A2A licensing
