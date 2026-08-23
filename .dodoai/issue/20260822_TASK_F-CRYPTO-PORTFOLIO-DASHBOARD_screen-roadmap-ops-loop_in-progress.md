---
type: issue
title: 画面ロードマップ改訂 — Ops（Network/Agent/WF）+ LOOP 運用画面の追加
tags: [crypto-wealth-os, screen-roadmap, ops, loop, a02]
---

# 画面ロードマップ改訂 — Ops + LOOP 運用画面

| 項目 | 値 |
| --- | --- |
| Task (SoT) | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd00-a02-screen-roadmap-ops-loop.json` |
| Feature | `F-CRYPTO-PORTFOLIO-DASHBOARD`（画面正本の現所有 Feature。Ops 系新 Feature の起票は HIL 後） |
| Status | in-progress |
| HIL 起点 | 2026-08-22 ユーザー指摘「ネットワーク接続管理・Agent 実行管理が無いと絶対できない」「Loop も追加して」 |

## 背景

ED15（`docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-list.md`）はドメイン画面 2 枚のみで、コンセプト（`03-approach.md` OODA×WF・LOOP Catalog、`04-network-policy.md` L1→L2→L3）を運用するための基盤画面が未定義。

## スコープ

1. `docs/3.strategy/03-screen-roadmap.md` を新設: 全画面（基盤 Ops + LOOP 運用 + ドメイン）を Feature / 運用ループステップ / 優先度へ接続した画面ロードマップ正本
2. ED15 screen-list から画面ロードマップへの参照追記
3. `roadmap.sync_gate` 実行

## スコープ外

- 各画面の ED15/ED16 詳細設計（所有 Feature の A02 で作成）
- Ops 系新 Feature（例: F-OPS-CONSOLE）の A02 起票 — EPIC/CAP 接続の HIL が先
- LOOP catalog（`loops.json`）の生成 — `F-WORKSPACE-BOOTSTRAP` の残作業
