# Exoskeleton Runtime — Canonical Boundary

Status: authoritative runtime boundary.

The Exoskeleton is the non-cognitive body surrounding Cybernetic-Ava007. It provides the substrate required to mount firmware, transport intent/observation references, schedule execution, access silicon, actuate Android without root, and degrade safely under hardware/resource failure.

## Owns

- temporal/timeline substrate and TweenAtom mechanics
- capability contracts and runtime dispatch
- firmware registry, verification, isolation, and loading
- Arrow/zero-copy transport and Duck substrate integration
- NPU/GPU/CPU dispatch and thermal/battery monitoring
- Android Accessibility/UiAutomation actuation
- security, signing, authority routing, and append-only audit
- degradation policy and circuit breakers
- versioned IPC/edge SDK contracts

## Does not own

- Ava007 reasoning or cognitive state
- RL training or policy intelligence
- Skills as intelligence authority
- Agent-X mesh/network identity
- service UI/application shells

## Boundary

```text
Cybernetic-Ava007
  Intent / Observation references
             │
             ▼
      A2A Exoskeleton
  runtime + transport + body
             │
             ▼
         Agent-X
  capability / mesh surface
```

## Failure policy

Runtime failures must degrade explicitly: NPU failure may fall back to CPU where supported; thermal pressure reduces work; memory pressure sheds nonessential buffers; firmware verification failure blocks execution; authority failures fail closed. No runtime failure manufactures or persists cognitive reasoning state.

## Honest performance language

mmap mapping cost and full model cold-start cost are separate measurements. Cold model activation must be benchmarked including page faults/warmup. Arrow/JSON claims must come from reproducible benchmarks. No fabricated speedup figures are architectural guarantees.

## Security language

Android Keystore/hardware-backed signing is the baseline. TEEGRIS/OP-TEE and ML-KEM/ML-DSA integration requires a dedicated device/vendor engineering workstream and must not be represented as already available merely because an abstraction exists.
