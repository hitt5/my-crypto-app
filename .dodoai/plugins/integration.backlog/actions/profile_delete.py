"""backlog.profile_delete — remove a project-scoped Backlog profile."""

from __future__ import annotations

from pydantic import BaseModel, Field

from dodo_core.module.plugin_sdk import action_spec

from ._core_api import CoreApiError, resolve_project, update_integration_profiles


class ProfileDeleteInput(BaseModel):
    project_id: str = Field(..., min_length=1)
    workspace_id: str = "local"
    profile_id: str = Field(..., min_length=1)


class ProfileDeleteOutput(BaseModel):
    ok: bool
    error: str | None = None
    project_id: str = ""
    profile_id: str = ""
    deleted: bool = False


@action_spec(
    key="backlog.profile_delete",
    version="1.0.0",
    summary="Delete a project-scoped Backlog connection profile",
    description=(
        "Removes one Backlog profile from the project's integration settings. "
        "Credential material in Keychain/SecretStore is NOT deleted (managed separately)."
    ),
    tags=["plugin", "backlog", "integration", "mutation"],
    source="plugin",
    idempotent=True,
    risk_level="medium",
    timeout_seconds=30.0,
)
async def backlog_profile_delete(input_data: ProfileDeleteInput) -> ProfileDeleteOutput:
    try:
        project_id, settings = await resolve_project(
            input_data.project_id, input_data.workspace_id
        )
    except CoreApiError:
        return ProfileDeleteOutput(
            ok=False, error="project_not_found", project_id=input_data.project_id
        )
    current = [
        profile
        for profile in settings.get("integration_profiles", [])
        if isinstance(profile, dict)
    ]
    remaining = [
        p
        for p in current
        if not (p.get("id") == input_data.profile_id and p.get("provider") == "backlog")
    ]
    deleted = len(remaining) != len(current)
    if deleted:
        try:
            await update_integration_profiles(project_id, remaining)
        except Exception as exc:
            return ProfileDeleteOutput(
                ok=False, error=f"update_failed: {exc}", project_id=project_id
            )

    return ProfileDeleteOutput(
        ok=True,
        project_id=project_id,
        profile_id=input_data.profile_id,
        deleted=deleted,
    )


entry = backlog_profile_delete.entry
