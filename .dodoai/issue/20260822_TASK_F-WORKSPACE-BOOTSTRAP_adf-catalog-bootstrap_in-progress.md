---
type: issue
title: ADF 要件カタログ（EPIC/CAP/FR JSON-first SoT + provenance Index）の新設と ADF パス接続
tags: [crypto-wealth-os, adf, catalog, epic, cap, fr, workspace-bootstrap]
---

# TASK — ADF 要件カタログ bootstrap（EPIC / CAP / FR + provenance Index）

> **Task**: `task-adf-catalog-bootstrap` | **Feature**: `F-WORKSPACE-BOOTSTRAP` | **Status**: running
> **TaskGraph 正本**: `docs/99.sdt/agn/features/task-adf-catalog-bootstrap/task-task-adf-catalog-bootstrap.json`（本 MD はその人間可読 view）
> **HIL 裁定**: 2026-08-22 dodo Coder セッションでユーザー承認 — EPIC 6 + CAP 8 + FR セット + `impl_provenance`（dodoAI 本体実装参照 Index）方式

## 背景

`docs/3.strategy/01-implementation-priority.md` が ADF の要件アーキテクチャ（EPIC→Feature 縦糸 / CAP─owns→FR 横糸）を経由せず Feature ID を直接並べており、catalog（`docs/99.sdt/art/catalog/source/`）も未初期化だった。A02 Step 0（所有 EPIC/CAP の catalog 確認 — HARD）を満たせない状態を解消する。

## スコープ（done_criteria）

1. `docs/99.sdt/art/catalog/source/epics.json` — 6 EPIC（FOUNDATION / VIABILITY / WORLD-MODEL / OPPORTUNITY / GUARDIAN / SETTLEMENT）+ 所属 Feature
2. `docs/99.sdt/art/catalog/source/caps.json` — 8 CAP + 所有 FR（各 FR に traces + impl_provenance + core_ref）
3. `docs/4.common/3.capability-requirements/00-capability-requirements.md` — CAP→FR の MD view（JSON と対）
4. `docs/3.strategy/01-implementation-priority.md` — EPIC / CAP(FR) / satisfies 列 + ADF パス参照の追加
5. `docs/1.concept/03-approach.md` — 実装順①〜⑪ → EPIC/CAP 写像
6. `docs/4.common/README.md` — CR→CAP(FR) 導出列
7. `docs/2.sdt-design/01-development-roadmap.md` / `docs/README.md` の同一変更追随（`1.concept/2.strategy` の旧パス参照 → `3.strategy` へのリンク修復含む）

## 裁定済みの体系（要旨）

- **EPIC 6**: EPIC-FOUNDATION / EPIC-VIABILITY / EPIC-WORLD-MODEL / EPIC-OPPORTUNITY / EPIC-GUARDIAN / EPIC-SETTLEMENT（Concept 三要素 + 04 の 3 グラフ空間から導出）
- **CAP 8**: CAP-ONCHAIN-OBSERVE / CAP-VIABILITY-EVAL / CAP-POLICY-ENGINE / CAP-OPPORTUNITY-GEN / CAP-RISK-DETECT / CAP-EVIDENCE-LEDGER / CAP-KEY-CUSTODY / CAP-EXEC-PIPELINE（SR 群 + 15 Gate + 運用ループ①〜⑥から導出）
- **impl_provenance**: `dodoai-core`（本体機構を参照のみ・再実装禁止）/ `dodoai-core+custom-rules`（機構は本体・検査ルールのみ custom）/ `custom`（personal scope 実装）

## 進行記録

| 日時 | 事象 |
|---|---|
| 2026-08-22 16:47 | Task node 作成（running）。HIL 承認済みの体系で catalog 作成開始 |
