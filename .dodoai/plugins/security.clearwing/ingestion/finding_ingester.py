"""Clearwing finding ingestion helpers.

This module is intentionally plugin-local. It parses Clearwing JSON/SARIF
reports and emits local AGN artifact candidates without importing Clearwing.
"""

from __future__ import annotations

import json
import logging
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

VERIFIED_LEVELS = {
    "crash_reproduced",
    "root_cause_explained",
    "exploit_demonstrated",
    "patch_validated",
}
OBSERVED_LEVELS = {"suspicion", "static_corroboration"}
SEVERITIES = {"critical", "high", "medium", "low", "info"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _coerce_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("findings", "results", "vulnerabilities", "issues"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return [payload] if payload.get("description") or payload.get("title") else []


def _sarif_results(payload: Any, sarif_path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        return findings
    for run in payload.get("runs", []):
        if not isinstance(run, dict):
            continue
        rules: dict[str, dict[str, Any]] = {}
        for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
            if isinstance(rule, dict) and rule.get("id"):
                rules[str(rule["id"])] = rule
        for result in run.get("results", []):
            if not isinstance(result, dict):
                continue
            rule_id = str(result.get("ruleId") or "clearwing")
            rule = rules.get(rule_id, {})
            location = (result.get("locations") or [{}])[0]
            physical = location.get("physicalLocation", {}) if isinstance(location, dict) else {}
            region = physical.get("region", {}) if isinstance(physical, dict) else {}
            artifact = physical.get("artifactLocation", {}) if isinstance(physical, dict) else {}
            findings.append(
                {
                    "id": result.get("fingerprints", {}).get("clearwing") or result.get("guid") or rule_id,
                    "title": result.get("message", {}).get("text") or rule.get("name") or rule_id,
                    "description": result.get("message", {}).get("text") or rule.get("fullDescription", {}).get("text") or rule_id,
                    "severity": result.get("level") or rule.get("defaultConfiguration", {}).get("level") or "medium",
                    "file_path": artifact.get("uri"),
                    "line_number": region.get("startLine"),
                    "cwe": _first_cwe(rule),
                    "evidence_level": result.get("properties", {}).get("evidence_level") or "static_corroboration",
                    "sarif_ref": sarif_path.as_posix(),
                }
            )
    return findings


def _first_cwe(rule: dict[str, Any]) -> str | None:
    for tag in rule.get("properties", {}).get("tags", []):
        if isinstance(tag, str) and tag.upper().startswith("CWE-"):
            return tag.upper()
    return None


def _severity(value: Any) -> str:
    raw = str(value or "medium").lower()
    if raw == "error":
        return "high"
    if raw == "warning":
        return "medium"
    if raw == "note":
        return "low"
    return raw if raw in SEVERITIES else "medium"


def _truth_type(evidence_level: str) -> str:
    level = evidence_level.lower()
    if level in VERIFIED_LEVELS:
        return "verified"
    if level in OBSERVED_LEVELS:
        return "observed"
    return "observed"


def _source_ref(finding: dict[str, Any]) -> str:
    file_path = str(finding.get("file_path") or finding.get("file") or finding.get("path") or "unknown")
    line = finding.get("line_number") or finding.get("line") or 0
    return f"{file_path}:{line}"


def _finding_id(session_id: str, finding: dict[str, Any]) -> str:
    raw_id = str(
        finding.get("id")
        or finding.get("finding_id")
        or finding.get("clearwing_finding_id")
        or _source_ref(finding)
    )
    return f"finding-security-{uuid.uuid5(uuid.NAMESPACE_URL, session_id + ':' + raw_id)}"


def discover_report_paths(report_dir: Path) -> dict[str, str]:
    paths: dict[str, str] = {}
    for path in sorted(report_dir.glob("*")):
        suffix = path.suffix.lower()
        if suffix == ".sarif" and "sarif" not in paths:
            paths["sarif"] = path.as_posix()
        elif suffix == ".json" and path.name not in {"agn-findings.json", "scan-evidence.json"} and "json" not in paths:
            paths["json"] = path.as_posix()
        elif suffix in {".md", ".markdown"} and "markdown" not in paths:
            paths["markdown"] = path.as_posix()
    return paths


def parse_clearwing_findings(report_dir: Path, report_paths: dict[str, str] | None = None) -> list[dict[str, Any]]:
    paths = dict(report_paths or {})
    if not paths:
        paths = discover_report_paths(report_dir)

    findings: list[dict[str, Any]] = []
    json_path = paths.get("json")
    if json_path:
        json_file = Path(json_path)
        if json_file.exists():
            findings.extend(_coerce_list(_read_json(json_file)))

    sarif_path = paths.get("sarif")
    if sarif_path:
        sarif_file = Path(sarif_path)
        if sarif_file.exists():
            findings.extend(_sarif_results(_read_json(sarif_file), sarif_file))

    return findings


def ingest_clearwing_findings(
    *,
    workspace_root: Path,
    session_id: str,
    report_dir: Path,
    source_check: str,
    report_paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    report_dir.mkdir(parents=True, exist_ok=True)
    resolved_paths = dict(report_paths or discover_report_paths(report_dir))
    raw_findings = parse_clearwing_findings(report_dir, resolved_paths)

    nodes: list[dict[str, Any]] = []
    for finding in raw_findings:
        evidence_level = str(finding.get("evidence_level") or "static_corroboration").lower()
        severity = _severity(finding.get("severity"))
        node_id = _finding_id(session_id, finding)
        source_ref = _source_ref(finding)
        description = str(finding.get("description") or finding.get("title") or "Clearwing security finding")
        nodes.append(
            {
                "node_id": node_id,
                "type": "finding",
                "layer": "execution",
                "truth_type": _truth_type(evidence_level),
                "finding_type": "security_vulnerability",
                "source_check": source_check,
                "severity": severity,
                "summary": description[:160],
                "description": description,
                "remediation": str(finding.get("remediation") or finding.get("fix") or "Review Clearwing report and patch the vulnerable code path."),
                "source_ref": source_ref,
                "metadata": {
                    "cwe": finding.get("cwe"),
                    "cvss": finding.get("cvss"),
                    "evidence_level": evidence_level,
                    "crash_evidence": finding.get("crash_evidence"),
                    "patch_status": finding.get("patch_status"),
                    "clearwing_session_id": session_id,
                    "clearwing_finding_id": str(finding.get("id") or finding.get("finding_id") or node_id),
                    "sarif_ref": finding.get("sarif_ref") or resolved_paths.get("sarif"),
                },
            }
        )

    severity_counts = Counter(node["severity"] for node in nodes)
    evidence_counts = Counter(node["metadata"]["evidence_level"] for node in nodes)
    evidence_id = f"evidence-security-scan-{uuid.uuid5(uuid.NAMESPACE_URL, session_id)}"
    evidence = {
        "node_id": evidence_id,
        "type": "evidence",
        "layer": "execution",
        "truth_type": "observed",
        "evidence_type": "security_scan",
        "status": "success",
        "session_id": session_id,
        "source_system": "clearwing",
        "created_at": _now_iso(),
        "workspace_root": workspace_root.as_posix(),
        "findings_count": len(nodes),
        "findings_by_severity": dict(severity_counts),
        "findings_by_evidence_level": dict(evidence_counts),
        "report_paths": resolved_paths,
        "created_by_action": source_check,
    }
    causal_refs = [
        {
            "from": evidence_id,
            "to": node["node_id"],
            "type": "caused_by_scan",
        }
        for node in nodes
    ]

    (report_dir / "agn-findings.json").write_text(
        json.dumps({"schema": "clearwing-agn-findings-v1", "nodes": nodes, "edges": causal_refs}, indent=2),
        encoding="utf-8",
    )
    (report_dir / "scan-evidence.json").write_text(
        json.dumps(evidence, indent=2),
        encoding="utf-8",
    )

    logger.debug(
        "clearwing_ingest session=%s findings=%d evidence=%s",
        session_id,
        len(nodes),
        evidence_id,
    )

    return {
        "findings_count": len(nodes),
        "findings_by_severity": dict(severity_counts),
        "findings_by_evidence_level": dict(evidence_counts),
        "agn_finding_ids": [node["node_id"] for node in nodes],
        "agn_evidence_id": evidence_id,
        "report_paths": {
            **resolved_paths,
            "agn_findings": (report_dir / "agn-findings.json").as_posix(),
            "scan_evidence": (report_dir / "scan-evidence.json").as_posix(),
        },
    }


def render_ingestion_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Clearwing Finding Ingestion",
        "",
        f"Findings: {result.get('findings_count', 0)}",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity, count in sorted(result.get("findings_by_severity", {}).items()):
        lines.append(f"| {severity} | {count} |")
    return "\n".join(lines)
