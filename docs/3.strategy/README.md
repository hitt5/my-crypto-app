---
type: concept
title: 3.strategy — 戦略（実装優先度の正本）索引
tags: [crypto-wealth-os, strategy, priority, concept, adf]
---

# 3.strategy — 戦略（Strategy）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: Concept（`../1.concept/00-overview.md` 〜 `07-why-not-simple.md`）が定義した「何を・なぜ作るか」を受けて、**「どの順で・どの基準で作るか（実装優先度）」を所有する戦略層**。
> **ADF パス（HARD）**: 優先度は ADF 要件アーキテクチャ（縦糸 `BR → SR → UC` / 横糸 `CAP ─owns→ FR`）の上に載る。**EPIC / CAP / FR の正本カタログ = [`../4.common/3.capability-requirements/00-capability-requirements.md`](../4.common/3.capability-requirements/00-capability-requirements.md)**（JSON-first: AGN catalog ノード）。EPIC / CAP 未接続の Feature を優先度キューに入れない（A02 Step 0）。
> **正本関係**: 実装順の概念的根拠（不可逆性の低い順①〜⑪）は [`../1.concept/03-approach.md`](../1.concept/03-approach.md) が所有する。本フォルダはそれを**優先度スコアリング基準・優先度付き実装キュー**として具体化した正本であり、[`../2.sdt-design/01-development-roadmap.md`](../2.sdt-design/01-development-roadmap.md)（設計 view）は本フォルダに追随する。矛盾したら Concept（03-approach）を正とし HIL へ。

## 構成

| # | ファイル | 役割 | 品質バー（Done の定義） |
|---|---|---|---|
| 01 | [`01-implementation-priority.md`](01-implementation-priority.md) | **実装優先度の正本** — ADF パス接続（§0）・優先度判定基準（5軸）・Feature 優先度マトリクス（EPIC / CAP(FR) / satisfies 付き）・P0〜P3 の優先度付き実装キュー・見直し条件 | 全 Feature に EPIC / CAP 接続・優先度・根拠・前提 Gate が付与され、判定基準が決定論的に再適用可能であること |
| 02 | [`02-epic-cap-priority-roadmap.md`](02-epic-cap-priority-roadmap.md) | **EPIC / CAP 優先度とロードマップ** — EPIC 6 の投資順序（E-P0〜P3・完了条件付き）・CAP 8 の成熟ロードマップ（M0〜M3）・EPIC×CAP×Feature 統合時間軸（t1/t2/t3 + 昇格条件） | 全 EPIC に完了条件、全 CAP に成熟度目標が付与され、時間軸の昇格条件が Gate として明示されていること |
| 03 | [`03-screen-roadmap.md`](03-screen-roadmap.md) | **画面ロードマップの正本** — OPS（ネットワーク管理 L1/L2/L3・環境設定・Agent 実行管理/Kill Switch）/ LOOP（Catalog・Run・Eval）/ DOMAIN（運用ループ①〜⑥対応）のカテゴリー構成と実装順 | 全画面が所有 Feature・運用ループステップ・優先度へ接続され、ED15/ED16 の作成先（所有 Feature の A02）が明示されていること |

## 本フォルダが所有するもの / しないもの

| 所有する | 所有しない（正本の所在） |
|---|---|
| 実装優先度の判定基準（スコアリング軸） | 実装順の概念的原理（不可逆性の低い順） → `../1.concept/03-approach.md` |
| Feature 単位の優先度マトリクスと実装キュー | **EPIC / CAP / FR の定義** → `../4.common/3.capability-requirements/`（JSON-first: AGN catalog ノード） |
| 優先度の見直し条件（トリガ） | Feature の要件詳細 → 各 A02（`../98.dodoai-custom-spec/`） |
| — | Stage 昇格の HIL 条件 → CR-2.5（`../4.common/0.common-requirements/00-common-requirements.md`） |
| — | Feature → 本体/カスタム分担 → `../2.sdt-design/01-development-roadmap.md` |

## 規律

- 優先度の変更は**本フォルダの正本を先に更新**し、`2.sdt-design/01-development-roadmap.md` を同一変更で追随させる（片側のみの更新禁止）
- 優先度は「期待収益の大きさ」ではなく、Concept の**大原則（生存制約下での幾何平均成長 + Optionality 最大化）と不可逆性の低い順**から導出する。これに反する優先度変更は HIL 必須
- 新 Feature の追加・優先度の再裁定は **A02 Step 0（所有 EPIC / CAP を [`../4.common/3.capability-requirements/`](../4.common/3.capability-requirements/00-capability-requirements.md) catalog で確認）** と HIL を先行させる。EPIC / CAP / FR の新設・変更も HIL 裁定必須

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.4.0 | 2026-08-22 | 03-screen-roadmap.md（OPS / LOOP / DOMAIN 画面ロードマップ正本）を新設し索引へ追加 |
| v0.3.0 | 2026-08-22 | 02-epic-cap-priority-roadmap.md（EPIC 6 / CAP 8 の優先度・成熟ロードマップ・統合時間軸）を新設し索引へ追加 |
| v0.2.0 | 2026-08-22 | ADF パス接続: EPIC / CAP / FR カタログ（4.common/3.capability-requirements — JSON-first）を正本参照へ追加。所有境界・A02 Step 0 の参照先を更新。旧 `1.concept/2.strategy` / `3.common` 表記のパスを現配置（`3.strategy` / `4.common`）へ修正 |
| v0.1.0 | 2026-08-22 | 新設。Concept 配下に戦略層（実装優先度の正本）を定義 |
