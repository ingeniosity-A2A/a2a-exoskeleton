# Sources registry — a2a-exoskeleton

Canonical design assets live primarily under **Ava007-Omni-OS** `docs/sources/`.
This file indexes what the Exoskeleton *consumes* vs *must not own*.

| Source | Consumer role | Owning path |
|--------|---------------|-------------|
| The Exoskeleton Framework_ Substrate Architecture and Gateway Elimination.PDF | Boundary + GSAP substrate design | Omni-OS `docs/sources/exoskeleton/` (mirror notes here) |
| Crown Jewel / BTR / SuperRefactor materials | observe-measure-propose only | `refactor/` · `docs/skills/ava-super-refactor/` |
| Aetheris / Bento / Q² GSAP timeline PDFs | UI *contracts* only — engine in Omni | Omni-OS `docs/sources/browser/` |
| Rev.ike zero-copy | Filing substrate — not Exoskeleton | Forged-Filing-Sys + Omni streaming index |

## Rule

If a PDF describes **hardware, browser engine, CUDA, or edge OS**, register it under Omni-OS sources, not here.
If it describes **orchestration lifecycle / GSAP kernel / contracts**, index here and implement only the substrate side.

See also: [Ava007-Omni-OS docs/sources/README.md](https://github.com/ingeniosity-A2A/Ava007-Omni-OS/blob/main/docs/sources/README.md)
