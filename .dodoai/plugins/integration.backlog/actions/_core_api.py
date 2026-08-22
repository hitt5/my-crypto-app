"""Public Core API client used by the Backlog plugin actions."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class CoreApiError(RuntimeError):
    """Raised when the public Core API cannot satisfy a plugin request."""


def _http_error_message(status: int, body: str) -> str:
    """Reduce FastAPI validation envelopes to stable, user-facing text."""
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return f"core_api_http_{status}: {body}"
    details = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(details, list):
        messages = [
            str(detail.get("msg"))
            for detail in details
            if isinstance(detail, dict) and detail.get("msg")
        ]
        if messages:
            return f"core_api_http_{status}: {'; '.join(messages)}"
    if isinstance(details, str):
        return f"core_api_http_{status}: {details}"
    return f"core_api_http_{status}: {body}"


def _base_url() -> str:
    return os.getenv("DODO_CORE_BASE_URL", "http://127.0.0.1:8510").rstrip("/")


def _request_sync(
    method: str, path: str, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        f"{_base_url()}{path}",
        data=body,
        method=method,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=10.0) as response:  # noqa: S310 - fixed loopback/configured Core URL
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise CoreApiError(_http_error_message(exc.code, detail)) from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise CoreApiError(f"core_api_unavailable: {exc}") from exc
    if not isinstance(result, dict):
        raise CoreApiError("core_api_invalid_response")
    return result


async def request_json(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call the Core REST boundary without blocking the Action event loop."""
    return await asyncio.to_thread(_request_sync, method, path, payload)


async def resolve_project(
    project_id: str, workspace_id: str
) -> tuple[str, dict[str, Any]]:
    """Resolve an id/slug and return the typed project settings payload."""
    listing = await request_json("GET", "/api/projects/")
    projects = listing.get("projects")
    if not isinstance(projects, list):
        raise CoreApiError("core_api_invalid_project_list")
    match = next(
        (
            project
            for project in projects
            if isinstance(project, dict)
            and (project.get("id") == project_id or project.get("slug") == project_id)
            and (not workspace_id or project.get("workspace_id") == workspace_id)
        ),
        None,
    )
    if match is None:
        raise CoreApiError("project_not_found")
    resolved_id = str(match["id"])
    response = await request_json(
        "GET", f"/api/projects/{quote(resolved_id, safe='')}/settings"
    )
    settings = response.get("settings")
    if not isinstance(settings, dict):
        raise CoreApiError("core_api_invalid_project_settings")
    return resolved_id, settings


async def update_integration_profiles(
    project_id: str,
    profiles: list[dict[str, Any]],
) -> None:
    """Persist integration profiles through the public project-settings API."""
    await request_json(
        "PUT",
        f"/api/projects/{quote(project_id, safe='')}/settings",
        {"integration_profiles": profiles},
    )
