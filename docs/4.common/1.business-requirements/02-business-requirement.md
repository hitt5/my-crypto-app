---
type: common-requirement
title: ビジネス要件（BR-1〜BR-7）
tags: [common, business-requirement, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 入力正本 | [`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)（CR-1〜CR-9）/ [`01-business-background-goals.md`](01-business-background-goals.md) |

# ビジネス要件（BR）

本ドキュメントは、dodo Crypto Wealth OS が充足しなければならない **7 つのビジネス要件（BR）** を定義する。各 BR はビジネス背景・ゴール（01）で定義した大原則・4 仮説・ポジショニングに根拠を置き、システム要件（SR）・非機能要件（NFR）の上位制約として機能する。

dodo Crypto Wealth OS は、ユーザー本人が定義したルール（投資憲法）と生存制約のもとで AI Agent を継続稼働させるための **パーソナル資産統治基盤** である。以下の 7 要件はこの定義を実現するための必須条件として設定される。

---

## BR-1: 生存制約下の資産統治の確立

**本システムは、ユーザーが定義した生存制約（P(ruin) < ε）と投資憲法（Policy）に基づいて、全ての Agent 実行・権限・介入を機械的に統制できなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | 大原則（生存制約下での幾何平均成長 + Optionality 最大化）。損失最小化でも期待収益最大化でも破綻する（01-problem.md 課題 0）。統制はユーザー本人のルールで定義され、Agent 自身にもベンダーにも変更させない |
| **具体的に何を意味するか** | Policy 非拘束の実行経路が存在しないこと。最終可否は LLM ではなく決定論的な Policy Engine が判断すること。生存制約を毀損する介入は期待収益に関わらず不実行 |
| **スコープ** | Policy Engine、Viability / Irreversibility / Sizing / Policy Gate、Observe → Approve → Autopilot の自律度段階管理 |
| **導出先** | [SR-POL](../2.system-requirements/02-policy-governance-requirements.md) / [SR-VIA](../2.system-requirements/05-viability-risk-requirements.md) |

---

## BR-2: 鍵・権限のソブリニティ（Non-custodial）

**本システムは、秘密鍵・シードをユーザー本人の統制下に完全に置き、AI / Agent / サーバーに一切渡さない構造でなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | 鍵・権限の丸渡しは最大の不可逆リスク（ruin の具体形）。既存自動売買の API キー丸渡し構造（01-problem.md 課題 6）を構造的に排除する |
| **具体的に何を意味するか** | 鍵は dodo クレデンシャル機構（基本）＋ 個人ハードウェアモジュール（補完）の二層で保持する。Agent が持てるのは期限付き・用途限定の実行権限（Session Key / Safe Module）のみ |
| **スコープ** | 鍵の二層管理、`env://` 間接参照、Session Key 発行・失効、Kill Switch、高権限操作の物理署名 |
| **導出先** | [SR-KEY](../2.system-requirements/01-key-custody-requirements.md) / [NFR-SEC](../2.system-requirements/nfr/01-nfr-security.md) |

---

## BR-3: 安全な実行パイプラインによる継続稼働

**本システムは、全ての執行を固定された安全パイプラインに通し、24 時間の観測・期限管理・退避を人間の気づきに依存せず継続稼働できなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | オペレーショナルα（巡回・期限管理・Claim・Approval 解除）は人間には継続不能（課題 5）。危険からの退避が人間頼み（課題 7）。不可逆損失を一度回避する価値は細かいトレードの数年分より大きい（H-1） |
| **具体的に何を意味するか** | 許可済み Adapter → デコード → 複数価格ソース照合 → fork シミュレーション → Policy 検査 → 署名 → 執行 → 記録の固定パイプライン。Guardian の常駐監視と自動停止フロー |
| **スコープ** | 実行パイプライン、Allowlist、複数ソース照合、fork シミュレーション、Guardian 停止フロー（新規取引停止 → 権限停止 → Approval 解除 → 退避案 → 人間緊急承認） |
| **導出先** | [SR-EXE](../2.system-requirements/03-execution-pipeline-requirements.md) / [SR-VIA](../2.system-requirements/05-viability-risk-requirements.md) |

---

## BR-4: 検証可能な判断根拠と投資知の蓄積（Evidence / IG）

**本システムは、全ての判断・実行・リスク判定を検証可能な根拠付きで記録し、予測校正と Counterfactual 比較によって投資判断の知（IG）を蓄積できなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | 判断記録の不在は「学習しないシステム」（課題 8）。差別化の中核は予測精度ではなく確度校正（Calibration）と Counterfactual 測定（07-why-not-simple.md §3.1） |
| **具体的に何を意味するか** | Evidence Ledger は追記のみ。Intervention と Observation の対、予測分布と実績の対（forecast error）、counterfactual_return を必ず記録。Fact / Belief / Hypothesis を分離する |
| **スコープ** | Evidence Ledger、予測校正、Counterfactual 測定、Source 信頼度更新、税務記録の兼用 |
| **導出先** | [SR-EVD](../2.system-requirements/04-evidence-requirements.md) |

---

## BR-5: 規制適合姿勢の維持

**本システムは、「ユーザー（自己勘定）が定義したルールの機械的実行を支援するソフトウェア」の範囲に留まり、規制動向を観測対象として運用できなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | 金融庁の暗号資産制度移行期（2026）。助言・媒介・運用該当は事業リスク（01-problem.md 放置リスク）。実行前承認を標準とする設計は規制適合と差別化を両立する |
| **具体的に何を意味するか** | 実行前承認（Approve 段階）を標準設定とし、個別銘柄推奨・有料継続助言・成果報酬に該当し得る機能は HIL 裁定なしに実装しない |
| **スコープ** | 規制ポスチャ、実行前承認の標準化、規制動向の観測 |
| **導出先** | [NFR-REG](../2.system-requirements/nfr/02-nfr-regulatory.md) |

---

## BR-6: 敵対的環境での Agent セキュリティ

**本システムは、汚染された情報源・敵対的コントラクト・プロンプトインジェクションが常態である環境で、Agent が乗っ取られても実害に至らない多層防御を備えなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | クリプトはゼロトラストが前提の環境（00-overview.md §AI 統治の試金石）。LLM の判断は汚染され得る前提で設計する |
| **具体的に何を意味するか** | クロール取得コンテンツを命令として解釈しない。最終可否は決定論的 Gate が持つため、LLM 汚染が直接実行に接続されない。改ざん・不審トークン・Approval 異常を RiskSignal として監視 |
| **スコープ** | プロンプトインジェクション対策、入力境界防御、SBOM/MCP 統制、Sybil farming 禁止 |
| **導出先** | [NFR-SEC](../2.system-requirements/nfr/01-nfr-security.md) |

---

## BR-7: パーソナル Custom App としての最適化

**本システムは、single-owner / local-first のパーソナル dodo Custom App として、ユーザー本人の Portfolio / Policy / Wallet / Evidence に最適化されなければならない。**

| 項目 | 内容 |
|------|------|
| **根拠** | Personal Custom App Policy（AGENTS.md — HARD）。一次利用者・資産所有者・最終承認者はユーザー本人。汎用 SaaS 化は既定スコープ外 |
| **具体的に何を意味するか** | dodoAI の personal scope（`.dodoai/personal/`）で実装する。multi-user / hosted custody / 顧客アカウント / 組織承認を前提にしない。将来の外販を理由に multi-tenant 機能を先行実装しない |
| **スコープ** | パーソナルスコープ境界、local-first データ境界、スコープ拡張時の HIL 前置 |
| **導出先** | [NFR-SCOPE](../2.system-requirements/nfr/03-nfr-personal-scope.md) |

---

## BR → CR / SR / NFR トレーサビリティ

| BR | 入力 CR | 導出先 |
|---|---|---|
| BR-1 生存制約下の資産統治 | CR-2, CR-5, CR-9 | SR-POL / SR-VIA |
| BR-2 鍵・権限のソブリニティ | CR-1 | SR-KEY / NFR-SEC |
| BR-3 安全な実行パイプライン | CR-3, CR-5.6 | SR-EXE / SR-VIA |
| BR-4 判断根拠と投資知の蓄積 | CR-4 | SR-EVD |
| BR-5 規制適合姿勢 | CR-7 | NFR-REG |
| BR-6 Agent セキュリティ | CR-6 | NFR-SEC |
| BR-7 パーソナル Custom App | CR-8 | NFR-SCOPE |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。Concept CR-1〜CR-9 と 4 仮説から BR-1〜BR-7 を定義（HIL: 本タスクのユーザー指示による） |
