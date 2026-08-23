---
type: spec
title: F-CRYPTO-PORTFOLIO-DASHBOARD — パーソナル資産ダッシュボード（EVM / Observe 段階）
tags: [crypto-wealth-os, personal-scope, a02, custom-ui, custom-action]
---

# F-CRYPTO-PORTFOLIO-DASHBOARD — パーソナル資産ダッシュボード

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **Feature ID**: `F-CRYPTO-PORTFOLIO-DASHBOARD`
> **Product Form**: パーソナル dodo Custom App（CR-8）。Personal UI 機構 + Personal Custom Action（`.dodoai/personal/`）で実装する。
> **自律度**: Stage 1 Observe のみ（read-only。実行・署名は本 Feature のスコープ外）。

## 1. 位置づけ

Concept `03-approach.md` の実装順 **①資産・ポジション統合表示（Fact 化）** を担う最初の Feature。
タイプ E（正本＋実態観測）の起点として、Wallet 残高・Position をオンチェーン実測（Fact）で統合表示し、価格 Tick を複数ソースで照合し、評価額・配分を可視化する。

- スコープ: **EVM 系チェーンから開始**（初期 = Ethereum mainnet。L2 は同一実装で chain_id 追加のみで拡張可能にする）
- 対象 Wallet: ユーザー本人の EOA / Safe（作成中）のアドレス。アドレスは公開情報だが個人実値のため **repo にコミットせず** personal scope のローカル設定に置く
- スコープ外: 取引実行・署名・Approve/Autopilot（CR-3 パイプライン）、Opportunity クロール、multi-user

## 2. BR（Business Requirements）

| ID | 要求 | 根拠 |
|---|---|---|
| BR-1 | 本人の EVM Wallet 群の資産・ポジションを 1 画面で統合把握できる | Concept 実装順①、答える問い 3（正本と実態の把握が前提） |
| BR-2 | 価格は単一ソースに依存せず複数ソース照合で表示する | CR-3.3（単一オラクル禁止）を Observe 段階から遵守 |
| BR-3 | 価格 Tick / 残高スナップショットの履歴をローカルに追記保存し、後段（差分検知・Evidence）の土台にする | CR-4（Evidence by Default）、E 型モニタリング |
| BR-4 | 秘密鍵・シード・個人実値を repo / SDT / ログへ保存しない | CR-1 / CR-8.3 |

## 3. SR（System Requirements）

| ID | 要求 | 検証方法 |
|---|---|---|
| SR-1 | Personal Custom Action `personal.crypto_portfolio_snapshot` が、設定ファイルの Wallet アドレス群について ETH 残高 + ERC-20 残高を RPC 実測で返す | pytest（RPC は mock）+ live dispatch |
| SR-2 | Personal Custom Action `personal.crypto_price_tick` が、2 つ以上の独立ソースから USD/JPY 価格を取得し、照合結果（乖離率）付きで返す。ソースが 1 つしか成功しない場合は `degraded` を明示する | pytest（HTTP は mock） |
| SR-3 | Personal Custom Action `personal.crypto_portfolio_valuation` が snapshot × tick を突合し、総資産額・Wallet 別/Asset 別内訳・（目標配分が定義されていれば）乖離を返す | pytest |
| SR-4 | Tick / snapshot は `.dodoai/personal/data/`（Git 非共有）へ JSONL 追記保存する。改変・削除はしない（追記のみ） | pytest + `.gitignore` 検査 |
| SR-5 | Wallet アドレス・目標配分は `.dodoai/personal/config/portfolio.json`（Git 非共有）から読む。repo 内 fixture に実アドレスを書かない | コードレビュー + fixture 検査 |
| SR-6 | Personal UI manifest `crypto-wealth` が dashboard ページ（総資産・Wallet 別内訳・Asset 一覧・価格照合状態）を提供する | `custom_ui.manifest_lint(mode="strict")` error_count=0 |
| SR-7 | 全 Action は read-only（外部への書き込み・署名・送金経路を持たない）、`risk_level: low` | action.json 検査 |
| SR-8 | Personal Custom Action `personal.crypto_testnet_ctl` が、ローカルテストネット（Anvil, chain_id 31337, localhost 限定 bind）を start/stop/status で制御できる。稼働判定は RPC 実測で行う | pytest（subprocess/RPC は mock）+ live smoke |
| SR-9 | Personal Custom Action `personal.crypto_testnet_fund` が、ローカルテストネット上のアドレスへ test ETH を注入できる。chain_id 31337 以外は実行前に拒否する（設定ミス防御） | pytest（31337 以外拒否のテスト必須）+ live smoke |

## 4. UC（Use Cases）

### UC-1 ポートフォリオを一目で確認する
- ユーザーが dodoAI の Personal UI「Crypto Wealth」を開く
- dashboard に総資産額（USD/JPY）、Wallet 別内訳、Asset 別保有量・評価額が表示される
- 受入基準: 設定済み Wallet 全件の残高が表示され、価格に照合ソース数と乖離率が併記される

### UC-2 価格 Tick を取得・蓄積する
- Action `personal.crypto_price_tick` を手動または CRON で dispatch する
- 複数ソースの価格が取得され、照合結果とともに JSONL へ追記される
- 受入基準: 2 ソース成功時は乖離率が記録され、1 ソース時は `degraded=true` が記録される

### UC-3 スナップショット履歴を残す
- Action `personal.crypto_portfolio_snapshot` の実行ごとに残高スナップショットが JSONL へ追記される
- 受入基準: 同一 payload での再実行が履歴を壊さない（追記のみ・冪等な読み取り）

### UC-4 ローカルテストネットで検証する
- ユーザーが Personal UI「テストネット」ページまたは Action dispatch で Anvil を起動し、Wallet アドレス（公開情報）へ test ETH を注入し、snapshot/dashboard の実 RPC 動作を確認する
- 受入基準: start → status(running, chain_id=31337) → fund（残高は eth_getBalance 実測で返る）→ stop が成功し、mainnet/公開 testnet への fund は拒否される
- ネットワーク選択の正本: `docs/2.sdt-design/04-network-policy.md`（L1 ローカル軸 — HIL 裁定 2026-08-22）

## 5. CAP / MOD

| CAP | FR | MOD（実装置き場） |
|---|---|---|
| CAP-PORTFOLIO-OBSERVE（資産実態観測） | FR: EVM 残高実測 / 複数ソース価格照合 / 評価額算出 / ローカル追記保存 | `.dodoai/personal/custom_actions/crypto_portfolio_snapshot/`・`crypto_price_tick/`・`crypto_portfolio_valuation/` |
| CAP-PORTFOLIO-VIEW（統合表示） | FR: dashboard / testnet ページ表示 | `.dodoai/personal/custom_ui/crypto-wealth/manifest.json` |
| CAP-PORTFOLIO-OBSERVE（検証基盤） | FR: ローカルテストネット制御 / test 資金注入（local 限定） | `.dodoai/personal/custom_actions/crypto_testnet_ctl/`・`crypto_testnet_fund/` |

> 注: EPIC / CAP catalog（`docs/99.sdt/art/catalog/source/`）は本プロジェクトで未初期化。catalog 初期化時に本表を正式登録する（fr_gap として記録）。

## 6. 画面一覧（Personal UI）

| Page | 内容 | Blocks |
|---|---|---|
| `dashboard` | 総資産額・観測鮮度・Wallet 別内訳・Asset 一覧・配分乖離・価格照合 | summary-hero / stat-card / data-table × 4 |
| `testnet` | ローカルテストネット（Anvil）状態・操作ガイド | summary-hero / markdown |
| （後段）`wallets` | Wallet 役割別詳細・Approval 一覧 | — |
| （後段）`ticks` | 価格履歴・ソース間乖離 | — |

## 7. データ設計（personal scope・Git 非共有）

```text
.dodoai/personal/
  config/portfolio.json      ← Wallet アドレス・監視トークン・目標配分（ユーザーが編集）
  data/ticks.jsonl           ← 価格 Tick 履歴（追記のみ）
  data/snapshots.jsonl       ← 残高スナップショット履歴（追記のみ）
```

`portfolio.json` スキーマ（実値は書かない — サンプルはプレースホルダのみ）:

```jsonc
{
  "chains": [{ "chain_id": 1, "name": "ethereum", "rpc_url": "env://EVM_RPC_URL_1" }],
  "wallets": [{ "label": "vault-safe", "role": "vault", "address": "0x...", "chain_id": 1 }],
  "tokens": [{ "symbol": "USDC", "chain_id": 1, "address": "0x...", "decimals": 6 }],
  "target_allocation": { "vault": 0.6, "earn": 0.25, "explore": 0.1, "trade": 0.05 }
}
```

- RPC URL は `env://` 間接参照（CR-1.2）。無料公開 RPC でも直書きせず env 経由にする。
- 価格ソース初期値: CoinGecko（simple price）+ Binance public ticker の 2 系統。API キー不要の public endpoint から開始。

## 8. HIL / 拡張条件

- 実行系（送金・Approve 操作）への拡張は本 Feature では行わない。着手前に HIL + A02 更新（CR-8.4 準用）。
- L2 / 非 EVM チェーン追加は config 追加で対応できる範囲は HIL 不要、データモデル変更を伴う場合は spec 改版。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.0 | 2026-08-22 | ローカルテストネット対応（HIL: ローカル軸）。SR-8/SR-9・UC-4・`testnet` ページ・`crypto_testnet_ctl` / `crypto_testnet_fund` を追加。ネットワーク選択の正本として `docs/2.sdt-design/04-network-policy.md` を新設・参照 |
| v0.1.0 | 2026-08-22 | 初版。EVM から開始（ユーザー裁定）。Observe 段階の Action 3 本 + Personal UI dashboard を定義 |
