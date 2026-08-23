---
type: test-result
execution_id: 8621c2e2-aa5a-4d19-90a7-c5a724fa4b4a
title: F-CRYPTO-PORTFOLIO-DASHBOARD DD02-DD03 visualization evidence
timestamp: 2026-08-22T12:56:34Z
---

# DD02–DD03 visualization evidence

## 結果

画面定義に対応する価格履歴・資産配分・held/watch-only 銘柄・価格ソース状態の実装、および DD03 の欠損/異常系テストは合格した。稼働中 Core は新規 Personal Action 登録前の registry のため、project-scoped live dispatch だけ未達。ユーザー可視 runtime の reload/restart は行っていない。

| 検証 | 結果 |
| --- | --- |
| focused pytest | PASS — 26 passed |
| Ruff | PASS — findings 0 |
| manifest JSON | PASS |
| strict manifest lint | PASS — errors 0 / warnings 0（personal path 非対応のため同一 bytes を正規 lint path で検証） |
| 実価格 Tick | PASS — 2 runs、ETH/BTC/BNB、保存済み |
| 価格履歴 | PASS — 13 points、BNB/BTC/ETH |
| 銘柄投影 | PASS — ETH held、BNB/BTC watch-only、配分は ETH のみ |
| 欠損値の 0 捏造防止 | PASS |
| 空/1点履歴、壊れた JSONL、範囲外入力 | PASS |
| 単一 source degradation | PASS |
| project-scoped Core dispatch | BLOCKED — 新 Action は 404、未承認 reload は未実施 |
| `roadmap.sync_gate` | PASS — `ok=true`、全 drift count 0（legacy milestone waiver） |

## 残作業

ユーザー自身の reload、または reload 操作への明示承認後に `personal.crypto_price_history` / `personal.crypto_asset_overview` を Core 経由で dispatch し、ダッシュボードの live UI 証跡を取得する。
