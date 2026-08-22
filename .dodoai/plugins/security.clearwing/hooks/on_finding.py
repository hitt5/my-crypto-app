"""Clearwing finding event hook placeholder.

Phase 1 records local Finding/Evidence artifact candidates. Phase 2/3 can wire
this hook to TaskGraph generation and Cockpit attention notifications.
"""

from __future__ import annotations

from typing import Any


async def handle(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "handled": False,
        "reason": "phase1_noop",
        "event": event,
    }
