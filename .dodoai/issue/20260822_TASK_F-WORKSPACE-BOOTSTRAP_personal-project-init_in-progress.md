---
type: issue
execution_id: workspace-bootstrap-20260822-01
title: my-crypto-app personal project initialization
---

# my-crypto-app personal project initialization

- Task: `F-WORKSPACE-BOOTSTRAP-DD01-PERSONAL-PROJECT-INIT`
- Feature: `F-WORKSPACE-BOOTSTRAP`
- Status: `running`
- User intent: dodoAI の正本 path を `AGENTS.md` に明記し、この checkout をパーソナルプロジェクトとして初期化する。

## Done criteria

- `project.scaffold` が current checkout に標準構成を生成する。
- `project.index` が `my-crypto-app` を exact path かつ `visibility=personal` で返す。
- `AGENTS.md` と ClineRules fallback 投影に dodoAI の正本 absolute path が記載される。
- 明示 project ID による bootstrap が exact path を返す。

## Evidence

- `project.scaffold` dry-run: existing files are preserved; missing standard files are planned.
- `project.scaffold` apply: 84 standard files created; 4 existing files skipped.
- Live `project.index`: `id=43e2f654-cdd7-4572-b921-962bea2f0820`, exact repository path, `visibility=personal`, `sdt_path=docs/99.sdt`.
- Live `project.bootstrap(project_id="my-crypto-app")`: `ok=true`, exact repository path, `AGENTS.md` selected.
- `.venv/bin/pytest dodo_core/tests/test_clinerules_l2_integrity_l1.py -q`: `28 passed`.
- `git diff --cached --check` and JSON parsing for repo context / Feature / Task: passed.
- `rules.audit`: failed because the scaffold does not provide `docs/99.sdt/agn/99.rules/rule-catalog.json`.
- `roadmap.sync_gate`: `ok=false`; roadmap SoT, owning EPIC, and Capability binding are not initialized.

## Notes

- 初回 scaffold は TaskGraph 自体を置くための bootstrap prerequisite として Task 作成前に実行した。
- Runtime/UI reload or restart was not performed.
- Requested initialization is live and usable; formal Feature closure remains `running` until the missing governance catalogs are initialized.
