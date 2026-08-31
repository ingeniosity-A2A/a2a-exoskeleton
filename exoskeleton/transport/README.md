# transport — Arrow Flight highway

JSON remains fine for small control messages. **Bulk tensors / inventory / timeline batches** prefer Flight.

| Module | Role |
|--------|------|
| `flight_server.py` | grpc Flight server stub (`:8815`) |
| `flight_client.py` | Client pull |

```bash
pip install 'pyarrow>=14'
python -c "from exoskeleton.transport.flight_client import SubstrateFlightClient"
```

Do not invent 809× speedups without benches under `benches/`.
