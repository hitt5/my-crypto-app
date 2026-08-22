"""backlog.profile_list — list project-scoped Backlog connection profiles.

The SoT for profiles is the project's ``integration_profiles`` settings
(list of ProjectIntegrationProfile with provider="backlog"). This plugin
Action reads them through the project repository so the Plugin Management
screen can manage Backlog connections per dodoAI project.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field

from dodo_core.module.plugin_sdk import action_spec

from ._core_api import CoreApiError, resolve_project


class ProfileListInput(BaseModel):
    project_id: str = Field(..., min_length=1, description="dodoAI project id or slug")
    workspace_id: str = "local"
    purpose: str | None = Field(
        default=None,
        description="Optional filter: vcs / work_item / both",
    )


class BacklogProfileView(BaseModel):
    id: str
    connection_id: str = ""
    display_name: str
    purpose: str = "both"
    enabled: bool = True
    base_url: str = ""
    project_key: str = ""
    permission_level: str = "lv1"
    auto_sync: bool = False
    sync_interval_minutes: int = 20
    max_issues_total: int | None = None
    max_issues_per_run: int = 100
    closed_status_names: list[str] = Field(
        default_factory=lambda: ["完了", "Closed", "Resolved", "Done"]
    )
    comment_policy: Literal["none", "active_only", "all"] = "active_only"
    api_key_configured: bool = False
    api_key_ref_kind: str = "none"  # keychain / secretstore / server-env / none
    api_key_ref_name: str = ""  # safe identifier only; never the secret value


class ProfileListOutput(BaseModel):
    ok: bool
    error: str | None = None
    project_id: str = ""
    profiles: list[BacklogProfileView] = Field(default_factory=list)


def _connection_id(project_id: str, profile_id: str) -> str:
    """Mirror the public Backlog connection identifier contract."""
    clean_project = re.sub(r"[^A-Za-z0-9_.-]+", "-", project_id.strip()).strip("-")
    clean_profile = (
        re.sub(r"[^A-Za-z0-9_.-]+", "-", profile_id.strip()).strip("-") or "backlog"
    )
    return (
        clean_profile
        if not clean_project or clean_profile.startswith(f"{clean_project}-")
        else f"{clean_project}-{clean_profile}"
    )


def _ref_kind(ref: str) -> str:
    if ref.startswith("keychain://"):
        return "keychain"
    if ref.startswith("secretstore://"):
        return "secretstore"
    if ref == "env://BACKLOG_API_KEY":
        return "server-env"
    return "none"


def _ref_name(ref: str) -> str:
    """Return the non-secret credential identifier without its storage scheme."""
    if ref.startswith("keychain://"):
        return ref.removeprefix("keychain://")
    if ref.startswith("secretstore://"):
        return ref.removeprefix("secretstore://")
    if ref == "env://BACKLOG_API_KEY":
        return "BACKLOG_API_KEY"
    return ""


def _to_view(profile: dict) -> BacklogProfileView:
    fields = profile.get("fields") or {}
    refs = profile.get("credential_refs") or {}
    api_key_ref = str(refs.get("api_key") or "")
    raw_interval = fields.get("sync_interval_minutes")
    try:
        interval = max(int(raw_interval), 1)
    except (TypeError, ValueError):
        interval = 20
    return BacklogProfileView(
        id=str(profile.get("id") or ""),
        display_name=str(profile.get("display_name") or ""),
        purpose=str(profile.get("purpose") or "both"),
        enabled=profile.get("enabled") is not False,
        base_url=str(fields.get("base_url") or ""),
        project_key=str(fields.get("project_key") or ""),
        permission_level=str(fields.get("permission_level") or "lv1"),
        auto_sync=fields.get("auto_sync") is True,
        sync_interval_minutes=interval,
        max_issues_total=(
            int(fields["max_issues_total"])
            if isinstance(fields.get("max_issues_total"), int)
            and fields["max_issues_total"] >= 1
            else None
        ),
        max_issues_per_run=(
            max(1, min(int(fields.get("max_issues_per_run", 100)), 1000))
            if isinstance(fields.get("max_issues_per_run", 100), int)
            else 100
        ),
        closed_status_names=[
            str(value)
            for value in fields.get(
                "closed_status_names", ["完了", "Closed", "Resolved", "Done"]
            )
            if isinstance(value, str) and value.strip()
        ],
        comment_policy=(
            fields.get("comment_policy")
            if fields.get("comment_policy") in {"none", "active_only", "all"}
            else "active_only"
        ),
        api_key_configured=bool(api_key_ref),
        api_key_ref_kind=_ref_kind(api_key_ref),
        api_key_ref_name=_ref_name(api_key_ref),
    )


@action_spec(
    key="backlog.profile_list",
    version="1.0.0",
    summary="List project-scoped Backlog connection profiles",
    description=(
        "Returns Backlog integration profiles (display name, purpose, URL, project key, "
        "permission level, credential status) for one dodoAI project. API key values are "
        "never returned — only the reference kind and non-secret credential identifier."
    ),
    tags=["plugin", "backlog", "integration", "readonly"],
    source="plugin",
    idempotent=True,
    risk_level="low",
    timeout_seconds=15.0,
)
async def backlog_profile_list(input_data: ProfileListInput) -> ProfileListOutput:
    try:
        project_id, settings = await resolve_project(
            input_data.project_id, input_data.workspace_id
        )
    except CoreApiError:
        return ProfileListOutput(
            ok=False, error="project_not_found", project_id=input_data.project_id
        )

    profiles = [
        _to_view(profile)
        for profile in settings.get("integration_profiles", [])
        if isinstance(profile, dict) and profile.get("provider") == "backlog"
    ]
    for profile in profiles:
        profile.connection_id = _connection_id(project_id, profile.id)
    if input_data.purpose in ("vcs", "work_item", "both"):
        profiles = [
            p
            for p in profiles
            if p.purpose == input_data.purpose or p.purpose == "both"
        ]

    return ProfileListOutput(ok=True, project_id=project_id, profiles=profiles)


entry = backlog_profile_list.entry
