---
type: execution-result
execution_id: 3cf772d6-d8a4-486a-8607-9162917d09b6
title: F-CRYPTO-PORTFOLIO-DASHBOARD A02 画面定義 Evidence
tags: [a02, ed15, ed16, screen-definition, epic-viability]
---

# A02 画面定義 Evidence

`EPIC-VIABILITY` と既存の `CAP-ONCHAIN-OBSERVE` / `CAP-VIABILITY-EVAL` / `CAP-EVIDENCE-LEDGER` に対し、ADF ED15 画面一覧と ED16 画面設計書を MD+JSON の対で作成した。新しい EPIC / CAP / FR は作成していない。

## 定義した表示責務

- ETH / BTC / BNB 等の銘柄記号、名称、held / watch-only、数量、価格、24h 変化、評価額、構成比、価格ソース状態
- 保存済み Fact だけで描く価格履歴 line chart
- 評価可能な保有銘柄だけで描く資産配分 bar chart
- Fresh / Stale、Healthy / Degraded / Alert、DRIFTED / Not configured
- 欠損値を `$0.00` やゼロ履歴へ捏造しない空状態・エラー状態
- chart と同じ観測を確認できる表形式代替、色だけに依存しない状態表示

## 検証

- JSON parse: PASS
- ED15 / ED16 Screen ID 対応: PASS
- 必須 dashboard blocks: PASS
- Feature 内の非正準 `CAP-PORTFOLIO-*` 参照除去: PASS
- `git diff --check`: PASS

## A03 結果

`a03.sdt_agn_conformance_gate` は `ok=false`。workspace に SDT layout / authoring contract が無く、schema self-conformance は `CONTRACT_MISSING`、authoring validation は 25/25 unclassified、placement は `NO_INPUT` だった。これは画面要件の不合格ではなく `F-WORKSPACE-BOOTSTRAP` の未完了負債だが、HARD Gate のため DD 実装は再開しない。

正規 `sdt_layout.schema_sync` は同期元 contract も同じ project 内に要求するため、初回生成には使えなかった。別 checkout の `workspace_root` から生成物だけを本 worktree に残す禁止経路は使っていない。

## Runtime

Native MCP は Core start timeout 後に利用不能となった。workspace slot 8522 に owner/listener がなく、標準 sidecar 起動を非破壊で 1 回試みたが resolver が dodoai workspace lease を選択したため fail-closed。Action 実行は project ID を明示した Tauri Desktop control gateway fallback を使用した。可視 UI / runtime の reload・restart は実行していない。

## 次の条件

1. `F-WORKSPACE-BOOTSTRAP` で layout / authoring contract を正規生成する。
2. A03 を再実行して DD 入場可能にする。
3. ED16 どおりに銘柄、価格履歴、配分グラフ、空/劣化状態を実装する。

## Roadmap sync

`roadmap.sync_gate` は `ok=false`。`roadmap_drift=0` だが、DD01 task status 2 件、Feature milestone 1 件、EPIC orphan 1 件、CAP unbound 1 件を検出した。Feature catalog / roadmap bootstrap の未完了を隠さず、A02 Task は `done` にしない。

Machine-readable pair: `evidence-a02-screen-definition.json`
