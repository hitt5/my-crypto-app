---
type: issue
title: P0 画面実装 — DOM-1 / OPS-1 / OPS-2 portfolio scope
tags: [crypto-wealth-os, custom-ui, p0, ops, dashboard]
---

# P0 画面実装 — Portfolio Feature 所有範囲

正本は [`task-dd01-screen-roadmap-p0-implementation.json`](../../docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd01-screen-roadmap-p0-implementation.json)。画面範囲は [`docs/3.strategy/03-screen-roadmap.md`](../../docs/3.strategy/03-screen-roadmap.md) に従う。

| 項目 | 値 |
| --- | --- |
| Task | `T-CRYPTO-PORTFOLIO-DASHBOARD-DD01-SCREEN-ROADMAP-P0-IMPLEMENTATION-20260822` |
| Feature | `F-CRYPTO-PORTFOLIO-DASHBOARD` |
| Status | running — local single-writer: `codex-root-screen-roadmap-20260822` |
| 対象 | DOM-1、OPS-1、OPS-2 の portfolio source 部分 |

## 完了条件

- DOM-1 の既存契約を壊さない。
- OPS-1 は chain、RPC、Anvil、L1→L2→L3 昇格証跡、mainnet Observe-only guard を秘密値なしで表示する。
- OPS-2 は config hash/lint、source freshness、`env://` 解決可否だけを表示し、解決値を返さない。
- manifest は `custom_ui.manifest_edit` の strict dry-run → apply、strict lint を通す。
- Python focused test で malformed/missing config、secret redaction、network guard、partial failure を検証する。

## この Task で実装しない画面

- OPS-3: 新 Feature の EPIC/CAP HIL が未完了。
- LOOP-1: project-local LOOP catalog が未初期化。
- DOM-3/4/5/7: 所有 Feature の A02/A03 が未完了。
- DOM-6: Stage 2 / H4 HIL 前の先行実装は禁止。

## Governance finding

`agn_issue_creator` v2 は対象 task を 13 files の scan 中に検出できず `matched_tasks=0` を返したため、本 view は Task SoT から手動作成した。Action の検出不整合は完了時 Evidence に残す。

## 現在の結果

- `crypto-wealth-ops/network` と `crypto-wealth-ops/sources` を `custom_ui.manifest_edit` strict dry-run → apply で作成した。
- `personal.crypto_ops_status` は秘密値を返さず、network/config/env/freshness/promotion 状態を返す。
- focused test は 45 passed。新 Action の Ruff は 0 findings。
- registry で既存 `crypto-wealth` と新規 `crypto-wealth-ops` の共存を確認した。

## 未達 Gate

- ED15/ED16 の A02 追補前に実装へ入ったため ADF 順序違反を Finding として記録した。
- `custom_ui.manifest_lint` は personal path を `MANIFEST_PATH_OUTSIDE_WORKSPACE` で拒否する。
- 稼働 Core に新 Action は未登録。reload/restart は実行していない。
- Core workspace slot `8522` は listener 不在となり、`roadmap.sync_gate` を実行できない。
- live UI / desktop / mobile visual evidence は未計測。
- 既存 screen-roadmap Issue が参照する `task-dd00-a02-screen-roadmap-ops-loop.json` は現 worktree に存在せず、既報 `done` を検証できない。

Evidence: `docs/99.sdt/art/test-results/F-CRYPTO-PORTFOLIO-DASHBOARD/evidence-dd03-screen-roadmap-p0-implementation.md`
