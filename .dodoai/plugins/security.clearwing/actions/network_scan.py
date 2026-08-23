"""clearwing.scan — Phase 2 network scan placeholder."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from dodo_core.module.plugin_sdk import action_spec


class NetworkScanInput(BaseModel):
    target: str
    ports: str = "22,80,443,8080,8443"
    scan_type: list[Literal["service", "vuln", "os"]] = Field(default_factory=lambda: ["service", "vuln"])
    timeout: int = 300
    workspace_root: str = "."
    allow_network_scan: bool = False


class NetworkScanOutput(BaseModel):
    ok: bool
    error: str
    message: str
    target: str
    markdown: str


@action_spec(
    key="clearwing.scan",
    version="1.0.0",
    summary="Clearwing network security scan",
    description="Phase 2 placeholder. Network scans require per-run human approval before implementation is enabled.",
    tags=["security", "clearwing", "network-scan"],
    source="plugin",
    idempotent=False,
    risk_level="high",
)
async def clearwing_scan(input_data: NetworkScanInput) -> NetworkScanOutput:
    message = "clearwing.scan is reserved for Phase 2 and is blocked until a human approval gate is implemented."
    return NetworkScanOutput(
        ok=False,
        error="phase2_not_enabled",
        message=message,
        target=input_data.target,
        markdown=f"# Clearwing Network Scan\n\nStatus: blocked\n\n{message}",
    )


entry = clearwing_scan.entry
