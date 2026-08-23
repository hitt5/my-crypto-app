---
type: common-requirement
title: SR-POL — 権限統治要件（Policy-Custodied Autonomy）
tags: [common, system-requirement, policy, governance, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-1（生存制約下の資産統治） |
| 入力正本 | CR-2（[`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)）/ [`05-multi-agent.md`](../../1.concept/05-multi-agent.md)（Gate 定義） |

# SR-POL — 権限統治要件（Policy-Custodied Autonomy）

全実行はユーザーが定義した Policy（投資憲法）に拘束され、最終可否は LLM ではなく**決定論的な Policy Engine** が判断する。

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| SR-POL-1 | HARD | 全実行はいずれかの Policy（投資憲法）に拘束される。Policy 非拘束の実行経路を作らない | 全 Execution ノードが `governs` エッジで Policy に接続されている（孤立 Execution = 0） |
| SR-POL-2 | HARD | Policy の項目（金額上限・Allowlist・スリッページ・レバレッジ禁止・損失限度・回転数上限・失効期限・承認閾値・不可逆性上限）は決定論的に検査可能な形式で定義する | 全 Policy 項目が機械検査可能（LLM 判定に依存する Policy 項目 = 0） |
| SR-POL-3 | HARD | **Agent 自身に権限上限・Policy を変更させない**。Policy / ViabilityConstraint の変更は HIL のみとする | Policy 変更操作の承認者記録が 100% 人間（＋SR-KEY-3 の物理署名） |
| SR-POL-4 | HARD | 最終可否は決定論的な Policy Engine が判断する。複数 Agent の多数決・LLM の確信度ベースの最終判定を禁止する | 実行可否の判定ログが決定論的検査結果のみで構成される |
| SR-POL-5 | HARD | 自律度は Observe → Approve → Autopilot の 3 段階のみとし、段階昇格は HIL 承認必須とする | 段階昇格の Evidence に HIL 承認が 100% 付随 |
| SR-POL-6 | HARD | Policy は必ず有効期限を持つ。失効期限到来・損失限度到達・Guardian の停止発動で Policy は失効し、失効中の実行は全リジェクトする | 有効期限なし Policy = 0。失効中の実行受理 = 0 |
| SR-POL-7 | SOFT | Gate 検査（Viability / Irreversibility / No-action Counterfactual / Sizing / Crowding / Policy / Key / Simulation / 回転数 / Canary / HIL / Risk — 05-multi-agent.md §Gate）の検査結果は実行案ごとに記録する | 実行案の Evidence に Gate 検査結果が付随 |

## 自律度段階（正本）

| 段階 | 実行 | HIL の範囲 |
|---|---|---|
| Stage 1 Observe | 分析と提案のみ（実行しない） | — |
| Stage 2 Approve | 人間承認後に執行 | 全取引 |
| Stage 3 Autopilot | Policy・回転数・Canary・不可逆性上限の枠内で自律執行 | 閾値超過取引・不可逆 Action・緊急退避 |

## 禁止事項（HARD）

- Policy 非拘束の実行経路の新設（SR-POL-1）
- Agent 自身による Policy / 権限上限 / 閾値の変更・緩和（SR-POL-3）
- LLM / 多数決 / 確信度による最終可否判定（SR-POL-4）
- HIL を経ない自律度昇格（SR-POL-5）

## トレーサビリティ

| 上位 | 本 SR | 関連 |
|---|---|---|
| BR-1 / CR-2.1〜2.5 | SR-POL-1〜7 | SR-VIA（生存制約検査）/ SR-EXE（パイプライン内 Policy 検査）/ SR-KEY（権限の物理面） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-2 を検証可能な SR-POL-1〜7 へ展開。自律度 3 段階を正本化 |
