"""Backlog WorkItem Actions owned by the integration.backlog Plugin."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from dodo_core.module.plugin_sdk import (
    ActionEntry,
    ClosureDigestBatchResult,
    FeedbackJob,
    WorkItemAnalysis,
    WorkItemAskResult,
    WorkItemAutoSyncResult,
    WorkItemConnection,
    WorkItemConnectionNotFound,
    WorkItemError,
    WorkItemIssueDetail,
    WorkItemPermissionError,
    WorkItemPermissionLevel,
    WorkItemReport,
    WorkItemSdtAskResult,
    WorkItemSdtProjectionResult,
    WorkItemSyncResult,
    action_spec,
    get_work_item_action_runtime,
)

logger = logging.getLogger(__name__)


def set_work_item_action_dependencies(**dependencies: object) -> None:
    """Test hook delegated through the public Plugin SDK runtime."""
    get_work_item_action_runtime().set_dependencies(**dependencies)


def reset_work_item_action_dependencies() -> None:
    get_work_item_action_runtime().reset_dependencies()


class BacklogConnectionRegisterInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    name: str = "Backlog"
    base_url: str
    backlog_project_key: str | None = None
    backlog_project_id: int | None = None
    credential_ref: str = Field(
        ..., description="Managed secret reference such as keychain://BACKLOG_API_KEY"
    )
    permission_level: WorkItemPermissionLevel = WorkItemPermissionLevel.LV1


class BacklogConnectionRegisterOutput(BaseModel):
    success: bool = True
    connection: WorkItemConnection | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.connection_register",
    version="1.0.0",
    summary="Register a Backlog issue connection for AIChat work item actions",
    description="Stores Backlog connection metadata and a credential reference. Raw API keys are never persisted.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "ai-chat", "setup"],
    risk_level="medium",
    timeout_seconds=30.0,
    idempotent=True,
    log_input=False,
)
async def backlog_connection_register(
    input: BacklogConnectionRegisterInput,
) -> BacklogConnectionRegisterOutput:
    try:
        if not input.project_id:
            return BacklogConnectionRegisterOutput(
                success=False,
                warnings=[
                    "project_id is required for tenant/project-scoped Backlog connections"
                ],
            )
        connection = await get_work_item_action_runtime().register_connection(
            **input.model_dump()
        )
        return BacklogConnectionRegisterOutput(connection=connection)
    except Exception as exc:  # noqa: BLE001 - plugin boundary returns sanitized failures
        logger.warning("work_item.backlog.connection_register failed: %s", exc)
        return BacklogConnectionRegisterOutput(success=False, warnings=[str(exc)])


class BacklogSyncInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    updated_since: datetime | None = None
    include_comments: bool = True
    max_issues: int = Field(default=100, ge=1, le=1000)
    actor: str | None = None


class BacklogSyncOutput(BaseModel):
    success: bool = True
    result: WorkItemSyncResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.sync",
    version="1.0.0",
    summary="Sync Backlog issues and comments into the local work item cache",
    description="Fetches Backlog issues with updatedSince cursor, stores issues/comments, and records sync audit rows.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sync", "ai-chat"],
    risk_level="medium",
    timeout_seconds=90.0,
    idempotent=True,
)
async def backlog_sync(input: BacklogSyncInput) -> BacklogSyncOutput:
    try:
        result = await get_work_item_action_runtime().sync(**input.model_dump())
        return BacklogSyncOutput(
            success=result.success, result=result, warnings=result.warnings
        )
    except WorkItemConnectionNotFound as exc:
        return BacklogSyncOutput(success=False, warnings=[str(exc)])


class BacklogIssueGetInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    issue_key: str
    include_comments: bool = True
    include_latest_analysis: bool = True


class BacklogIssueGetOutput(BaseModel):
    success: bool = True
    detail: WorkItemIssueDetail | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.issue_get",
    version="1.0.0",
    summary="Get one Backlog issue detail from the project-scoped local cache",
    description="Returns a synchronized Backlog issue with comments and latest analysis for the active project only.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "issue", "detail", "ai-chat", "readonly"],
    risk_level="low",
    timeout_seconds=30.0,
    idempotent=True,
)
async def backlog_issue_get(input: BacklogIssueGetInput) -> BacklogIssueGetOutput:
    try:
        detail = await get_work_item_action_runtime().issue_get(**input.model_dump())
        return BacklogIssueGetOutput(detail=detail)
    except (WorkItemConnectionNotFound, LookupError, WorkItemError) as exc:
        return BacklogIssueGetOutput(success=False, warnings=[str(exc)])


class BacklogAskInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    question: str = Field(..., min_length=1)
    issue_key: str | None = None
    limit: int = Field(default=100, ge=1, le=500)


class BacklogAskOutput(BaseModel):
    success: bool = True
    answer: str | None = None
    result: WorkItemAskResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.ask",
    version="1.0.0",
    summary="Answer natural-language questions about synchronized Backlog issues",
    description="Uses the active project's local Backlog cache to answer questions without exposing other projects.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "qa", "ai-chat", "readonly"],
    risk_level="low",
    timeout_seconds=45.0,
    idempotent=True,
)
async def backlog_ask(input: BacklogAskInput) -> BacklogAskOutput:
    try:
        result = await get_work_item_action_runtime().ask(**input.model_dump())
        return BacklogAskOutput(
            answer=result.answer, result=result, warnings=result.warnings
        )
    except (WorkItemConnectionNotFound, LookupError, WorkItemError) as exc:
        return BacklogAskOutput(success=False, warnings=[str(exc)])


class BacklogSyncDueConnectionsInput(BaseModel):
    tenant_id: str = "default"
    workspace_id: str = "local"
    project_id: str | None = None
    include_comments: bool = True
    max_issues_per_connection: int = Field(default=100, ge=1, le=1000)
    actor: str = "cron:backlog-auto-sync"


class BacklogSyncDueConnectionsOutput(BaseModel):
    success: bool = True
    result: WorkItemAutoSyncResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.sync_due_connections",
    version="1.0.0",
    summary="Sync Backlog profiles that enabled project-settings auto sync",
    description="Scans project integration profiles and synchronizes only enabled Backlog profiles with fields.auto_sync=true.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sync", "cron", "project-settings"],
    risk_level="medium",
    timeout_seconds=180.0,
    idempotent=True,
)
async def backlog_sync_due_connections(
    input: BacklogSyncDueConnectionsInput,
) -> BacklogSyncDueConnectionsOutput:
    try:
        result = await get_work_item_action_runtime().sync_due_connections(
            **input.model_dump()
        )
        return BacklogSyncDueConnectionsOutput(
            success=result.success, result=result, warnings=result.warnings
        )
    except WorkItemError as exc:
        return BacklogSyncDueConnectionsOutput(success=False, warnings=[str(exc)])
    except Exception as exc:  # noqa: BLE001 - one profile failure must not abort the scan
        logger.warning("work_item.backlog.sync_due_connections failed: %s", exc)
        return BacklogSyncDueConnectionsOutput(success=False, warnings=[str(exc)])


class BacklogAnalyzeInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    issue_keys: list[str] | None = None
    limit: int = Field(default=20, ge=1, le=100)
    use_llm: bool = False
    llm_model: str | None = None


class BacklogAnalyzeOutput(BaseModel):
    success: bool = True
    analyses: list[WorkItemAnalysis] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.analyze",
    version="1.0.0",
    summary="Analyze Backlog issues for summary, category, risk, and next actions",
    description="Produces read-only AI/heuristic recommendations and never mutates Backlog issue fields.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "analysis", "ai-chat", "readonly"],
    risk_level="low",
    timeout_seconds=90.0,
    idempotent=True,
)
async def backlog_analyze(input: BacklogAnalyzeInput) -> BacklogAnalyzeOutput:
    try:
        analyses = await get_work_item_action_runtime().analyze(**input.model_dump())
        return BacklogAnalyzeOutput(analyses=analyses)
    except (WorkItemConnectionNotFound, WorkItemError) as exc:
        return BacklogAnalyzeOutput(success=False, warnings=[str(exc)])


class BacklogCommentPostInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    issue_key: str
    analysis_id: str | None = None
    comment_body: str | None = Field(
        default=None,
        description="Optional free-form comment body. Requires dry_run=true preview before dry_run=false posting.",
    )
    dry_run: bool = True
    actor: str | None = None


class BacklogCommentPostOutput(BaseModel):
    success: bool = True
    feedback: FeedbackJob | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.comment_post",
    version="1.0.0",
    summary="Post an AI analysis comment to Backlog when dry_run is explicitly false",
    description="Formats a saved analysis as a Backlog comment; no field/status/priority mutation is supported.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "comment", "mutation", "ai-chat"],
    risk_level="medium",
    timeout_seconds=60.0,
    idempotent=False,
)
async def backlog_comment_post(
    input: BacklogCommentPostInput,
) -> BacklogCommentPostOutput:
    try:
        feedback = await get_work_item_action_runtime().comment_post(
            **input.model_dump()
        )
        return BacklogCommentPostOutput(
            success=feedback.error_message is None,
            feedback=feedback,
            warnings=[feedback.error_message] if feedback.error_message else [],
        )
    except (WorkItemConnectionNotFound, WorkItemPermissionError, LookupError) as exc:
        return BacklogCommentPostOutput(success=False, warnings=[str(exc)])


class BacklogReportGenerateInput(BaseModel):
    tenant_id: str = "default"
    project_id: str | None = None
    connection_id: str | None = None
    limit: int = Field(default=100, ge=1, le=1000)


class BacklogReportGenerateOutput(BaseModel):
    success: bool = True
    report: WorkItemReport | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.report_generate",
    version="1.0.0",
    summary="Generate a Backlog AI project report from saved analyses",
    description="Aggregates categories, risk levels, overdue/unassigned counts, top risks, and next actions.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "report", "ai-chat", "readonly"],
    risk_level="low",
    timeout_seconds=30.0,
    idempotent=True,
)
async def backlog_report_generate(
    input: BacklogReportGenerateInput,
) -> BacklogReportGenerateOutput:
    try:
        report = await get_work_item_action_runtime().report_generate(
            **input.model_dump()
        )
        return BacklogReportGenerateOutput(report=report)
    except WorkItemConnectionNotFound as exc:
        return BacklogReportGenerateOutput(success=False, warnings=[str(exc)])


class BacklogSdtProjectInput(BaseModel):
    tenant_id: str = "default"
    project_id: str
    connection_id: str | None = None
    max_issues_per_run: int | None = Field(default=None, ge=1, le=1000)
    max_issues_total: int | None = Field(default=None, ge=1)
    comment_policy: Literal["none", "active_only", "all"] | None = None
    actor: str | None = None


class BacklogSdtProjectOutput(BaseModel):
    success: bool = True
    result: WorkItemSdtProjectionResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.sdt_project",
    version="1.0.0",
    summary="Project one bounded Backlog issue batch into project-scoped SDT shards",
    description="Uses the profile limits and cursor without writing the legacy work_items cache.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sdt", "projection"],
    risk_level="medium",
    timeout_seconds=180.0,
    idempotent=True,
)
async def backlog_sdt_project(input: BacklogSdtProjectInput) -> BacklogSdtProjectOutput:
    try:
        result = await get_work_item_action_runtime().sdt_project(**input.model_dump())
        return BacklogSdtProjectOutput(
            success=result.success, result=result, warnings=result.warnings
        )
    except (WorkItemConnectionNotFound, WorkItemError, ValueError) as exc:
        return BacklogSdtProjectOutput(success=False, warnings=[str(exc)])


@action_spec(
    key="work_item.backlog.backfill",
    version="1.0.0",
    summary="Run one resumable Backlog-to-SDT backfill step",
    description="Advances the durable offset only after a successful bounded projection step.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sdt", "backfill"],
    risk_level="medium",
    timeout_seconds=180.0,
    idempotent=True,
)
async def backlog_sdt_backfill(
    input: BacklogSdtProjectInput,
) -> BacklogSdtProjectOutput:
    try:
        result = await get_work_item_action_runtime().sdt_backfill(**input.model_dump())
        return BacklogSdtProjectOutput(
            success=result.success, result=result, warnings=result.warnings
        )
    except (WorkItemConnectionNotFound, WorkItemError, ValueError) as exc:
        return BacklogSdtProjectOutput(success=False, warnings=[str(exc)])


class BacklogSdtAskInput(BaseModel):
    tenant_id: str = "default"
    project_id: str
    connection_id: str | None = None
    question: str = Field(..., min_length=1)
    include_closed: bool = False
    top_n: int | None = Field(default=None, ge=1, le=100)
    display_limit: int = Field(default=20, ge=1, le=100)
    response_level: Literal["L1", "L2", "L3"] = "L1"


class BacklogSdtAskOutput(BaseModel):
    success: bool = True
    answer: str = ""
    result: WorkItemSdtAskResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.sdt_ask",
    version="1.0.0",
    summary="Query Backlog SDT with bounded L1/L2/L3 disclosure",
    description="Scores the index first and opens only selected shards for L3 responses.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sdt", "qa", "readonly"],
    risk_level="low",
    timeout_seconds=45.0,
    idempotent=True,
)
async def backlog_sdt_ask(input: BacklogSdtAskInput) -> BacklogSdtAskOutput:
    try:
        result = await get_work_item_action_runtime().sdt_ask(**input.model_dump())
        return BacklogSdtAskOutput(
            answer=result.answer, result=result, warnings=result.warnings
        )
    except (WorkItemConnectionNotFound, WorkItemError, ValueError) as exc:
        return BacklogSdtAskOutput(success=False, warnings=[str(exc)])


class BacklogClosureDigestInput(BaseModel):
    tenant_id: str = "default"
    project_id: str
    connection_id: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


class BacklogClosureDigestOutput(BaseModel):
    success: bool = True
    result: ClosureDigestBatchResult | None = None
    warnings: list[str] = Field(default_factory=list)


@action_spec(
    key="work_item.backlog.closure_digest",
    version="1.0.0",
    summary="Generate a bounded batch of evidence-grounded Backlog Closure Digests",
    description="Uses deterministic fallback and never emits a digest without evidence_refs.",
    owner="integration.backlog",
    tags=["plugin", "work-item", "backlog", "sdt", "closure", "digest"],
    risk_level="medium",
    timeout_seconds=90.0,
    idempotent=True,
)
async def backlog_closure_digest(
    input: BacklogClosureDigestInput,
) -> BacklogClosureDigestOutput:
    try:
        result = await get_work_item_action_runtime().closure_digest(
            **input.model_dump()
        )
        return BacklogClosureDigestOutput(result=result, warnings=result.warnings)
    except (WorkItemConnectionNotFound, WorkItemError, LookupError, ValueError) as exc:
        return BacklogClosureDigestOutput(success=False, warnings=[str(exc)])


connection_register_entry: ActionEntry = backlog_connection_register.entry
sync_entry: ActionEntry = backlog_sync.entry
issue_get_entry: ActionEntry = backlog_issue_get.entry
ask_entry: ActionEntry = backlog_ask.entry
sync_due_connections_entry: ActionEntry = backlog_sync_due_connections.entry
analyze_entry: ActionEntry = backlog_analyze.entry
comment_post_entry: ActionEntry = backlog_comment_post.entry
report_generate_entry: ActionEntry = backlog_report_generate.entry
sdt_project_entry: ActionEntry = backlog_sdt_project.entry
backfill_entry: ActionEntry = backlog_sdt_backfill.entry
sdt_ask_entry: ActionEntry = backlog_sdt_ask.entry
closure_digest_entry: ActionEntry = backlog_closure_digest.entry
