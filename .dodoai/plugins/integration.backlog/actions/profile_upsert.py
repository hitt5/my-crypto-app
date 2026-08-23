"""backlog.profile_upsert — create or update a project-scoped Backlog profile.

Writes to the project's ``integration_profiles`` settings (the single SoT
shared with the VCS pipeline and the AI Chat work-item pipeline). API key
values are never accepted raw — only managed credential references
(``keychain://``, ``secretstore://``, ``env://BACKLOG_API_KEY``).
"""

from __future__ import annotations

from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, field_validator

from dodo_core.module.plugin_sdk import action_spec

from ._core_api import CoreApiError, resolve_project, update_integration_profiles

_ALLOWED_REF_PREFIXES = ("keychain://", "secretstore://")
_SERVER_ENV_REF = "env://BACKLOG_API_KEY"


class ProfileUpsertInput(BaseModel):
    project_id: str = Field(..., min_length=1)
    workspace_id: str = "local"
    profile_id: str = Field(..., min_length=1, max_length=80)
    display_name: str = Field(..., min_length=1, max_length=120)
    purpose: Literal["vcs", "work_item", "both"] = "both"
    base_url: str = Field(..., min_length=1)
    project_key: str = Field(..., min_length=2)
    permission_level: Literal["lv1", "lv2", "lv3", "lv4"] = "lv1"
    api_key_ref: str | None = Field(
        default=None,
        description="keychain://<key> | secretstore://<key> | env://BACKLOG_API_KEY",
    )
    auto_sync: bool = False
    sync_interval_minutes: int = Field(default=20, ge=1)
    max_issues_total: int | None = Field(default=None, ge=1)
    max_issues_per_run: int = Field(default=100, ge=1, le=1000)
    closed_status_names: list[str] = Field(
        default_factory=lambda: ["完了", "Closed", "Resolved", "Done"]
    )
    comment_policy: Literal["none", "active_only", "all"] = "active_only"
    enabled: bool = True

    @field_validator("api_key_ref")
    @classmethod
    def validate_api_key_ref(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if cleaned == _SERVER_ENV_REF:
            return cleaned
        if any(
            cleaned.startswith(prefix) and len(cleaned) > len(prefix)
            for prefix in _ALLOWED_REF_PREFIXES
        ):
            return cleaned
        raise ValueError(
            "api_key_ref must be keychain://<key>, secretstore://<key>, or env://BACKLOG_API_KEY "
            "(raw API key values are rejected)"
        )


class ProfileUpsertOutput(BaseModel):
    ok: bool
    error: str | None = None
    project_id: str = ""
    profile_id: str = ""
    created: bool = False


@action_spec(
    key="backlog.profile_upsert",
    version="1.0.0",
    summary="Create or update a project-scoped Backlog connection profile",
    description=(
        "Upserts one Backlog profile (display name, purpose Git/Issues/Both, URL, project key, "
        "permission level, API key credential ref) into the project's integration settings. "
        "Multiple profiles per project are supported."
    ),
    tags=["plugin", "backlog", "integration", "mutation"],
    source="plugin",
    idempotent=True,
    risk_level="medium",
    timeout_seconds=30.0,
)
async def backlog_profile_upsert(input_data: ProfileUpsertInput) -> ProfileUpsertOutput:
    base_url = input_data.base_url.strip().rstrip("/")
    parsed_base_url = urlsplit(base_url)
    if parsed_base_url.scheme != "https" or not parsed_base_url.hostname:
        return ProfileUpsertOutput(
            ok=False,
            error="base_url_https_required",
            project_id=input_data.project_id,
            profile_id=input_data.profile_id,
        )
    try:
        project_id, settings = await resolve_project(
            input_data.project_id, input_data.workspace_id
        )
    except CoreApiError:
        return ProfileUpsertOutput(
            ok=False, error="project_not_found", project_id=input_data.project_id
        )
    current = [
        profile
        for profile in settings.get("integration_profiles", [])
        if isinstance(profile, dict)
    ]
    existing = next(
        (profile for profile in current if profile.get("id") == input_data.profile_id),
        None,
    )
    api_key_ref = input_data.api_key_ref or (
        (existing.get("credential_refs") or {}).get("api_key")
        if existing is not None
        else None
    )
    if not api_key_ref:
        return ProfileUpsertOutput(
            ok=False,
            error="api_key_ref_required_for_new_profile",
            project_id=project_id,
            profile_id=input_data.profile_id,
        )

    new_profile = {
        "id": input_data.profile_id,
        "provider": "backlog",
        "display_name": input_data.display_name,
        "purpose": input_data.purpose,
        "enabled": input_data.enabled,
        "fields": {
            "base_url": base_url,
            "project_key": input_data.project_key,
            "permission_level": input_data.permission_level,
            "auto_sync": input_data.auto_sync,
            "sync_interval_minutes": input_data.sync_interval_minutes,
            "max_issues_total": input_data.max_issues_total,
            "max_issues_per_run": input_data.max_issues_per_run,
            "closed_status_names": input_data.closed_status_names,
            "comment_policy": input_data.comment_policy,
        },
        "credential_refs": {"api_key": api_key_ref},
    }

    profiles = [p for p in current if p.get("id") != input_data.profile_id]
    created = len(profiles) == len(current)
    profiles.append(new_profile)
    try:
        await update_integration_profiles(project_id, profiles)
    except Exception as exc:  # noqa: BLE001 - plugin boundary returns a typed failure
        return ProfileUpsertOutput(
            ok=False, error=f"update_failed: {exc}", project_id=project_id
        )

    return ProfileUpsertOutput(
        ok=True,
        project_id=project_id,
        profile_id=input_data.profile_id,
        created=created,
    )


entry = backlog_profile_upsert.entry
