"""Utility hooks that run before Chainlit launches.

Ensures a usable port is picked when the default 8000 is busy. Python automatically
loads `sitecustomize` on startup, so we opportunistically set `CHAINLIT_PORT`
for Chainlit CLI invocations that didn't explicitly ask for a port.
"""

from __future__ import annotations

import os
import socket
import sys
from contextlib import closing

# Default behaviour can be disabled by exporting CHAINLIT_AUTO_PORT=0.
_AUTO_PORT_ENABLED = os.environ.get("CHAINLIT_AUTO_PORT", "1").lower() in {"1", "true", "yes"}


def _should_configure_port() -> bool:
    """Return True when the current process is a Chainlit CLI invocation."""

    if not _AUTO_PORT_ENABLED:
        return False

    if "CHAINLIT_PORT" in os.environ:
        return False

    argv = [str(arg).lower() for arg in sys.argv if isinstance(arg, str)]
    if not argv:
        return False

    # Handles `chainlit ...` entrypoint scripts on Windows & POSIX.
    if "chainlit" in os.path.basename(argv[0]):
        return True

    # Handles `python -m chainlit run ...` style invocations.
    if len(argv) > 1 and "chainlit" in argv[1]:
        return True

    # Fallback: look at the entire command for "chainlit" references.
    return any("chainlit" in arg for arg in argv[1:])


def _find_available_port(start: int, attempts: int) -> int | None:
    """Return an available port starting from `start`, or None if none were found."""

    for offset in range(attempts):
        candidate = start + offset
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", candidate))
            except OSError:
                continue
            return candidate
    return None


def _select_port() -> int:
    base = int(os.environ.get("CHAINLIT_BASE_PORT", "8000"))
    search_span = max(int(os.environ.get("CHAINLIT_PORT_SEARCH_SPAN", "50")), 1)

    port = _find_available_port(base, search_span)
    if port is not None:
        return port

    # As a last resort, ask the OS for an ephemeral port.
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


if _should_configure_port():
    chosen = _select_port()
    os.environ["CHAINLIT_PORT"] = str(chosen)
    # Uvicorn also checks PORT in some deployment scenarios; set it if absent.
    os.environ.setdefault("PORT", str(chosen))
    # Helpful hint in the console so users know which port to open.
    print(f"[chainlit auto-port] Using available port {chosen}", flush=True)
