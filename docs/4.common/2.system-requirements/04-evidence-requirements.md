---
type: common-requirement
title: SR-EVD — Evidence・記録要件（Evidence by Default）
tags: [common, system-requirement, evidence, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-4（判断根拠と投資知の蓄積） |
| 入力正本 | CR-4（[`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)）/ [`07-why-not-simple.md`](../../1.concept/07-why-not-simple.md) §3.1（Calibration） |

# SR-EVD — Evidence・記録要件（Evidence by Default）

全ての判断・実行・リスク判定は Evidence を必須とし、Evidence Ledger は**追記のみ**（改変・削除禁止）で運用する。Evidence は監査ログではなく、予測校正（IG）と Counterfactual 測定の一次データである。

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| SR-EVD-1 | HARD | 全ての判断・実行・リスク判定は Evidence（Intervention と Observation の対 ＋ Source 参照 ＋ 使用 Agent・モデル・戦略バージョン）を必須とする | Evidence 参照なしの Execution / Opportunity 評価 / RiskSignal 判定 = 0 |
| SR-EVD-2 | HARD | Evidence Ledger は追記のみとする。既存 Evidence の改変・削除を禁止する（append-only） | Evidence の UPDATE / DELETE 操作 = 0（正規経路の追記のみ） |
| SR-EVD-3 | HARD | Fact / Belief / Hypothesis を分離して記録する。SNS 等の低信頼 Source を Fact として扱わない。State に LLM 推定値・自己申告を書かない（WM-3） | 記録の確度区分が 100% 付与され、Source 信頼度階層と整合 |
| SR-EVD-4 | HARD | 予測を伴う Evidence は予測分布を記録し、事後に forecast error と counterfactual_return を追記する（IG の測定単位） | 予測 Evidence の事後追記率を測定・報告できる |
| SR-EVD-5 | SOFT | 税務要件（取得価格・取引理由）を Evidence が兼ねられる形式で記録する | Position の取得価格・取引理由が Evidence 参照から復元できる |
| SR-EVD-6 | SOFT | Source の信頼度スコアは supports / contradicts の的中実績により更新し、更新履歴を残す | Source 信頼度の更新が実績データに基づいて追跡できる |

## Evidence の最小スキーマ（規範）

```yaml
evidence:
  intervention: <実行・判断の内容と参照>       # 必須
  observation: <結果>                          # 実行完了後に必須（対で記録）
  sources: [<Source 参照＋信頼度階層>]          # 必須
  actor: {agent, model, strategy_version}      # 必須
  forecast: {distribution, calibration}        # 予測を伴う場合必須
  outcome: {forecast_error, counterfactual_return}  # 事後追記
  tax: {acquisition_price, reason_ref}         # 取引の場合
```

## 禁止事項（HARD）

- Evidence の改変・削除（SR-EVD-2）
- Fact / Belief / Hypothesis の混在記録、低信頼 Source の Fact 昇格（SR-EVD-3）
- Evidence なしの判断・実行の SoT への書き込み（SR-EVD-1）

## トレーサビリティ

| 上位 | 本 SR | 関連 |
|---|---|---|
| BR-4 / CR-4.1〜4.4 | SR-EVD-1〜6 | SR-EXE-6（Intervention/Observation 対）/ SR-VIA（増分利益測定）/ NFR-SEC（改ざん不能な監査線） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-4 を検証可能な SR-EVD-1〜6 へ展開。07 §3.1 の校正フィールドを最小スキーマとして規範化 |
