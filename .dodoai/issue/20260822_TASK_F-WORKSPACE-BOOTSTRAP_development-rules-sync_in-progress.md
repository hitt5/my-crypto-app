---
type: issue
title: Synchronize reusable dodoAI development rules
tags: [workspace-bootstrap, governance, rules]
---

# F-WORKSPACE-BOOTSTRAP — dodoAI development rules sync

TaskGraph SoT: `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-WORKSPACE-BOOTSTRAP/task-dd01-development-rules-sync.json`.

## Status

- Task: `F-WORKSPACE-BOOTSTRAP-DD01-DEVELOPMENT-RULES-SYNC`
- Feature: `F-WORKSPACE-BOOTSTRAP`
- Phase: `DD01`
- Status: `running`

## Intent

Current dodoAI development rules are compared with this personal Crypto App and only reusable governance is adopted. Crypto Concept, CR-1 to CR-9, and the single-owner/local-first policy remain project-local constraints.

## Done criteria

- `AGENTS.md` includes applicable current rules without losing project-specific constraints.
- Charter, MCP guide, ClineRules L0/L1/L2, and runtime ownership guidance agree.
- The local Charter has P1-P29 and no template placeholders.
- Stale, unregistered L2 files are removed.
- Focused integrity checks, `rules.audit`, and `roadmap.sync_gate` are recorded truthfully.

## Known blockers

- `operations.json` and Agent catalog are not initialized, so no Operation or Agent is guessed.
- `sdt_layout.resolve` cannot run because the layout contract is absent; the existing Feature directory is used.
- `rules.audit`: Charter grounding is complete, but the same four delivery findings present upstream remain (`cline` / `claude` / `codex` managed sections and unmapped `dodo-code`). Applying `rules.render` would duplicate a 67 KB generated section into three instruction files, so its dry-run was intentionally not applied.
- `agn.sdt_contract_test`: this task has no remaining findings; the Feature still has three pre-existing errors in `task-dd01-terminology-resolution-guidance.json`.
- `roadmap.sync_gate`: `stale_task_status=0` and `roadmap_drift=0`, but the Feature has no roadmap milestone, owning EPIC, or capability binding.

## Evidence

- `git diff --check`: PASS.
- JSON parse validation (`jq empty`) for the task, rule catalogs/schema, and Charter DocGraph: PASS.
- Registered L2 inventory: exactly `00-README.md`, `10-preload-gate.md`, `11-completion-gate.md`, `20-navigation.md`, `30-environment.md`, and `40-domain-gates.md`.
- Charter DocGraph: 7 documents / 126 chunks; `rules.charter_sync` reports 279 grounded rules and zero source drift.
- Runtime/UI reload or restart: not performed.
