"""Defense MVP demo status action."""

from __future__ import annotations

import os
import socket
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from dodo_core.module.router.domain.decorators import action_spec


DEFAULT_DEFENSE_REPO = os.environ.get("DODOAI_DEFENSE_REPO", str(Path.home() / "dodoai-defense"))


class DefenseMvpStatusInput(BaseModel):
    workspace_id: str = Field(default="local")
    org_id: str = Field(default="local")
    user_id: str = Field(default="local")
    role: Literal["owner", "admin", "member", "viewer"] = "owner"
    deploy_tier: Literal["desktop", "server", "edge", "mission"] = "desktop"
    mission_id: str = Field(default="RECON-ALPHA")
    defense_repo: str = Field(default=DEFAULT_DEFENSE_REPO)


class DefenseMvpStatusOutput(BaseModel):
    success: bool
    status: Literal["running", "stopped", "partial", "error"]
    message: str
    workspace_id: str
    mission_id: str
    defense_repo: str
    server_port_open: bool = False
    ui_port_open: bool = False
    pid: int | None = None
    urls: dict[str, str] = Field(default_factory=dict)
    commands: dict[str, str] = Field(default_factory=dict)


def _repo(path: str) -> Path:
    repo = Path(path).expanduser().resolve()
    if not repo.exists():
        raise ValueError(f"defense_repo not found: {repo}")
    return repo


def _pid_file(repo: Path) -> Path:
    return repo / ".dodoai" / "runtime" / "defense-mvp" / "demo.pid"


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _read_pid(repo: Path) -> int | None:
    try:
        raw = _pid_file(repo).read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except (FileNotFoundError, ValueError):
        return None


def _pid_alive(pid: int | None) -> bool:
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


@action_spec(
    key="defense.mvp.status",
    version="1.0.0",
    summary="Get Defense MVP demo runtime status",
    description=(
        "Checks the dodoai-defense MVP demo server/UI ports and reports "
        "the tenant-scoped launch commands."
    ),
    tags=["defense", "mvp", "demo", "status"],
    source="plugin",
    idempotent=True,
    timeout_seconds=10.0,
    risk_level="low",
)
async def defense_mvp_status(input_data: DefenseMvpStatusInput) -> DefenseMvpStatusOutput:
    repo = _repo(input_data.defense_repo)
    server_open = _port_open(8000)
    ui_open = _port_open(3000)
    pid = _read_pid(repo)
    pid_running = _pid_alive(pid)

    if server_open:
        status: Literal["running", "stopped", "partial", "error"] = "running"
        message = "Defense MVP server is reachable and serves the Command Center UI."
    elif ui_open or pid_running:
        status = "partial"
        message = "Defense MVP appears partially running."
    else:
        status = "stopped"
        message = "Defense MVP is not running."

    return DefenseMvpStatusOutput(
        success=True,
        status=status,
        message=message,
        workspace_id=input_data.workspace_id,
        mission_id=input_data.mission_id,
        defense_repo=str(repo),
        server_port_open=server_open,
        ui_port_open=ui_open,
        pid=pid if pid_running else None,
        urls={
            "api": "http://localhost:8000",
            "api_docs": "http://localhost:8000/docs",
            "websocket": "ws://localhost:8000/ws",
            "command_center": "http://localhost:8000",
            "command_center_dev": "http://localhost:3000",
        },
        commands={
            "start_server": "defense.mvp.control action=start mode=server",
            "start_full": "defense.mvp.control action=start mode=full",
            "stop": "defense.mvp.control action=stop",
            "state": "curl localhost:8000/api/state",
            "gps_spoof": (
                "curl -X POST localhost:8000/api/threat/inject "
                "-H 'Content-Type: application/json' "
                "-d '{\"threat_type\":\"gps_spoofing\",\"drone_id\":\"drone-003\"}'"
            ),
        },
    )


entry = defense_mvp_status.entry
