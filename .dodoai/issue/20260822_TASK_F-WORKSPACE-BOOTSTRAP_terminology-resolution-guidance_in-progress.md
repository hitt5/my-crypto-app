---
type: issue
execution_id: terminology-resolution-guidance-20260822-01
title: SCO and ADF terminology resolution guidance
---

# SCO and ADF terminology resolution guidance

- Task: `F-WORKSPACE-BOOTSTRAP-DD01-TERMINOLOGY-RESOLUTION-GUIDANCE`
- Feature: `F-WORKSPACE-BOOTSTRAP`
- Status: `running`
- User intent: SCO と ADF を推測で解釈せず、正本から理解できるようにする。未知語は Charter / 用語集を参照し、ADF は dodoAI の ADF 正本パスを読む。

## Done criteria

- `AGENTS.md` が未知・多義的な用語を `docs/0.charter/` と `docs/GLOSSARY.md` で確認するよう指示する。
- `AGENTS.md` が ADF の参照先を `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/` と dodoAI の開発フロー Charter に固定する。
- `docs/GLOSSARY.md` が SCO を Semantic Canonical Ontology として説明し、project scope との混同を防ぐ。
- 対象文字列検査、Markdown front matter 検査、`git diff --check` が通る。

## Evidence

- dodoAI の SCO 画面設計は SCO を `SDT Semantic Canonical Ontology` と定義している。
- dodoAI の ADF 日本語概要・用語集は ADF を `Agentic Development Framework` と定義している。
- `sdt_layout.resolve` は project-local layout contract 未生成で失敗したため、既存 `F-WORKSPACE-BOOTSTRAP` の workflow 配置を使用した。
- `task_graph.acquire_edit_lease`: `success=true`, `required=false`（SQLite-backed project）。
- 参照 path 実在、対象用語、front matter、Task JSON、`git diff --check`: PASS。
- `rules.audit`: rule catalog 未生成（`docs/99.sdt/agn/99.rules/rule-catalog.json` 不在）のため実行不能。
- `roadmap.sync_gate`: `ok=false`; `stale_task_status=0`, `missing_milestone=1`, `epic_orphan=1`, `cap_unbound=1`, `roadmap_drift=0`。
- `sovereign.hook_gate`: `block=false`, `required_operations=0`。

## Changed files

- `AGENTS.md`
- `docs/GLOSSARY.md`
- `.clinerules/00-CORE.md`
- `.clinerules/00-INDEX.md`
- `.dodoai/issue/20260822_TASK_F-WORKSPACE-BOOTSTRAP_terminology-resolution-guidance_in-progress.md`
- `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-WORKSPACE-BOOTSTRAP/task-dd01-terminology-resolution-guidance.json`

## Existing blockers

- Operation catalog / Agent definitions が未初期化のため、Operation / Agent は推測選定しない。
- `F-WORKSPACE-BOOTSTRAP` の既存 catalog / layout-contract 負債は本作業の外であり、Feature 完了扱いにしない。
- edit lease は `required=false` だったため release 対象 token はない。Task は Completion Gate 未達のまま `running` を維持する。

## Notes

- Runtime / UI の reload・restart は行わない。
