---
type: common-requirement
title: EPIC / CAP / FR カタログ（認知 view — JSON-first SoT の対）
tags: [common, requirements, epic, cap, fr, adf, crypto-wealth-os]
---

# EPIC / CAP / FR カタログ — Capability Requirements

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **正本関係（JSON-first）**: 本書は **AGN catalog ノードの認知 view** である。機械可読 SoT は次の 2 ノード（`agn.node_upsert` 経由で読み書き — SDT JSON 直読み・直編集禁止）:
> - EPIC catalog: `ln://agn/epic-catalog-crypto-wealth-os/task-epic-catalog-crypto-wealth-os`
> - CAP/FR catalog: `ln://agn/cap-catalog-crypto-wealth-os/task-cap-catalog-crypto-wealth-os`
>
> **HIL 裁定**: 2026-08-22 — EPIC 6 + CAP 8 + FR セット + `impl_provenance`（dodoAI 本体実装参照 Index）方式をユーザー承認。**EPIC / CAP / FR の新設・変更は HIL 裁定必須**（AGENTS.md §Requirements Model）。
> **ADF パス**: 縦糸 `BR → SR → UC（各 Feature A02）→ Evidence` ⟷ 横糸 `CAP ─owns→ FR → Mod`。**FR は CAP が所有**し、Feature / UC は `satisfies` で参照のみ（正本: dodoAI Charter `07-requirements-architecture-map.md` 同型）。

## 1. impl_provenance（本体実装参照 Index の凡例）

本カタログは新規定義であると同時に、**dodoAI 本体（`/Users/hitoshimurakami/myApps/dodoai`）実装への参照 Index** を兼ねる。各 CAP / FR は `impl_provenance` を持つ:

| provenance | 意味 | 規律 |
|---|---|---|
| `dodoai-core` | dodoAI 本体の既存実装を参照のみ | 本プロジェクトで**再実装禁止**。不足は還流課題として起票（roadmap §3.4） |
| `dodoai-core+custom-rules` | 機構は本体、検査ルール・スキーマ・語彙のみ本プロジェクトが定義 | FR は「本体機構 X に検査ルール Y を接続する」形で実装 |
| `custom` | 本プロジェクトの personal scope 実装 | `.dodoai/personal/custom_actions/` / `custom_ui/` に実装 |

**参照先実在確認（2026-08-22）**: 本体 `docs/2.common/` の grep + `F-WALLET-CORE` feature.json 実在確認により、`CAP-EVIDENCE-LEDGER` / `CAP-POLICY-SECURITY` / `CAP-IDENTITY-ACCESS` / `CAP-ACTION-EXECUTION` / `CAP-SDT-STORE` / `CAP-SDT-GOVERNANCE` / `CAP-WORKFLOW-ORCHESTRATION` / `F-WALLET-CORE`（sovereign-wallet）の実在を確認済み。本体側の実装詳細は転記しない（drift 防止 — 参照 ID のみ保持）。

## 2. EPIC カタログ（縦糸 — 6 EPIC）

| EPIC | 名称 | 所属 Feature | satisfies BR | 導出根拠 |
|---|---|---|---|---|
| `EPIC-FOUNDATION` | ワークスペース基盤 | `F-WORKSPACE-BOOTSTRAP` | — | catalog / roadmap SoT・標準 WF カタログ等の開発基盤 |
| `EPIC-VIABILITY` | 生存・統治正本 | `F-VIABILITY-POLICY-CORE`, `F-CRYPTO-PORTFOLIO-DASHBOARD` | BR-1, BR-7 | 三要素② / 04 Viability 空間。DRIFTED 監視を含む |
| `EPIC-WORLD-MODEL` | 世界モデル観測 | `F-WORLD-MODEL-OBSERVE` | BR-4 | 三要素① / 04 World Model 空間。H-2 / H-4 検証面 |
| `EPIC-OPPORTUNITY` | 機会生成・評価 | `F-OPPORTUNITY-ENGINE`, `F-AIRDROP-CLAIM-TRACKER`, `F-YIELD-COMPARE` | BR-1, BR-4 | 04 Intervention 空間前半。Convexity / Counterfactual（H-3） |
| `EPIC-GUARDIAN` | リスク検知・退避 | `F-GUARDIAN-RISKSIGNAL` | BR-3, BR-6 | CR-5.6 停止フロー。Viability と Settlement に交差するため独立（HIL 裁定） |
| `EPIC-SETTLEMENT` | 実行・承認 | `F-EXECUTION-APPROVE`（⑧〜⑪は P4 凍結） | BR-2, BR-3, BR-5 | 三要素③。CR-1 / CR-3・dodo-wallet 統合・Stage 2/3 |

## 3. CAP カタログ（横糸 — 8 CAP と所有 FR）

### CAP-ONCHAIN-OBSERVE — オンチェーン・市場観測（`custom`）

> core_ref: `CAP-SDT-STORE`, `CAP-ACTION-EXECUTION`（SDT 書込・Action Registry は本体機構） / 利用 Feature: DASHBOARD, WORLD-MODEL-OBSERVE, GUARDIAN

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-OBS-1 | Wallet 残高・Position・Approval のオンチェーン実測（Fact 化、複数 RPC） | SR-VIA / 04:Position | custom |
| FR-OBS-2 | 複数価格ソース照合（単一オラクル禁止） | CR-3.3 / SR-EXE | custom |
| FR-OBS-3 | BoundaryVariable の定期観測と分布更新（単一点推定禁止） | 04:BoundaryVariable / WM-3 | custom |
| FR-OBS-4 | ConstraintNode 観測（観測可能性等級 direct/proxy/structural-prior 付与） | 04:ConstraintNode / H-2 | custom |
| FR-OBS-5 | Source 信頼度階層の管理と的中実績による更新 | 04:Source / CR-4.3 | custom |

### CAP-VIABILITY-EVAL — 生存制約評価（`custom`）

> 利用 Feature: VIABILITY-CORE, DASHBOARD, OPPORTUNITY

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-VIA-1 | ViabilityConstraint（ε・総損失限度・最低流動性準備率・不可逆性上限）の機械検査 | CR-9.1 / SR-VIA | custom |
| FR-VIA-2 | ruin 距離の実測と閾値監視 | CR-9.1 / 04:ViabilityConstraint | custom |
| FR-VIA-3 | DRIFTED 検知（正本 vs 実態の決定論的乖離判定） | 04:Wallet / タイプ E | custom |
| FR-VIA-4 | Ω（OptionalitySet）実測と ΔΩ 追跡（LLM 自己申告禁止） | CR-9.8 / WM-3 | custom |
| FR-VIA-5 | Fractional Kelly サイジング（不確実性でサイズ制限・因果相関の合算上限） | CR-9.4 / CR-9.5 | custom |

### CAP-POLICY-ENGINE — 決定論的 Policy 検査（`dodoai-core+custom-rules`）

> core_ref: `CAP-POLICY-SECURITY`, `CAP-SDT-GOVERNANCE`（Gate 実行・staging approve・Capability Routing は本体。15 Gate の判定ロジックのみ custom） / 利用 Feature: VIABILITY-CORE, EXECUTION-APPROVE, GUARDIAN

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-POL-1 | Policy 全項目の決定論的検査（LLM 最終可否禁止） | CR-2.2 / CR-2.4 | core+rules |
| FR-POL-2 | Policy 変更の HIL 限定（Agent 自己変更遮断） | CR-2.3 | core+rules |
| FR-POL-3 | Stage（Observe/Approve/Autopilot）管理と昇格 HIL | CR-2.5 | core+rules |
| FR-POL-4 | 15 Gate 検査ルールの実行（本体 Gate 機構へ接続） | 05:Gate 表 | core+rules |

### CAP-OPPORTUNITY-GEN — 差分生成・Convexity 評価（`custom`）

> 利用 Feature: OPPORTUNITY, AIRDROP, YIELD

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-OPP-1 | W.M.×V.M. 差分からの Opportunity 機械生成（`derives_from` 必須） | 04:Opportunity | custom |
| FR-OPP-2 | Convexity 評価（確率分布×損益分布×不可逆性） | CR-9.3 / H-3 | custom |
| FR-OPP-3 | No-action Counterfactual 比較（優位 3 倍未満は不実行） | CR-5.1 | custom |
| FR-OPP-4 | 期待純収益（全コスト込み）算出 — 表面 APY 単独比較の機械的拒否 | 04:Opportunity⑥ | custom |
| FR-OPP-5 | 期限管理・Eligibility 構造化・Claim 検知（Sybil 禁止） | CR-6.4 | custom |

### CAP-RISK-DETECT — RiskSignal 検知（`custom`）

> core_ref: `CAP-ACTION-EXECUTION`（通知・停止の実行機構は本体） / 利用 Feature: GUARDIAN, WORLD-MODEL-OBSERVE

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-RSK-1 | 決定論的閾値による RiskSignal 検知（閾値緩和は HIL のみ） | 04:RiskSignal | custom |
| FR-RSK-2 | 不可逆性レベル（可逆/条件付き/不可逆）付与 | CR-9.2 | custom |
| FR-RSK-3 | CrowdingSignal 観測と混雑時の再評価強制発火 | CR-9.7 / H-4 | custom |
| FR-RSK-4 | 停止フロー起動（新規停止→権限停止→Approval 解除→退避案→緊急 HIL） | CR-5.6 | custom |

### CAP-EVIDENCE-LEDGER — Evidence 記録・校正（`dodoai-core+custom-rules`）

> core_ref: 本体 `CAP-EVIDENCE-LEDGER`（追記のみ Ledger・Intervention/Observation 対の機構は本体。記録スキーマのみ custom） / 利用 Feature: 全 Feature 横断

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-EVD-1 | 追記のみ Evidence（Intervention/Observation 対・Source・Agent/モデル/戦略版） | CR-4.1 / CR-4.2 | dodoai-core |
| FR-EVD-2 | 予測校正（forecast error）・counterfactual_return の事後追記 = IG 測定 | BR-4 / 04:Evidence | core+rules |
| FR-EVD-3 | Fact / Belief / Hypothesis 分離記録 | CR-4.3 / WM-3 | dodoai-core |
| FR-EVD-4 | 税務兼用記録（取得価格・取引理由） | CR-4.4 | core+rules |
| FR-EVD-5 | 評価成果物の SDT(JSON)+MD 双対保持 | 03:双対 HARD / WM-5 | core+rules |

### CAP-KEY-CUSTODY — 鍵・権限統治（`dodoai-core` — 参照 Index のみ）

> core_ref: `CAP-IDENTITY-ACCESS`, `F-WALLET-CORE`（sovereign-wallet）。**dodo-wallet + dodo クレデンシャル機構が正本。本プロジェクトは統合 FR のみ所有し再実装禁止**（不足は還流課題として起票） / 利用 Feature: EXECUTION-APPROVE

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-KEY-1 | 二層鍵管理統合（dodo クレデンシャル + 個人 HW）。鍵の非保持 | CR-1.1 / CR-1.3 | dodoai-core |
| FR-KEY-2 | `env://` 間接参照のみ（平文遮断） | CR-1.2 | dodoai-core |
| FR-KEY-3 | Session Key 期限・失効・Kill Switch 統合 | CR-1.4 | dodoai-core |

### CAP-EXEC-PIPELINE — 実行パイプライン（`dodoai-core+custom-rules`）

> core_ref: `CAP-ACTION-EXECUTION`, `CAP-WORKFLOW-ORCHESTRATION`（パイプライン実行・Adapter 統治は本体/外部委任。Allowlist・回転数の値と検査ルールが custom） / 利用 Feature: EXECUTION-APPROVE, ⑧〜⑪（凍結）

| FR | 内容 | traces | provenance |
|---|---|---|---|
| FR-EXE-1 | CR-3 固定パイプラインの通過強制（省略・順序変更遮断） | CR-3 | core+rules |
| FR-EXE-2 | Allowlist 済み Adapter のみ（任意 calldata 遮断） | CR-3.1 / CR-3.2 | core+rules |
| FR-EXE-3 | 署名前 fork シミュレーション・乖離 Finding 記録 | CR-3.4 | custom |
| FR-EXE-4 | 回転数上限（回数・代金・ガス・スリッページ・再実行間隔） | CR-5.2 | custom |

## 4. Feature → EPIC / CAP 参照マトリクス（satisfies）

| Feature | EPIC | 主要 CAP（利用） | satisfies BR |
|---|---|---|---|
| `F-WORKSPACE-BOOTSTRAP` | EPIC-FOUNDATION | —（開発基盤） | — |
| `F-CRYPTO-PORTFOLIO-DASHBOARD` | EPIC-VIABILITY | ONCHAIN-OBSERVE, VIABILITY-EVAL, EVIDENCE-LEDGER | BR-1, BR-7 |
| `F-VIABILITY-POLICY-CORE` | EPIC-VIABILITY | VIABILITY-EVAL, POLICY-ENGINE, EVIDENCE-LEDGER | BR-1, BR-7 |
| `F-WORLD-MODEL-OBSERVE` | EPIC-WORLD-MODEL | ONCHAIN-OBSERVE, RISK-DETECT, EVIDENCE-LEDGER | BR-4 |
| `F-OPPORTUNITY-ENGINE` | EPIC-OPPORTUNITY | OPPORTUNITY-GEN, VIABILITY-EVAL, EVIDENCE-LEDGER | BR-1, BR-4 |
| `F-GUARDIAN-RISKSIGNAL` | EPIC-GUARDIAN | RISK-DETECT, ONCHAIN-OBSERVE, POLICY-ENGINE | BR-3, BR-6 |
| `F-AIRDROP-CLAIM-TRACKER` | EPIC-OPPORTUNITY | OPPORTUNITY-GEN, EVIDENCE-LEDGER | BR-4 |
| `F-YIELD-COMPARE` | EPIC-OPPORTUNITY | OPPORTUNITY-GEN, EVIDENCE-LEDGER | BR-4 |
| `F-EXECUTION-APPROVE` | EPIC-SETTLEMENT | EXEC-PIPELINE, KEY-CUSTODY, POLICY-ENGINE, EVIDENCE-LEDGER | BR-2, BR-3, BR-5 |

## 5. 規律

- **JSON-first**: 構造変更は AGN catalog ノード（`agn.node_upsert`）を先に更新し、本 MD view を同一変更で追随させる。MD だけの構造更新禁止（WM-5）
- **FR は CAP が所有** — Feature A02 は FR を新設せず `satisfies` 参照のみ。欠落 FR は `fr_gap` として記録し HIL へ
- `dodoai-core` provenance の FR を本プロジェクトで再実装しない。本体機構の不足はカスタム代替でなく**還流課題**として起票（roadmap §3.4）
- 本体側実装詳細（コード・数値・内部構成）をこちらへ転記して正本化しない — 参照 ID のみ保持

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 新設（HIL 裁定）。EPIC 6 / CAP 8 / FR 35 を JSON-first catalog（AGN ノード）+ 本 MD view の双対で定義。impl_provenance（dodoAI 本体実装参照 Index）を導入 |
