"""clearwing.sourcehunt — run Clearwing source-code vulnerability hunting."""

from __future__ import annotations

import asyncio
import importlib.util
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from dodo_core.module.plugin_sdk import action_spec


def _load_ingester():
    module_path = Path(__file__).resolve().parents[1] / "ingestion" / "finding_ingester.py"
    spec = importlib.util.spec_from_file_location("security_clearwing_ingester", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Clearwing ingester: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourcehuntInput(BaseModel):
    repo_url: str | None = None
    local_path: str | None = None
    depth: Literal["quick", "standard", "deep"] = "standard"
    budget_usd: float = 10.0
    max_parallel: int = 5
    output_formats: list[Literal["json", "sarif", "markdown"]] = Field(
        default_factory=lambda: ["json", "sarif", "markdown"]
    )
    workspace_root: str = "."
    clearwing_path: str = "clearwing"
    auto_ingest: bool = True
    auto_task_gen: bool = False
    timeout_seconds: int = 3600

    @model_validator(mode="after")
    def validate_target(self) -> "SourcehuntInput":
        if bool(self.repo_url) == bool(self.local_path):
            raise ValueError("Exactly one of repo_url or local_path is required")
        return self


class SourcehuntOutput(BaseModel):
    ok: bool
    error: str | None = None
    message: str = ""
    session_id: str = ""
    command: list[str] = Field(default_factory=list)
    output_dir: str = ""
    exit_code: int | None = None
    stdout_tail: str = ""
    stderr_tail: str = ""
    findings_count: int = 0
    findings_by_severity: dict[str, int] = Field(default_factory=dict)
    findings_by_evidence_level: dict[str, int] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
    agn_finding_ids: list[str] = Field(default_factory=list)
    agn_evidence_id: str | None = None
    task_graph_paths: list[str] = Field(default_factory=list)
    markdown: str = ""


def _now_session_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"cw-{stamp}-{uuid.uuid4().hex[:8]}"


def _install_message() -> str:
    return "\n".join(
        [
            "Clearwing CLI was not found.",
            "Install and configure it with:",
            "  git clone https://github.com/Lazarus-AI/clearwing.git",
            "  cd clearwing && uv sync --all-extras",
            "  clearwing setup",
        ]
    )


def _resolve_binary(clearwing_path: str) -> str | None:
    candidate = Path(clearwing_path).expanduser()
    if candidate.exists() and candidate.is_file():
        return str(candidate.resolve())
    return shutil.which(clearwing_path)


def _resolve_target(input_data: SourcehuntInput, workspace_root: Path) -> str:
    if input_data.repo_url:
        return input_data.repo_url
    local = Path(input_data.local_path or ".").expanduser()
    if not local.is_absolute():
        local = workspace_root / local
    return str(local.resolve())


def _format_arg(formats: list[str]) -> str:
    normalized = {fmt.lower() for fmt in formats}
    if {"json", "sarif", "markdown"}.issubset(normalized):
        return "all"
    if len(normalized) == 1:
        return next(iter(normalized))
    return "all"


def _tail(text: bytes, limit: int = 4000) -> str:
    decoded = text.decode("utf-8", errors="replace")
    return decoded[-limit:]


def _markdown(output: SourcehuntOutput) -> str:
    lines = [
        "# Clearwing Sourcehunt",
        "",
        f"Status: {'OK' if output.ok else 'FAILED'}",
        f"Session: `{output.session_id}`",
        f"Findings: {output.findings_count}",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity, count in sorted(output.findings_by_severity.items()):
        lines.append(f"| {severity} | {count} |")
    if output.error:
        lines.extend(["", f"Error: `{output.error}`", "", output.message])
    return "\n".join(lines)


async def _run_command(command: list[str], timeout_seconds: int) -> tuple[int, bytes, bytes]:
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout_seconds)
    except TimeoutError:
        process.kill()
        stdout, stderr = await process.communicate()
        return 124, stdout, stderr
    return process.returncode or 0, stdout, stderr


@action_spec(
    key="clearwing.sourcehunt",
    version="1.0.0",
    summary="Run Clearwing source-code vulnerability hunting",
    description="Invokes the external Clearwing CLI, stores reports under data/secscan/results, and optionally ingests findings.",
    tags=["security", "clearwing", "sourcehunt", "vulnerability"],
    source="plugin",
    idempotent=False,
    risk_level="high",
    timeout_seconds=3600.0,
)
async def clearwing_sourcehunt(input_data: SourcehuntInput) -> SourcehuntOutput:
    workspace_root = Path(input_data.workspace_root).resolve()
    session_id = _now_session_id()
    output_dir = workspace_root / "data" / "secscan" / "results" / session_id
    binary = _resolve_binary(input_data.clearwing_path)

    if binary is None:
        output = SourcehuntOutput(
            ok=False,
            error="clearwing_not_found",
            message=_install_message(),
            session_id=session_id,
            output_dir=output_dir.as_posix(),
        )
        output.markdown = _markdown(output)
        return output

    output_dir.mkdir(parents=True, exist_ok=True)
    target = _resolve_target(input_data, workspace_root)
    command = [
        binary,
        "sourcehunt",
        target,
        "--depth",
        input_data.depth,
        "--budget",
        str(input_data.budget_usd),
        "--max-parallel",
        str(input_data.max_parallel),
        "--output-dir",
        output_dir.as_posix(),
        "--format",
        _format_arg(input_data.output_formats),
    ]

    exit_code, stdout, stderr = await _run_command(command, input_data.timeout_seconds)
    ingester = _load_ingester()
    report_paths = ingester.discover_report_paths(output_dir)

    findings_count = 0
    findings_by_severity: dict[str, int] = {}
    findings_by_evidence_level: dict[str, int] = {}
    agn_finding_ids: list[str] = []
    agn_evidence_id: str | None = None
    if input_data.auto_ingest:
        ingestion = ingester.ingest_clearwing_findings(
            workspace_root=workspace_root,
            session_id=session_id,
            report_dir=output_dir,
            source_check="clearwing.sourcehunt@1.0.0",
            report_paths=report_paths,
        )
        report_paths = ingestion["report_paths"]
        findings_count = ingestion["findings_count"]
        findings_by_severity = ingestion["findings_by_severity"]
        findings_by_evidence_level = ingestion["findings_by_evidence_level"]
        agn_finding_ids = ingestion["agn_finding_ids"]
        agn_evidence_id = ingestion["agn_evidence_id"]

    ok = exit_code == 0
    output = SourcehuntOutput(
        ok=ok,
        error=None if ok else "clearwing_exit_nonzero",
        message="Clearwing sourcehunt completed." if ok else "Clearwing sourcehunt exited with a nonzero status.",
        session_id=session_id,
        command=command,
        output_dir=output_dir.as_posix(),
        exit_code=exit_code,
        stdout_tail=_tail(stdout),
        stderr_tail=_tail(stderr),
        findings_count=findings_count,
        findings_by_severity=findings_by_severity,
        findings_by_evidence_level=findings_by_evidence_level,
        report_paths=report_paths,
        agn_finding_ids=agn_finding_ids,
        agn_evidence_id=agn_evidence_id,
        task_graph_paths=[],
    )
    output.markdown = _markdown(output)
    return output


entry = clearwing_sourcehunt.entry
