---
type: test-result
execution_id: exec-20260822-crypto-table-render-01
title: F-CRYPTO-PORTFOLIO-DASHBOARD table block rendering evidence
tags: [crypto-wealth-os, personal-custom-ui, dd03]
---

# Table block rendering evidence

## Verdict

Unsupported block 表示の修復は実装・テスト・live render 確認まで PASS。Task / Feature の完了 Gate は未達のため `running` を維持する。

## Implementation

- `.dodoai/personal/custom_ui/crypto-wealth/manifest.json`: 4 block を `table` から `data-table`、`items_field` から `rows_field` へ移行。
- `.dodoai/personal/custom_actions/tests/test_crypto_actions.py`: block ID、data source、row field を固定した回帰テストを追加。

## Evidence

- manifest contract: `true`
- focused test: `1 passed in 0.02s`
- full personal crypto suite（canonical dodoAI workspace を `PYTHONPATH` に設定）: `17 passed in 0.09s`
- bare Python invocation: `dodo_core` import path 未設定のため `5 passed / 12 failed`。configured run で置換した harness 設定不備として記録。
- strict content lint（canonical temporary placement）: `checked_manifests=1 / error_count=0 / warning_count=0`
- Tauri-owned Core registry: manifest `1.0.1` と4つの `data-table` を live read
- headless dashboard: unsupported fallback `0`、HTML table `4`
- ユーザー可視 runtime の reload / restart: 実施なし

## Open gates

- personal scope の実パスを lint すると `checked_manifests=0` であり、実 manifest の検査証明にならない。
- action test は `/Users/hitoshimurakami/myApps/dodoai` を `PYTHONPATH` に必要とする。
- live `personal.crypto_portfolio_valuation` dispatch は HTTP 404。表構造は描画されるがデータは空表示。
- `roadmap.sync_gate`: `ok=false`。`stale_task_status=3`、`missing_milestone=1`、`roadmap_drift=0`、`epic_orphan=1`、`cap_unbound=1`、`phase_contains_missing=1`。

機械可読の対は `evidence-dd03-table-block-rendering.json`。
