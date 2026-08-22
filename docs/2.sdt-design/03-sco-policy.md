---
type: design
title: SCO 方針（語彙の正準化 — Core SCO 写像 + Domain SCO Package）
tags: [crypto-wealth-os, sco, ontology, sdt-design, personal-scope]
---

# 03 — SCO 方針（Semantic Canonical Ontology）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: [`02-data-model.md`](02-data-model.md) が定義したノード型・エッジ型・固有語彙を、**SDT の実ノード型・機械可読語彙としてどう正準化するか**の方針正本。dodoAI 本体の 2 層 SCO 機構（Core SCO + Domain SCO Package + STM mapping）に準拠する。
> **本体側の正本**: Domain SCO Package の meta-schema・検証 Action は dodoAI 本体（`F-SDT-SCO-DOMAIN-PKG`、schema: `domain-sco-package-schema-v1.0`）が所有する。本書はその**利用方針（crypto profile での中身）**のみを所有し、機構を再定義しない（境界原則 — [`01-development-roadmap.md`](01-development-roadmap.md) §3）。

## 1. 基本方針 — 2 層 SCO + STM mapping

本プロジェクトの語彙は次の 3 経路で機械可読化する。**shadow ontology（SCO を経由しない独自ノード型の新設）は禁止**。

```text
02-data-model.md（人間可読の定義 SoT）
        |
        +-- ① STM mapping ------------> Core SCO C:*（承認済みの広い概念へ写像）
        |      mappings/crypto.mapping.json
        |
        +-- ② Domain SCO Package -----> DC:* draft（crypto 固有の狭い正準概念候補）
        |      crypto-wealth-sco-package（extends: Core SCO）
        |
        +-- ③ 固有値（式・係数・enum）--> mapping の値域として吸収（概念化しない）
```

| 層 | 名前空間 | 所有 | 変更可否 |
|---|---|---|---|
| Core SCO | `C:*` | dodoAI 本体（`sdt-canonical-ontology-v1.0`・凍結） | ❌ 本プロジェクトから変更・重複定義しない |
| Domain SCO Package | `DC:*` | 本プロジェクト（`crypto-wealth-sco-package`、`extends` = Core SCO） | ✅ `draft` 起案は Agent 可 / `frozen` 昇格は HIL のみ |
| STM mapping | — | 本プロジェクト（`mappings/crypto.mapping.json`） | ✅ 写像先は Core SCO canonical または frozen DC のみ |

## 2. 経路の判定基準

| 判定 | 経路 | 例 |
|---|---|---|
| Core に同じ意味の概念がある | ① 直接写像（新 `DC:*` を作らない） | Evidence → `C:Evidence` / Execution → `C:Intervention` / Source → `C:Source` 系 / Policy → `C:GovernanceRule` 系 |
| Core より狭い不変条件を持つ複合概念 | ② Core anchor 付き `DC:*` 候補 | BoundaryVariable / ConstraintNode / CrowdingSignal / ViabilityConstraint / OptionalitySet / Opportunity / RiskBudget / StrategyVersion |
| 概念ではなく値・式・enum | ③ mapping の値域 | α・β・ε、不可逆性レベル（可逆/条件付き可逆/不可逆）、Wallet 役割（Vault/Earn/Explore/Trade）、観測可能性等級（direct/proxy/structural-prior）、Convexity 評価式、Fractional Kelly 係数、Canary 段階、信頼度階層 |

### 2.1 02-data-model ノード型の初期写像方針（起案時に精査）

| 02 のノード型 | 想定経路 | broad Core anchor（候補） | World Model 十要素 |
|---|---|---|---|
| BoundaryVariable | ② `DC:BoundaryVariable` | `C:State` / `C:Entity` | State |
| ConstraintNode | ② `DC:MarketConstraint` | `C:Constraint` | Constraint |
| CrowdingSignal | ② `DC:CrowdingSignal` | `C:Observation` | Observation |
| Protocol | ② `DC:ExternalProtocol` | `C:Entity` | Entity |
| RiskSignal | ② `DC:IrreversibilityRiskSignal` | `C:Observation` | Observation |
| Source | ① → `C:Source` 系（信頼度階層は mapping 値域） | — | — |
| ViabilityConstraint | ② `DC:ViabilityConstraint` | `C:Constraint` | Constraint |
| OptionalitySet | ② `DC:OptionalitySet` | `C:State` | State |
| Wallet / Asset / Position | ② `DC:RoleSeparatedWallet` 等 | `C:Entity` / `C:State` | Entity / State |
| Policy | ① broad は `C:GovernanceRule`、狭い不変条件は ② `DC:InvestmentConstitution` | `C:GovernanceRule` | Constraint |
| RiskBudget | ② `DC:RuinBudget` | `C:Constraint` | Constraint |
| Opportunity | ② `DC:ConvexOpportunity` | `C:Hypothesis` | Hypothesis |
| Execution | ① → `C:Intervention`（WM-4 の Intervention/Observation 対で表現） | — | — |
| StrategyVersion | ② `DC:CanaryStrategyVersion` | `C:Contract` / `C:Workflow` | Dynamics |
| Evidence | ① → `C:Evidence` | — | — |

> 表は**起案の初期方針**であり正準決定ではない。各 `DC:*` の起案時に `sdt.search` / `sdt.semantic_search` で Core・既存 DC の重複を必ず探索し、Core に十分な概念があれば ① へ倒す（DC の乱造禁止 — エントロピー最小化 WM-2）。

## 3. Lifecycle と HIL（HARD）

| 状態 | 誰が作れるか | 使ってよい範囲 |
|---|---|---|
| `draft` | Agent が起案可（explicit intent の範囲内） | 探索・レビュー・設計参照のみ。**実 SDT ノード型・STM 写像先には使わない** |
| `frozen` | **HIL 裁定のみ**（approver / approved_at 必須） | 実 SDT ノード型・STM 写像先として使用可 |
| Core canonical | dodoAI 本体のみ | 参照のみ。Domain package から変更・重複定義しない |

- 各 `DC:*` は最低限、**定義・他概念との弁別・World Model 十要素分類（Q3 上位アンカー）・不変条件（02 の成立/見直し条件を継承）・Core anchor・定義 SoT 参照（本書 + 02-data-model）** を持つ。十要素に分類できない概念は `draft` に留めて HIL へ（WM-1）。
- `draft` → `frozen` 昇格は Feature の A02/A03 でそのノード型を**実際に使う直前**にまとめて HIL に出す（先行して全部凍結しない）。
- ノード型の意味変更（不変条件の変更を含む）は 02-data-model の改訂と**同一変更**で行う（MD+JSON 双対 — WM-5）。

## 4. 成果物の置き場と操作規律

| 成果物 | 置き場 | 操作 |
|---|---|---|
| Domain SCO Package（`crypto-wealth-sco-package.json`） | `docs/99.sdt/agn/0.schema/ontology/packages/` | 書込前に `sdt.authoring_resolve`。配置は `sdt_layout.resolve` で解決（推測配置禁止） |
| STM mapping（`crypto.mapping.json`） | `docs/99.sdt/agn/0.schema/ontology/mappings/` | 写像先は Core canonical / frozen DC のみ |
| 集約投影 | `sdt.sco_master`（`entry_class=project` rows） | 参照のみ。derived を source として手編集しない |
| 検証 | `sdt.ontology_validate` | package について `anchor_missing=0` / `anchor_unresolved=0` / `unapproved_frozen=0` / `shadow_ontology=0` を維持 |

- SDT JSON の直読み・直編集は禁止 — 読み書きは MCP Action 経由（AGENTS.md §Tools）。
- SCO 化の作業自体も Per-Work TaskGraph Lifecycle Gate に従う（Task node → Issue view → lease → 遷移）。

## 5. Feature ロードマップとの接続

| Feature（[`01-development-roadmap.md`](01-development-roadmap.md) §2） | SCO 上の主対象 |
|---|---|
| `F-CRYPTO-PORTFOLIO-DASHBOARD` | Wallet / Asset / Position（① + ② 起案） |
| `F-VIABILITY-POLICY-CORE` | ViabilityConstraint / Policy / RiskBudget / OptionalitySet の `DC:*` 起案 → **frozen 昇格 HIL（H2 と同時）** |
| `F-WORLD-MODEL-OBSERVE` | BoundaryVariable / ConstraintNode / Source の `DC:*` 起案 + 観測可能性等級の mapping 値域確定 |
| `F-OPPORTUNITY-ENGINE` | Opportunity（Convexity・Counterfactual 不変条件込み）の `DC:*` 起案 |
| `F-GUARDIAN-RISKSIGNAL` | RiskSignal / 不可逆性レベルの `DC:*` + mapping 値域 |

- 各 Feature の A02 Step 0 で、当該 Feature が導入するノード型の SCO 経路（①/②/③）を確定してから DD01 へ進む。
- Package / mapping の初期ファイル作成は `F-WORKSPACE-BOOTSTRAP`（catalog 初期化）の解消範囲に含める。

## 6. 禁止事項（Red Lines）

- ❌ SCO を経由しない SDT ノード型の新設（shadow ontology）
- ❌ `draft` DC を実ノード型・STM 写像先に使う
- ❌ Agent 単独での `frozen` 昇格・Core SCO の変更・重複概念の再定義
- ❌ 秘密鍵・シード・個人実値を SCO package / mapping / SDT に書く（CR-1。ε 等の**正本値**は `.dodoai/personal/config/` — Git 非共有。SCO が持つのは**概念と検査形式**のみ）
- ❌ 集約投影（`sdt.sco_master` 出力）の手編集

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 新設。dodoAI 本体の 2 層 SCO 機構に準拠した crypto profile の語彙正準化方針（経路判定・初期写像方針・lifecycle/HIL・置き場・Feature 接続・禁止事項）を定義 |
