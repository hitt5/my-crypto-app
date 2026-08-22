    ---
type: spec
title: F-VIABILITY-POLICY-CORE — Viability 正本（生存制約・投資憲法・RiskBudget・Ω）
tags: [crypto-wealth-os, personal-scope, a02, custom-action, custom-ui, viability]
---

# F-VIABILITY-POLICY-CORE — Viability 正本（S1）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **Feature ID**: `F-VIABILITY-POLICY-CORE`
> **Product Form**: パーソナル dodo Custom App（CR-8）。Personal Custom Action + Personal UI（`.dodoai/personal/`）で実装する。
> **自律度**: Stage 1 Observe のみ（read-only 評価。実行・署名・Policy Enforcement 実行系接続は本 Feature のスコープ外）。
> **Status**: draft — **H1（Concept v0.5 再承認）+ H2（正本値の HIL 確定）が本 Feature の DD01 入場前提**。

## 1. 位置づけ

Concept `03-approach.md` の **S1（Viability Model の初期定義）** を担う Feature。ロードマップ（[`../../2.sdt-design/01-development-roadmap.md`](../../2.sdt-design/01-development-roadmap.md)）の順 2。

タイプ E（正本＋実態観測）の「正本」側を確立する: ViabilityConstraint（生存制約 ε）・Policy（投資憲法）・Wallet 役割・RiskBudget・OptionalitySet（Ω）を**機械検査可能な JSON 正本**として定義し、`F-CRYPTO-PORTFOLIO-DASHBOARD` の実態観測（Fact）と突合して **DRIFTED（乖離）** を検知・表示する。

- W.M.×V.M. 差分検知（`F-OPPORTUNITY-ENGINE`）の V.M. 要求側入力になる — 本 Feature なしに実装順③以降は成立しない
- スコープ外: Policy の実行系エンフォース（署名拒否等 — Approve 段階の `F-EXECUTION-APPROVE` で dodo-wallet と統合）、Guardian の停止フロー、Opportunity 生成

## 2. BR（Business Requirements）

| ID | 要求 | 根拠 |
|---|---|---|
| BR-1 | 生存制約（ε・総損失限度・最低流動性準備率・不可逆性エクスポージャ上限）を数値で定義し、常に現状と比較できる | CR-9.1、答える問い 1 |
| BR-2 | 投資憲法（Policy）を決定論的に検査可能な形式で定義し、変更は HIL のみとする | CR-2.2 / CR-2.3 |
| BR-3 | Wallet を役割別（Vault/Earn/Explore/Trade）に分離し、目標配分との乖離（DRIFTED）を機械検知する | CR-5.5、04-data-model Wallet 不変条件 |
| BR-4 | RiskBudget（ε の配分）と Ω（介入可能性）の現状を実測ベースで把握できる | CR-9.8、答える問い 3 |
| BR-5 | 正本の実値（金額・配分・アドレス）を repo / SDT / ログへ保存しない | CR-1 / CR-8.3 |

## 3. SR（System Requirements）

| ID | 要求 | 検証方法 |
|---|---|---|
| SR-1 | Viability 正本スキーマ（`viability.json`: ViabilityConstraint / Policy / Wallet 役割 / target_allocation / RiskBudget / Ω 棚卸し）を JSON Schema として定義し、Personal Custom Action `personal.crypto_viability_lint` が正本ファイルをスキーマ + 意味検査（全項目が決定論的に検査可能・有効期限あり・RiskBudget 合計 ≤ 総損失限度）する | pytest + live dispatch |
| SR-2 | Personal Custom Action `personal.crypto_drift_check` が、正本（viability.json）× 実態（snapshot / valuation の出力）を突合し、役割別配分乖離・流動性準備率・ruin 距離プロキシ（総損失限度に対する現エクスポージャ比）を DRIFTED 判定付きで返す | pytest（実態は fixture、実値なし） |
| SR-3 | drift 判定は決定論的閾値（正本に定義された tolerance）のみで行い、LLM 推定値を使わない（WM-3） | コードレビュー + pytest |
| SR-4 | drift 結果は `.dodoai/personal/data/drift.jsonl` へ追記保存する（追記のみ） | pytest + `.gitignore` 検査 |
| SR-5 | 正本は `.dodoai/personal/config/viability.json`（Git 非共有）に置き、repo にはプレースホルダのみの `viability.sample.json` を置く | fixture 検査 |
| SR-6 | 正本の変更検知: `personal.crypto_viability_lint` は正本ファイルの hash を記録し、前回からの変更を出力に含める（変更承認の HIL 補助。Agent による正本書き換え経路は作らない — CR-2.3） | pytest |
| SR-7 | Personal UI `crypto-wealth` に `viability` ページ（生存制約の現在値 vs 上限・役割別配分 目標 vs 実態・DRIFTED 一覧・Ω 棚卸し）を追加する | `custom_ui.manifest_lint(mode="strict")` error_count=0 |
| SR-8 | 全 Action は read-only（正本ファイルへの書き込み経路を持たない）、`risk_level: low` | action.json 検査 |

## 4. UC（Use Cases）

### UC-1 生存制約と実態の乖離を一目で確認する
- ユーザーが Personal UI「Crypto Wealth」の `viability` ページを開く
- 生存制約（ε・損失限度・流動性準備率）の現在値/上限、役割別配分の目標 vs 実態、DRIFTED 一覧が表示される
- 受入基準: 正本に定義された全制約項目が表示され、各項目に OK / DRIFTED が併記される

### UC-2 正本を lint して HIL 承認の材料にする
- `personal.crypto_viability_lint` を dispatch する
- スキーマ違反・非決定論的項目・RiskBudget 超過・有効期限切れ・前回からの変更差分が報告される
- 受入基準: 意図的に壊した fixture で各違反が個別に検出される。正本 hash 変更が検出される

### UC-3 drift 履歴を蓄積する
- `personal.crypto_drift_check` を手動または CRON で dispatch する
- DRIFTED 判定が drift.jsonl へ追記される
- 受入基準: 同一入力での再実行が履歴を壊さない（追記のみ）。判定に使った閾値と入力参照が記録に含まれる

## 5. CAP / MOD

| CAP | FR | MOD（実装置き場） |
|---|---|---|
| CAP-VIABILITY-CANON（生存正本管理） | FR: 正本スキーマ定義 / lint / 変更検知 | `.dodoai/personal/custom_actions/crypto_viability_lint/` |
| CAP-VIABILITY-DRIFT（乖離検知） | FR: 正本×実態突合 / DRIFTED 判定 / 追記保存 | `.dodoai/personal/custom_actions/crypto_drift_check/` |
| CAP-PORTFOLIO-VIEW（統合表示 — 既存 CAP へ追加） | FR: viability ページ表示 | `.dodoai/personal/custom_ui/crypto-wealth/manifest.json` |

> 注: EPIC / CAP catalog（`docs/99.sdt/art/catalog/source/`）は未初期化。catalog 初期化時に正式登録する（fr_gap として記録 — `F-CRYPTO-PORTFOLIO-DASHBOARD` と同じ既知負債）。

## 6. データ設計（personal scope・Git 非共有）

```text
.dodoai/personal/
  config/viability.json        ← 正本（ユーザーが HIL で編集。Agent 書込禁止）
  data/drift.jsonl             ← DRIFTED 判定履歴（追記のみ）
```

`viability.json` スキーマ骨子（実値は書かない — サンプルはプレースホルダのみ）:

```jsonc
{
  "version": "1.0.0",
  "valid_until": "2027-XX-XX",                    // 有効期限必須（Policy 不変条件）
  "viability_constraint": {
    "epsilon": 0.0,                                // P(ruin) 上限（HIL 定義）
    "total_loss_limit_usd": 0,                     // 総損失限度
    "min_liquidity_reserve_ratio": 0.0,            // 最低流動性準備率
    "irreversibility_exposure_limit_usd": 0        // 不可逆性エクスポージャ上限
  },
  "policy": {
    "daily_amount_limit_usd": 0,
    "allowlist_assets": [],
    "allowlist_protocols": [],
    "max_slippage_bps": 0,
    "leverage_forbidden": true,
    "loss_limit_usd": 0,
    "turnover_limits": { "trades_per_day": 0, "monthly_volume_usd": 0, "gas_budget_usd": 0 },
    "approval_threshold_usd": 0
  },
  "wallet_roles": [
    { "label": "vault-safe", "role": "vault", "autonomy": "manual-only" }
  ],
  "target_allocation": { "vault": 0.6, "earn": 0.25, "explore": 0.1, "trade": 0.05 },
  "allocation_tolerance": 0.05,                    // DRIFTED 判定閾値
  "risk_budget": [
    { "scope": "wallet:vault-safe", "max_expected_loss_usd": 0 }
  ],
  "optionality_inventory": [
    { "kind": "liquidity", "proxy": "instantly_liquid_usd" },
    { "kind": "protocol_access", "proxy": "accessed_protocol_count" }
  ]
}
```

## 7. HIL / 拡張条件

- **DD01 入場前提**: H1（Concept v0.5 再承認）+ H2（ε・損失限度・目標配分・Allowlist の実値 HIL 確定）
- Policy の実行系エンフォース（署名拒否・Session Key 制約）への拡張は本 Feature では行わない。`F-EXECUTION-APPROVE` の A02 + Stage 昇格 HIL で扱う
- ruin 距離の本格推定（分布ベース）は `F-WORLD-MODEL-OBSERVE` 以降。本 Feature では決定論的プロキシ（損失限度比）に留める

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版（draft）。S1 = Viability 正本（生存制約・投資憲法・Wallet 役割・RiskBudget・Ω）+ DRIFTED 検知を Observe 段階の Action 2 本 + viability ページとして定義。H1/H2 を DD01 入場前提として明記 |
