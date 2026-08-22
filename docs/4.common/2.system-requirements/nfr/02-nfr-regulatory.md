---
type: common-requirement
title: NFR-REG — 規制適合非機能要件（Regulatory Posture）
tags: [common, nfr, regulatory, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-5（規制適合姿勢の維持） |
| 入力正本 | CR-7（[`../../0.common-requirements/00-common-requirements.md`](../../0.common-requirements/00-common-requirements.md)） |

# NFR-REG — 規制適合非機能要件（Regulatory Posture）

本システムは金融庁の暗号資産制度移行期（2026 — 暗号資産を金商法上の金融商品として扱う方向の WG 議論）を前提に、**「ユーザー（自己勘定）が定義したルールの機械的実行を支援するソフトウェア」** の範囲に留まる設計を採る。

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| NFR-REG-1 | HARD | 初期スコープは「ユーザー（自己勘定）が定義したルールの機械的実行を支援するソフトウェア」の範囲に留める。第三者資産の運用・預託・媒介に該当する機能を実装しない | 機能一覧のレビューで該当機能 = 0（NFR-SCOPE と整合） |
| NFR-REG-2 | HARD | 実行前承認（Approve 段階）を標準設定とする。Autopilot はユーザーの明示的な段階昇格（HIL — SR-POL-5）によってのみ有効化される | 初期設定が Approve 段階であることの検証。既定 Autopilot = 0 |
| NFR-REG-3 | HARD | 個別銘柄推奨・有料継続助言・成果報酬・不透明なルーティング報酬に該当し得る機能は HIL 裁定なしに実装しない | 該当し得る機能の実装前に HIL 記録が存在する |
| NFR-REG-4 | SOFT | 金融庁の暗号資産制度動向（2026 制度移行期）を World Model の観測対象（BoundaryVariable「規制による行動制約」）に含め、変化を検知したら Concept / 要件セットの再評価を発火する | 規制動向の観測ソースが登録され、観測記録が残る |
| NFR-REG-5 | SOFT | 税務要件（取得価格・取引理由の記録 — SR-EVD-5）を満たす記録形式を維持し、申告に必要な情報を Evidence から復元できる | 年間取引の税務データが Evidence から生成できる |

## 補足（設計判断の根拠）

- 「実行前承認を標準」「ユーザー定義ルールの機械的実行」「自己勘定支援」という設計を最初から選ぶことで、規制適合と差別化（07-why-not-simple.md）を両立する
- 規制は Constraint Graph の自分側のノードである（01-problem.md）— 外部制約としてだけでなく、自身の行動制約として World Model に組み込む

## トレーサビリティ

| 上位 | 本 NFR | 関連 |
|---|---|---|
| BR-5 / CR-7.1〜7.4 | NFR-REG-1〜5 | SR-POL-5（段階昇格 HIL）/ SR-EVD-5（税務記録）/ NFR-SCOPE（スコープ境界） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-7 を検証可能な NFR-REG-1〜5 へ展開 |
