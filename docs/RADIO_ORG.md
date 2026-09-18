# Radio organization (authoritative)

```text
Omnibus (Ava007-Omni-OS)     communication hub + ADB bridge
        │
        ├─► Agent-X
        │     skills/onomondo-ncs          firmware definition
        │     containers/cellular-edge     SoftSIM / nRF91 EXECUTION
        │     containers/rf-edge           LoRa / SX1262
        │     containers/sdr-edge          non-gNB SDR
        │     containers/hardware-io       USB serial
        │     containers/telecom-gateway   Telnyx
        │     containers/edge-tunnel       Cloudflare
        │
        └─► fapo-ran                       RAN / srsRAN / FAPO ONLY

QAG-MemBrain/skills/telecom                LEGACY extract only
```

Detail: `Agent-X/docs/RADIO_INVENTORY.md`
