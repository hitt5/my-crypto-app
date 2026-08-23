---
type: issue
title: F-CRYPTO-PORTFOLIO-DASHBOARD table block rendering repair
tags: [crypto-wealth-os, personal-custom-ui, dd03]
---

# F-CRYPTO-PORTFOLIO-DASHBOARD — table block rendering repair

## TaskGraph SoT

- Task: `T-CRYPTO-PORTFOLIO-DASHBOARD-TABLE-RENDER-20260822`
- Feature: `F-CRYPTO-PORTFOLIO-DASHBOARD`
- Status: `running`
- Task node: `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd03-table-block-rendering.json`
- Spec: `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`

## Intent

Crypto Wealth dashboard の4つの `table` block が unsupported fallback として表示される不具合を、現行 Custom UI block contract に合わせて修復する。Portfolio/Opportunity の意味、read-only 境界、Action payload は変更しない。

## Done criteria

- 4 block が `data-table` と `rows_field` を使用する。
- `table` / `items_field` の旧 contract が残らない。
- focused manifest regression test が PASS する。
- live dashboard に unsupported fallback が残らない。
- strict manifest lint と `roadmap.sync_gate` の実結果を記録する。未達なら Task は `running` のままにする。

## Known governance findings

- project Operation/Agent catalog、SDT layout contract、ADF test definition、roadmap graph は未初期化。
- 現行 `custom_ui.manifest_lint` は personal scope path を `.dodoai/custom_ui` 外として拒否する。

## Activity

- 2026-08-22: `task_graph.acquire_edit_lease` は SQLite backend のため `required=false`。
- 2026-08-22: `task_graph.transition_status` で `ready → running`。
- 2026-08-22: 4 block を `data-table` / `rows_field` contract へ移行し、manifest 回帰テストを追加。
- 2026-08-22: focused `1 passed`、configured full suite `17 passed`、strict content lint `error_count=0`。bare Python は `dodo_core` import path 不足で invalid。
- 2026-08-22: live registry は manifest `1.0.1` を返し、headless dashboard は unsupported fallback `0` / table `4`。
- 2026-08-22: live personal Action は未登録で HTTP 404。ユーザー可視 runtime の reload / restart は未実施。
- 2026-08-22: `roadmap.sync_gate` は `ok=false`。Task は `running` を維持。

## Evidence

- `docs/99.sdt/art/test-results/F-CRYPTO-PORTFOLIO-DASHBOARD/evidence-dd03-table-block-rendering.json`
- `docs/99.sdt/art/test-results/F-CRYPTO-PORTFOLIO-DASHBOARD/evidence-dd03-table-block-rendering.md`
