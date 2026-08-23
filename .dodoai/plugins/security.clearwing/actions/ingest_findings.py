"""clearwing.ingest — ingest Clearwing JSON/SARIF findings."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from pydantic import BaseModel, Field

from dodo_core.module.plugin_sdk import action_spec


def _load_ingester():
    module_path = Path(__file__).resolve().parents[1] / "ingestion" / "finding_ingester.py"
    spec = importlib.util.spec_from_file_location("security_clearwing_ingester", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Clearwing ingester: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IngestFindingsInput(BaseModel):
    workspace_root: str = Field(default=".", description="dodoai workspace root")
    session_id: str = Field(description="Clearwing sourcehunt session id")
    source_check: str = Field(default="clearwing.sourcehunt@1.0.0")
    report_dir: str | None = Field(default=None)
    report_paths: dict[str, str] = Field(default_factory=dict)


class IngestFindingsOutput(BaseModel):
    ok: bool
    session_id: str
    findings_count: int = 0
    findings_by_severity: dict[str, int] = Field(default_factory=dict)
    findings_by_evidence_level: dict[str, int] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
    agn_finding_ids: list[str] = Field(default_factory=list)
    agn_evidence_id: str | None = None
    markdown: str = ""


@action_spec(
    key="clearwing.ingest",
    version="1.0.0",
    summary="Ingest Clearwing findings",
    description="Parses Clearwing JSON/SARIF reports and emits local AGN Finding/Evidence artifact candidates.",
    tags=["security", "clearwing", "ingestion", "sarif"],
    source="plugin",
    idempotent=True,
    risk_level="low",
)
async def clearwing_ingest(input_data: IngestFindingsInput) -> IngestFindingsOutput:
    workspace_root = Path(input_data.workspace_root).resolve()
    report_dir = Path(input_data.report_dir).resolve() if input_data.report_dir else workspace_root / "data" / "secscan" / "results" / input_data.session_id
    ingester = _load_ingester()
    result = ingester.ingest_clearwing_findings(
        workspace_root=workspace_root,
        session_id=input_data.session_id,
        report_dir=report_dir,
        source_check=input_data.source_check,
        report_paths=input_data.report_paths,
    )
    return IngestFindingsOutput(
        ok=True,
        session_id=input_data.session_id,
        findings_count=result["findings_count"],
        findings_by_severity=result["findings_by_severity"],
        findings_by_evidence_level=result["findings_by_evidence_level"],
        report_paths=result["report_paths"],
        agn_finding_ids=result["agn_finding_ids"],
        agn_evidence_id=result["agn_evidence_id"],
        markdown=ingester.render_ingestion_markdown(result),
    )


entry = clearwing_ingest.entry
