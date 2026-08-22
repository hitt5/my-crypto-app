---
type: design
title: 開発ロードマップ（Concept 準拠・不可逆性順）と DODO 本体/カスタム分担
tags: [crypto-wealth-os, roadmap, design, personal-scope]
---

# 01 — 開発ロードマップ（Concept 準拠）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **正本関係**: 実装順の正本は [`../1.concept/03-approach.md`](../1.concept/03-approach.md)（不可逆性の低い順①〜⑪・ステップ S1〜S7）。同ファイル v0.5.0 で全体フローは **OODA×WF 実行モデル**（運用ループの WF 写像・評価成果物の SDT+MD 双対 HARD 原則）へ改訂済み — 各 Feature の観測/評価系はこの WF 写像と双対原則に準拠すること。本書はそれを **Feature 系列 + 本体/カスタム分担**へ写像した設計 view。**実装優先度（5軸判定基準・P0〜P4 キュー）の正本は [`../1.concept/2.strategy/01-implementation-priority.md`](../1.concept/2.strategy/01-implementation-priority.md)** — 本書 §2 の Feature 順は同書の優先度に追随する。矛盾したら Concept を正とし HIL へ。
> **Product Form**: single-owner / local-first のパーソナル dodo Custom App（CR-8）。Stage 1 Observe を完成させるまで実行系（署名・取引）には触れない。
> **同フォルダの正本**: SDT データモデル = [`02-data-model.md`](02-data-model.md)（1.concept/04 から移設）/ SCO 方針（語彙の正準化） = [`03-sco-policy.md`](03-sco-policy.md)。

## 1. 現在地

| 項目 | 状態 |
|---|---|
| Concept（1.concept 00〜07） | ✅ 記入済（v0.5 根本改訂・**H1 再承認待ち**） |
| 共通要件（3.common BR/SR/NFR） | ✅ 展開済 |
| `F-WORKSPACE-BOOTSTRAP` | running（catalog / roadmap SoT 未初期化 — 既知負債） |
| `F-CRYPTO-PORTFOLIO-DASHBOARD`（実装順①） | running（Observe MVP 実装済・pytest 16 passed・live dispatch / 実値設定が残） |
| 実装順②以降 | 未着手 |

## 2. Feature ロードマップ（実装順 = 不可逆性の低い順）

Concept `03-approach.md` の実装順①〜⑪を Feature 系列へ写像する。**着手順は上から**（優先度 P0〜P4 の正本 = [`../1.concept/2.strategy/01-implementation-priority.md`](../1.concept/2.strategy/01-implementation-priority.md)）。各 Feature の着手時に A02（6 層要件セット）→ A03 → DD01–03 の正規フローを踏む。

| 順 | Concept 実装順 | Feature（候補 ID） | Stage | 優先度 | 概要 | 前提 |
|---|---|---|---|---|---|---|
| 1 | ① 資産・ポジション統合表示 | `F-CRYPTO-PORTFOLIO-DASHBOARD` | Observe | P0 | Wallet 残高・Position の Fact 化、複数ソース価格照合、dashboard（**着手済**） | — |
| 2 | S1 Viability 正本 | `F-VIABILITY-POLICY-CORE` | Observe | P0 | ViabilityConstraint（ε・総損失限度・流動性準備率）・Policy（投資憲法）・Wallet 役割（Vault/Earn/Explore/Trade）・RiskBudget・Ω 初期棚卸しを**機械検査可能な正本**として定義し、①に DRIFTED（正本 vs 実態乖離）表示を追加 | H1 再承認 + H2（正本値の HIL 確定） |
| 3 | ② 境界変数・Constraint Graph 観測 | `F-WORLD-MODEL-OBSERVE` | Observe | P1 | BoundaryVariable（Unlock・Stablecoin 供給・金利等、観測容易なものから）・ConstraintNode・Source 信頼度階層の観測 Action 群 + 観測ページ | H1 再承認 |
| 4 | ③ Opportunity 生成・Convexity 評価 | `F-OPPORTUNITY-ENGINE` | Observe | P1 | W.M.×V.M. 差分からの Opportunity 機械生成、Convexity 評価（分布×損益×不可逆性）、No-action Counterfactual 比較、`derives_from` 必須 | 2・3 |
| 5 | ④ RiskSignal 検知（Guardian） | `F-GUARDIAN-RISKSIGNAL` | Observe | P1 | 決定論的閾値の RiskSignal 検知・不可逆性レベル付与・通知（停止フローの実行系接続は後段） | 2・3 |
| 6 | ⑤ Airdrop / Claim / 期限管理 | `F-AIRDROP-CLAIM-TRACKER` | Observe | P2 | Eligibility 構造化・期限管理・Claim 検知（実行なし） | 4 |
| 7 | ⑥ Lending / Staking 比較 | `F-YIELD-COMPARE` | Observe | P2 | 期待純収益（コスト込み）比較・表面 APY 比較禁止 | 4 |
| 8 | ⑦ 人間承認つき実行 | `F-EXECUTION-APPROVE` | **Approve** | P3 | CR-3 固定パイプライン + 全 Gate + HIL 全件承認。dodo-wallet / Session Key 統合 | **H4 + Stage 昇格 HIL**（CR-2.5） |
| 9 | ⑧〜⑪ 限定自律〜トレーディング | （後日 A02） | Autopilot | P4（凍結） | Canary Gate 経由でのみ昇格 | Stage 3 昇格 HIL |

**規律**:

- Stage 昇格（Observe→Approve→Autopilot）は HIL 承認必須（CR-2.5）。順 8 以降は本ロードマップの再裁定なしに着手しない。
- 「Swap 実行」「Yield 最適化」単体を主価値とする Feature を新設しない（07-why-not-simple §6）。
- 新 Feature の A02 Step 0 で所有 EPIC / CAP を catalog に定義する（現状 catalog 未初期化 — `F-WORKSPACE-BOOTSTRAP` の解消が全 Feature の共通負債）。
- **評価系成果物（Convexity 評価・校正・Gate 判定等）は SDT(JSON)+MD の双対で設計する**（Concept 03 §評価成果物の双対表現 — HARD）。運用ループは標準 WF（`workflow.catalog_upsert` 登録）として実装し、アドホック実行を定常運転にしない。標準 WF カタログの初期化は `F-WORKSPACE-BOOTSTRAP` の解消範囲に含める。
- 優先度（P0〜P4）の変更は `1.concept/2.strategy/01-implementation-priority.md` を先に更新し、本書を同一変更で追随させる（片側のみの更新禁止）。

## 3. DODO 本体 vs 本プロジェクト（カスタム）の実装分担

根拠: [`../1.concept/07-why-not-simple.md`](../1.concept/07-why-not-simple.md) §4（役割分担）・[`../1.concept/02-why-dodoai.md`](../1.concept/02-why-dodoai.md)（dodo Core MCP）。

> **境界原則: 「統治の機構」= DODO 本体 / 「統治の中身（ドメインルール・データ）」= 本プロジェクトのカスタム。**

### 3.1 DODO 本体が持つもの（本プロジェクトでは作らない）

| 領域 | 具体 | 本プロジェクトからの使い方 |
|---|---|---|
| SDT 基盤 | グラフ格納・Fact/Belief/Hypothesis 統治・`sdt.semantic_search` / `sdt.khop_traverse` 等 | 3 空間のノード・エッジは SDT Action 経由で読み書き。グラフエンジンは作らない |
| MCP / Action Registry | `dodo_action_dispatch`・risk_level 統治・スキーマ検証 | Custom Action の実行口 |
| Gate / HIL 実行機構 | staging approve・completion gate・Capability Routing・承認 UI | Gate の**検査ルール（中身）**だけカスタムで定義し、実行機構は本体に委ねる |
| クレデンシャル統治 | `env://` 間接参照・DID/VC・Desktop 内署名 | RPC/API キー・鍵参照を全て載せる（CR-1.2） |
| **dodo-wallet** | Signer・鍵管理・Session Key 発行/失効・Policy Enforcement（CR-1 二層の基本層） | 本体側開発物。本プロジェクトは Approve 段階（順 8）で呼び出す側 |
| Agent / Skill / Operation 機構 | Agent 定義ロード・`agent.context_pack`・Multi-Agent 実行 | 05 の 14 Agent は定義のみカスタム |
| Evidence 基盤 | 追記のみ Ledger・Intervention/Observation 対の記録機構 | 記録**スキーマ**（forecast_error・counterfactual_return 等）はカスタム |
| Personal UI 機構 | Custom UI manifest レンダリング・`custom_ui.manifest_lint` | ページは manifest 定義のみ |

### 3.2 本プロジェクト（personal scope カスタム）が実装するもの

| 領域 | 具体 | 置き場 |
|---|---|---|
| ドメイン Custom Action | snapshot / price_tick / valuation（済）、境界変数観測・Constraint 観測・DRIFTED 検知・Convexity 評価・ruin 距離算出（今後） | `.dodoai/personal/custom_actions/` |
| Custom UI | dashboard（済）、wallets / ticks / world-model / opportunities ページ（今後） | `.dodoai/personal/custom_ui/crypto-wealth/` |
| ドメイン語彙・写像 | ノード型（BoundaryVariable・ConstraintNode・Opportunity 等）・α/β/ε・不可逆性レベル・Wallet 役割・Convexity 式・Fractional Kelly 係数 | `mappings/crypto.mapping.json` + SDT catalog |
| Policy / Viability 正本データ | 投資憲法 JSON・生存制約・目標配分・Allowlist（**実値は Git 非共有**） | `.dodoai/personal/config/` |
| Gate 検査ルール | Viability / Irreversibility / No-action Counterfactual / Sizing / Crowding 等 15 Gate の決定論的判定ロジック | Custom Action として実装し本体 Gate 機構へ接続 |
| Agent 定義 | World Model / Constraint / Crowding / Viability / Guardian 等 14 Agent の役割・Skill | `docs/99.sdt/agn/2.agents/` |
| 外部 Venue 統合 | 価格ソース・RPC・（将来）Adapter 呼び出しの配線 | Custom Action |

### 3.3 どちらも作らないもの（外部委任 — 07 §4.2）

- DEX Routing / Bridge Routing / Lending calldata / LP 構築 / Perp 注文（実行の配管）
- Smart Account 基盤コントラクト（Safe 等）・一般的な Wallet UI

ただし **Signer・鍵管理・Session Key 統治・Policy Enforcement は外部委任しない**（dodo-wallet + dodo クレデンシャル機構が持つ — CR-1）。

### 3.4 迷ったときの判定手順

1. それは「統治の機構」か「ドメインルール」か → 機構なら本体、ルールならカスタム
2. 鍵・署名・権限失効に触れるか → 触れるなら必ず本体（dodo-wallet + クレデンシャル機構）。カスタム側に署名経路を作らない（Key Gate）
3. チェーン実行の配管か → 外部委任（Adapter 経由）
4. 本体機構に不足があるか → カスタムで代替実装せず、**dodoAI 本体への還流課題**として起票（07 §5.3）

## 4. 直近のアクション（順序）

> 正本: [`../1.concept/2.strategy/01-implementation-priority.md`](../1.concept/2.strategy/01-implementation-priority.md) §3 の P0 キュー。

1. `F-CRYPTO-PORTFOLIO-DASHBOARD` の完了: portfolio.json 実値設定（HIL・ユーザー作業）→ live dispatch / manifest_lint → Issue close（P0-1）
2. `F-WORKSPACE-BOOTSTRAP` の catalog / roadmap SoT 初期化（TaskGraph 負債の解消 — 全 Feature 共通の前提）（P0-2）
3. H1（Concept v0.5 再承認）の HIL（P0-3）
4. `F-VIABILITY-POLICY-CORE` の A02 着手（→ [`../98.dodoai-custom-spec/F-VIABILITY-POLICY-CORE/00-spec.md`](../98.dodoai-custom-spec/F-VIABILITY-POLICY-CORE/00-spec.md)）（P0-4）
5. `F-WORLD-MODEL-OBSERVE` の A02 着手（P1-1）

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.1 | 2026-08-22 | 同フォルダに `02-data-model.md`（1.concept/04 から移設）・`03-sco-policy.md`（SCO 方針）を新設したことを反映（ヘッダへ正本参照を追加） |
| v0.2.0 | 2026-08-22 | 実装優先度の正本を `1.concept/2.strategy/01-implementation-priority.md` へ新設したことに追随: §2 に優先度列（P0〜P4）を追加、§4 を P0 キュー参照へ接続、片側更新禁止の規律を追加 |
| v0.1.1 | 2026-08-22 | Concept 03-approach v0.5.0（OODA×WF 実行モデル・評価 SDT+MD 双対 HARD）へ追随。規律へ双対原則・標準 WF 登録を追加 |
| v0.1.0 | 2026-08-22 | 初版。Concept 03-approach の実装順を Feature 系列へ写像し、DODO 本体/カスタム分担（境界原則・判定手順）を正本化 |
