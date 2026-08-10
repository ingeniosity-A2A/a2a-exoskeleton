"""Zero-copy memory transport over Arrow IPC and sendfile.

Streams intelligence across edge nodes at wire speed with
zero CPU tax. Bypasses user-space memory entirely.

- ZeroCopyBufferStream: Page cache access for raw byte streaming
- EdgeNodeClient: Client for edge deployment targets (Workers, Termux, SoftSIM)
"""

from exoskeleton.transport.zero_copy import ZeroCopyBufferStream, EdgeNodeClient

__all__ = [
    "ZeroCopyBufferStream",
    "EdgeNodeClient",
]
