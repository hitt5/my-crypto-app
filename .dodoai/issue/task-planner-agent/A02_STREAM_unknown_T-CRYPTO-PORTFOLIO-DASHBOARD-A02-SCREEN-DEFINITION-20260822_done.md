---
type: issue-stream
title: A02 - EPIC/CAP aligned crypto portfolio screen definition
tags: [crypto-wealth-os, a02, screen-list, screen-design, epic, capability]
---

# STREAM Define EPIC/CAP-aligned crypto portfolio screens

| Field | Value |
| --- | --- |
| Task ID: | `T-CRYPTO-PORTFOLIO-DASHBOARD-A02-SCREEN-DEFINITION-20260822` |
| Slug: | `T-CRYPTO-PORTFOLIO-DASHBOARD-A02-SCREEN-DEFINITION-20260822` |
| UC ID | UC-1, UC-2, UC-3 |
| FR IDs | FR-OBS-1, FR-OBS-2, FR-VIA-3, FR-EVD-1, FR-EVD-5 |
| Feature | `F-CRYPTO-PORTFOLIO-DASHBOARD` |
| EPIC | `EPIC-VIABILITY` |
| Module | `.dodoai/personal` |
| Agent | `task-planner-agent` |
| DD Phase | `A02` |
| Priority | `P0` |
| Status | ✅ Done |
| Task Graph Ref: | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd00-a02-screen-definition.json#T-CRYPTO-PORTFOLIO-DASHBOARD-A02-SCREEN-DEFINITION-20260822` |
| Created By | `agn_issue_creator@2.0.0` |
| Created At | `2026-08-22T12:13:55.576777+00:00` |

## 🎯 目標（1行）
承認済み EPIC/CAP/FR に基づき、ADF ED15 画面一覧と ED16 画面設計書を MD+JSON の対で定義してから実装へ戻す。

## 📥 入力（spec_refs — このStreamが読むファイル）
- `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/5.document/3.external-design/46-screen-list.md`
- `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/5.document/3.external-design/47-screen-design.md`
- `docs/3.strategy/02-epic-cap-priority-roadmap.md`
- `docs/4.common/3.capability-requirements/00-capability-requirements.md`
- `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`

## 📤 出力（このStreamが書き込むファイル — Owned Files）
- `docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-list.md`
- `docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-list.json`
- `docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-design.md`
- `docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-design.json`
- Feature spec / Feature node / Task node の trace 同期

## 🔧 実装ステップ
1. `EPIC-VIABILITY` と正準 CAP/FR の対応を修復する。
2. ADF ED15 に従い、安定 Screen ID・route・役割・遷移・アクセス・優先度を定義する。
3. ADF ED16 に従い、銘柄行・評価額/配分/履歴グラフ・状態・Action 契約・異常系・アクセシビリティ・テストを定義する。
4. MD+JSON 双対を検証し、A03 conformance を記録する。A03 前に UI 実装へ戻らない。

## ✅ 完了チェックリスト（FR の受入基準から）
- [x] ADF ED15 / ED16 と承認済み EPIC/CAP/FR を確認した
- [x] `CAP-PORTFOLIO-*` 非正準参照を除去した
- [x] ED15 画面一覧を MD+JSON で作成した
- [x] ED16 画面設計を MD+JSON で作成した
- [x] 銘柄一覧と履歴/配分グラフの表示契約・空/エラー/鮮度状態を定義した
- [x] A03 conformance を実行し、workspace contract 欠損による fail-closed を記録した
- [x] `roadmap.sync_gate` を実行し、既存 bootstrap 負債を記録した

## 🚪 Gate 条件
No further dashboard implementation until the ED15/ED16 MD+JSON pairs trace every visible section to existing UC and CAP-owned FR, and A03 conformance results are recorded.

## A03 Finding

`a03.sdt_agn_conformance_gate` は `ok=false`。Feature 固有の画面要件ではなく、workspace の `docs/99.sdt/0.schema/sdt-layout-contract.json` / `sdt-authoring-contract.json` が未生成であるため、schema self-conformance が `CONTRACT_MISSING`、authoring validation が 25/25 unclassified、placement が `NO_INPUT` となった。別 checkout の contract を流し込む回避策は採用せず、`F-WORKSPACE-BOOTSTRAP` の正規生成経路で解消するまで DD 実装を再開しない。

Evidence: `docs/99.sdt/art/test-results/F-CRYPTO-PORTFOLIO-DASHBOARD/evidence-a02-screen-definition.json`

## Roadmap Finding

`roadmap.sync_gate` は `ok=false`。`roadmap_drift=0` だが、DD01 task status 2 件、milestone 1 件、EPIC binding 1 件、CAP binding 1 件が不足している。A02 画面要件は作成済みだが、Completion Gate と A03 Gate を満たさないため Task は `blocked` とする。

2026-08-22: ユーザーが DD03 までの実装再開を明示。project contract と catalog の bootstrap 修復を開始し、TaskGraph status を `running` へ戻した。

解消結果: project contract/catalog を補完し、A03 は Feature advanced、`roadmap.sync_gate` は milestone compatibility waiver 付きで全 finding 0。TaskGraph を `done` へ同期した。

## 🔗 次のStreamへの引き継ぎ情報
- depends_on: `-`
- assigned_agent: `task-planner-agent`
