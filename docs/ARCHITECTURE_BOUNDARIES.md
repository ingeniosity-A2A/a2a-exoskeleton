# Architecture boundaries — a2a-exoskeleton

## Stack

```text
Cybernetic-Ava007     INTELLECT
        │ Intent
        ▼
a2a-exoskeleton       GSAP orchestration substrate   ← here
        │ capability.request
        ▼
Ava007-Omni-OS        environments · devices · compute · browser
        │
   Agent-X / S26 / RevPi / Oracle / fapo-ran (as registered)
```

## GSAP verbs only

```text
discover → select → allocate → execute → observe → interrupt → reverse → release
```

Providers (CUDA, Termux, Soapy, Agent Browser, containers) are **registered under Omni-OS**. Exoskeleton selects them by contract, it does not implement them.

## Hard keep-out

| Do not absorb into this repo | Home |
|------------------------------|------|
| Model weights / cognition loop | Cybernetic-Ava007 |
| Omnibus A2A hub implementation | Ava007-Omni-OS |
| Agent Browser engine | Ava007-Omni-OS `capabilities/browser` |
| CUDA worker images / GPU cloud adapters | Ava007-Omni-OS `capabilities/compute` |
| DragonOS / termux-usb / SDR drivers | Ava007-Omni-OS |
| Filing / zero-copy vault authority | Forged-Filing-Sys |
| srsRAN / FAPO | fapo-ran |

## CUDA placement

```text
Exoskeleton: "need GPU capability X"
     →
Omni-OS compute registry:
  local CUDA | Oracle GPU | Colab/HF ephemeral | …
```

Never place CUDA/PyTorch worker stacks inside this repository as the system of record.
