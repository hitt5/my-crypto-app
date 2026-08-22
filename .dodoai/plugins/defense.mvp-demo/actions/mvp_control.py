"""Defense MVP demo control actions.

The implementation deliberately keeps the MVP runtime in the
`dodoai-defense` repository and exposes it to dodo Core through the
project Plugin / Action Registry boundary.
"""

from __future__ import annotations

import os
import signal
import socket
import subprocess
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from dodo_core.module.router.domain.decorators import action_spec


DEFAULT_DEFENSE_REPO = os.environ.get("DODOAI_DEFENSE_REPO", str(Path.home() / "dodoai-defense"))


class DefenseMvpContext(BaseModel):
    workspace_id: str = Field(default="local")
    org_id: str = Field(default="local")
    user_id: str = Field(default="local")
    role: Literal["owner", "admin", "member", "viewer"] = "owner"
    deploy_tier: Literal["desktop", "server", "edge", "mission"] = "desktop"
    mission_id: str = Field(default="RECON-ALPHA")


class DefenseMvpStatusInput(DefenseMvpContext):
    defense_repo: str = Field(default=DEFAULT_DEFENSE_REPO)


class DefenseMvpControlInput(DefenseMvpContext):
    action: Literal["start", "stop", "status"] = "status"
    mode: Literal["server", "full", "ui", "standalone"] = "server"
    defense_repo: str = Field(default=DEFAULT_DEFENSE_REPO)
    install: bool = Field(
        default=False,
        description="Run launch-mvp.sh --install before starting the demo.",
    )
    px4: bool = Field(
        default=False,
        description="Only used by mode=standalone; runs mvp_demo.py --px4.",
    )


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


def _runtime_dir(repo: Path) -> Path:
    path = repo / ".dodoai" / "runtime" / "defense-mvp"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _pid_file(repo: Path) -> Path:
    return _runtime_dir(repo) / "demo.pid"


def _log_file(repo: Path) -> Path:
    return _runtime_dir(repo) / "demo.log"


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


def _status(input_data: DefenseMvpStatusInput) -> DefenseMvpStatusOutput:
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


def _launch_command(input_data: DefenseMvpControlInput, repo: Path) -> list[str]:
    if input_data.mode == "standalone":
        command = ["python3", "mvp_demo.py"]
        if input_data.px4:
            command.append("--px4")
        return command

    script = repo / "scripts" / "launch-mvp.sh"
    if not script.exists():
        raise ValueError(f"launch script not found: {script}")

    if input_data.install:
        subprocess.run(["bash", str(script), "--install"], cwd=repo, check=True)

    if input_data.mode == "full":
        return ["bash", str(script), "--full"]
    if input_data.mode == "ui":
        return ["bash", str(script), "--ui"]
    return ["bash", str(script)]


@action_spec(
    key="defense.mvp.control",
    version="1.0.0",
    summary="Start, stop, or inspect the Defense MVP demo",
    description=(
        "Controls the existing dodoai-defense MVP demo through a project "
        "plugin boundary. This action launches scripts/launch-mvp.sh or "
        "mvp_demo.py without copying defense code into Core."
    ),
    tags=["defense", "mvp", "demo", "control", "tenant-scoped"],
    source="plugin",
    idempotent=False,
    timeout_seconds=60.0,
    risk_level="high",
)
async def defense_mvp_control(input_data: DefenseMvpControlInput) -> DefenseMvpStatusOutput:
    repo = _repo(input_data.defense_repo)

    if input_data.action == "status":
        return _status(DefenseMvpStatusInput(**input_data.model_dump()))

    if input_data.action == "stop":
        pid = _read_pid(repo)
        if _pid_alive(pid):
            try:
                os.killpg(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        _pid_file(repo).unlink(missing_ok=True)
        return _status(DefenseMvpStatusInput(**input_data.model_dump())).model_copy(
            update={"message": "Defense MVP stop requested."}
        )

    command = _launch_command(input_data, repo)
    log_path = _log_file(repo)
    log_handle = log_path.open("ab")
    process = subprocess.Popen(
        command,
        cwd=repo,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    _pid_file(repo).write_text(str(process.pid), encoding="utf-8")

    result = _status(DefenseMvpStatusInput(**input_data.model_dump()))
    return result.model_copy(
        update={
            "status": "partial" if result.status == "stopped" else result.status,
            "message": (
                f"Defense MVP launch requested (mode={input_data.mode}, "
                f"pid={process.pid}, log={log_path})."
            ),
            "pid": process.pid,
        }
    )


entry = defense_mvp_control.entry
