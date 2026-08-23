---
type: issue
execution_id: personal-custom-app-policy-20260822-01
title: Personal Custom App policy
---

# Personal Custom App policy

- Task: `F-WORKSPACE-BOOTSTRAP-DD01-PERSONAL-CUSTOM-APP-POLICY`
- Feature: `F-WORKSPACE-BOOTSTRAP`
- Status: `running`
- User intent: dodo Crypto Wealth OS を基本方針としてパーソナルの dodo Custom App として作り、Concept と `AGENTS.md` に反映する。

## Done criteria

- `AGENTS.md` が personal dodo Custom App を既定のプロダクト形態として宣言する。
- Concept が single-owner / local-first / Custom UI + Custom Action の境界を宣言する。
- multi-user、public SaaS、hosted custody、第三者向け商用化への拡張は HIL と Concept/A02 更新なしに行わない。
- 変更した governance artifact の JSON parse と対象文字列検査が通る。

## Evidence

- User HIL: `user://2026-08-22/personal-custom-app-policy`
- `agn.route_next`: explicit `F-WORKSPACE-BOOTSTRAP`, adaptive mode because the standard workflow is not initialized.
- `taskgraph.dd_select_claim`: lease acquired by `codex-root` for this Task node.
- Scoped policy assertions and `git diff --check`: PASS against `AGENTS.md`, `.clinerules/00-CORE.md`, `docs/README.md`, and `docs/1.concept/*`.
- Upstream ClineRules integrity test: `28 passed`.
- `rules.audit`: unavailable because `docs/99.sdt/agn/99.rules/rule-catalog.json` is not initialized.
- `roadmap.sync_gate`: `ok=false`, `stale_task_status=1`; the roadmap workflow cannot resolve `F-WORKSPACE-BOOTSTRAP`.
- Edit lease release returned already expired / not owned; no active lease remained.

## Changed files

- `AGENTS.md`
- `.clinerules/00-CORE.md`
- `docs/README.md`
- `docs/1.concept/00-overview.md`
- `docs/1.concept/06-common-requirements.md`
- `.dodoai/issue/20260822_TASK_F-WORKSPACE-BOOTSTRAP_personal-custom-app-policy_in-progress.md`

## Remaining governance work

- A concurrent docs SoT migration removed `docs/99.sdt/agn/1.workflows/workspace-initialization/features/F-WORKSPACE-BOOTSTRAP/` from the working tree after this task had been created and claimed. The staged Task JSON was not used to overwrite that concurrent deletion.
- Rules catalog / Roadmap SoT / owning Feature registration must be reconciled before this Task or Feature can be marked `done`.
- Formal status remains `running`; the requested Concept and instruction policy edits themselves are present and locally verified.

## Notes

- Operation catalog / Agent definition は未初期化のため推測選定しない。
- Runtime/UI reload or restart は行わない。
