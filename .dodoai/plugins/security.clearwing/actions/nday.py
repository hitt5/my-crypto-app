"""clearwing.nday — Phase 2 N-day assessment placeholder."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from dodo_core.module.plugin_sdk import action_spec


class NdayInput(BaseModel):
    repo_url: str | None = None
    local_path: str | None = None
    cve_list: list[str] = Field(default_factory=list)
    workspace_root: str = "."

    @model_validator(mode="after")
    def validate_target(self) -> "NdayInput":
        if bool(self.repo_url) == bool(self.local_path):
            raise ValueError("Exactly one of repo_url or local_path is required")
        return self


class NdayOutput(BaseModel):
    ok: bool
    error: str
    message: str
    cve_list: list[str]
    markdown: str


@action_spec(
    key="clearwing.nday",
    version="1.0.0",
    summary="Clearwing N-day CVE impact assessment",
    description="Phase 2 placeholder for Clearwing N-day sourcehunt mode.",
    tags=["security", "clearwing", "nday", "cve"],
    source="plugin",
    idempotent=False,
    risk_level="medium",
)
async def clearwing_nday(input_data: NdayInput) -> NdayOutput:
    message = "clearwing.nday is reserved for Phase 2. Phase 1 implements sourcehunt and ingestion."
    return NdayOutput(
        ok=False,
        error="phase2_not_enabled",
        message=message,
        cve_list=input_data.cve_list,
        markdown=f"# Clearwing N-day Assessment\n\nStatus: blocked\n\n{message}",
    )


entry = clearwing_nday.entry
