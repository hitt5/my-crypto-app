---
type: strategy
title: 画面ロードマップ（基盤 Ops / LOOP 運用 / ドメイン画面の正本）
tags: [crypto-wealth-os, strategy, screen-roadmap, ops, loop, network, agent]
---

# 03 — 画面ロードマップ（Screen Roadmap）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: プロジェクト全体の**画面構成の正本**。優先度は [`01-implementation-priority.md`](01-implementation-priority.md)、運用ループは [`../1.concept/03-approach.md`](../1.concept/03-approach.md)、ネットワーク方針は [`../2.sdt-design/04-network-policy.md`](../2.sdt-design/04-network-policy.md) に追随する。各画面の詳細（ED15 画面一覧 / ED16 画面設計）は**所有 Feature の A02 で作成**し、本書は転記しない。
> **HIL 裁定**: 2026-08-22 — ユーザー指摘「ネットワーク接続管理（local→testnet→mainnet）と Agent 実行管理が無いと運用できない。Loop も追加」を受けて基盤 Ops カテゴリーと LOOP 運用画面を画面計画に組み込む。

## 1. 画面設計の原則

1. **画面は運用ループ①〜⑥へ対応させる**（`03-approach.md` §運用ループ）。どのステップにも対応しない画面を作らない。
2. **基盤（Ops）とドメイン（資産判断）を混在させない** — ネットワーク・Agent・WF・LOOP の運用状態は資産判断画面と別カテゴリー。
3. **不可逆性の昇順**（A 軸ハード制約）: 実行系画面（HIL 承認面）は P3 まで実装しない。mainnet は Observe（read-only）のみ。
4. **Fact / Belief の画面分離**（WM-3）: 評価（Belief）と実績・監査（Fact）は別画面。
5. **変動値を画面定義に書かない**: 画面はデータ取得 Action を参照する。LOOP 画面は catalog（宣言）と実行状態（TaskGraph/ART）を別レイヤーとして表示し、宣言側に変動値を書き戻さない。

## 2. カテゴリー構成（全体像）

```text
[OPS — 運用基盤]                        [LOOP — 閉ループ運用]
 OPS-1 ネットワーク管理 (L1/L2/L3)        LOOP-1 LOOP Catalog（宣言・統治）
 OPS-2 環境設定・接続ソース               LOOP-2 Loop Run（WF 周回・実行履歴）
 OPS-3 Agent 実行管理 / Kill Switch       LOOP-3 Loop Eval（校正・IG・空転検出）

[DOMAIN — 資産判断（運用ループ①〜⑥）]
 DOM-1 資産・生存ダッシュボード ①        DOM-4 Opportunity 評価 ②③
 DOM-2 Viability（正本 vs 実態）②        DOM-5 Guardian / RiskSignal ①④
 DOM-3 World Model 観測 ①               DOM-6 実行承認 HIL ④⑤（P3）
                                          DOM-7 Evidence / 監査 ⑥
```

## 3. OPS — 運用基盤画面

| ID | 画面 | 役割 | 所有 Feature | 優先度 | 根拠 |
|---|---|---|---|---|---|
| OPS-1 | ネットワーク管理 | chain 一覧（`network_class` 別）と RPC 接続状態、Anvil 起動/停止/fork 状態（`personal.crypto_testnet_ctl`）、**L1→L2→L3 昇格状態の可視化**（どのシナリオが L1 PASS 済みか・L2 昇格条件の記録）、mainnet = Observe-only のガード表示。既存 `SCR-CRYPTO-TESTNET-001` を発展吸収する | `F-CRYPTO-PORTFOLIO-DASHBOARD`（拡張） | **P0** | `04-network-policy.md` §2/§4。「迷ったら L1」を画面で強制 |
| OPS-2 | 環境設定・接続ソース | `portfolio.json` / `viability.json` の設定状態（実値非表示 — hash・valid_until・lint 結果のみ）、価格ソース・RPC の疎通と観測鮮度、`env://` 参照の解決可否（値は非表示） | `F-VIABILITY-POLICY-CORE`（lint/hash）+ `F-CRYPTO-PORTFOLIO-DASHBOARD`（ソース鮮度） | P0 | CR-1 / SR-5/6。鮮度は全判断の前提 |
| OPS-3 | Agent 実行管理 / Kill Switch | 14 Agent（`05-multi-agent.md`）の稼働状態・最終実行・権限状態（Session Key 有効期限・失効）、Stage 表示（Observe/Approve/Autopilot — Feature 別）、Guardian 発火時の停止フロー状態と**権限一括停止（Kill Switch）** | 新 Feature 要（例: `F-OPS-AGENT-CONSOLE` — EPIC/CAP 接続の HIL 先行） | P1 | CR-2、Key Gate、blast radius 限定。Agent 定常実行の開始（P1）までに必要 |

- OPS 画面は dodoAI 本体の Core 機構（WF/TaskGraph/Agent/HIL）を**参照統合**する。`impl_provenance = dodoai-core` の機能を Custom UI で再実装しない（`01-implementation-priority.md` §5）。

## 4. LOOP — 閉ループ運用画面

`03-approach.md` §LOOP Catalog の 3 層分離（**LOOP = 宣言・統治 / WF = 1 周の実行型 / SDT = 状態空間**）を画面境界にそのまま写像する。宣言と実行状態を同一画面に混ぜて catalog へ変動値を書き戻す経路を作らない。

| ID | 画面 | 役割 | データ源 | 優先度 |
|---|---|---|---|---|
| LOOP-1 | LOOP Catalog（宣言・統治） | 登録済み LOOP の一覧: OODA 4 フェーズ + Improve の所有者、成熟度（E0/E1/E2）と `maturity_basis`、空転検出定義、接地 references。**成熟度の昇格は HIL 導線（画面から直接変更しない）、降格は機械即時の結果表示** | `docs/99.sdt/agn/4.loops/loops.json`（SDT Action 経由。**catalog 未初期化の間は「未登録」を明示表示** — 推測表示しない） | P1（catalog 初期化 = `F-WORKSPACE-BOOTSTRAP` 完了後） |
| LOOP-2 | Loop Run（WF 周回・実行履歴） | 標準 WF（`wf-observe-loop` / `wf-evaluate-loop` / `wf-guardian-watch` / `wf-calibration-weekly`）の登録状態・スケジュール（Operation `tier` = 心拍）・各周回の TaskGraph 状態（ready/running/done/failed）・dispatch と observe の対（WM-4）・失敗周回の再実行導線 | `workflow.catalog_list` + TaskGraph（Core 参照） | **P0 相当**（開発ループ自体の観測面。ドメイン WF 登録前は開発系 WF を表示） |
| LOOP-3 | Loop Eval（校正・IG・空転検出） | 周回ごとの評価: forecast error（予測校正）・増分利益（対 No-action）・ΔΩ・IG の推移、`workflow.effectiveness_eval`（WF 遵守率・効率 — ループのループ）、空転検出（LOOP 宣言の定義に対する実測判定）。OODA Report（R-1/R-2/R-3）のレビュー面 | `docs/99.sdt/art/` の評価レコード（SDT Action 経由）。数値は取得 Action 参照 — 画面定義に転記しない | P1（`F-OPPORTUNITY-ENGINE` で校正ループが閉じてから本格化） |

- LOOP-3 とドメインの DOM-7（Evidence / 監査）の境界: DOM-7 は**資産判断の Evidence**（取引根拠・Gate 判定・承認記録）、LOOP-3 は**ループ自体の健全性**（校正・遵守率・空転）。同じ Evidence Ledger を読むが問いが異なるため画面を分ける。

## 5. DOMAIN — 資産判断画面（運用ループ①〜⑥）

| ID | 画面 | ループ | 所有 Feature | 優先度 | 状態 |
|---|---|---|---|---|---|
| DOM-1 | 資産・生存ダッシュボード | ① 観測 | `F-CRYPTO-PORTFOLIO-DASHBOARD` | P0 | ED15 定義済（`SCR-CRYPTO-PORTFOLIO-001`） |
| DOM-2 | Viability（生存制約・投資憲法 — 正本 vs 実態・DRIFTED） | ② 差分検知 | `F-VIABILITY-POLICY-CORE` | P0 | spec 済（SR-7） |
| DOM-3 | World Model 観測（境界変数・Constraint イベントカレンダー・Source 信頼度） | ① 観測 | `F-WORLD-MODEL-OBSERVE` | P1 | A02 未着手 |
| DOM-4 | Opportunity 評価（Convexity・No-action Counterfactual・Kelly サイズ・混雑度・`derives_from`。デフォルト「何もしない」を明示） | ②③ 評価 | `F-OPPORTUNITY-ENGINE` | P1 | A02 未着手 |
| DOM-5 | Guardian / RiskSignal（不可逆性シグナル・ruin 距離・停止フロー状態） | ①④ 検知 | `F-GUARDIAN-RISKSIGNAL` | P1 | A02 未着手 |
| DOM-6 | 実行承認 HIL（実行案 + 15 Gate 検査結果の全件表示・承認/却下） | ④⑤ HIL | `F-EXECUTION-APPROVE` | **P3**（Stage 2 昇格 HIL 前提 — 先行実装禁止） | 凍結 |
| DOM-7 | Evidence / 監査（Evidence Ledger 追記履歴・取引根拠・Gate 判定・承認記録） | ⑥ 学習 | 横断（CAP-EVIDENCE-LEDGER） | P1〜 | A02 未着手 |

## 6. 実装順（優先度キューへの接続）

| 段階 | 画面 | 前提 |
|---|---|---|
| P0（今） | DOM-1（完了させる）・DOM-2・OPS-1・OPS-2・LOOP-2（開発系 WF 表示） | `01-implementation-priority.md` P0 キュー |
| P1 | DOM-3・DOM-4・DOM-5・OPS-3・LOOP-1・LOOP-3・DOM-7 | LOOP catalog 初期化（`F-WORKSPACE-BOOTSTRAP`）、OPS-3 は新 Feature の A02+HIL |
| P2 | Airdrop/Claim・Yield 比較（DOM-4 の評価枠組みに従属するサブ画面） | P1-2 |
| P3 | DOM-6 | H4 + Stage 2 昇格 HIL（CR-2.5） |

## 7. 本書が禁止する画面判断

- OPS/LOOP 画面を後回しにしてドメイン画面だけ増やすこと（運用ループが回らない）
- LOOP catalog 未初期化のまま LOOP-1 に推測データを表示すること（`03-approach.md` §LOOP Catalog — JSON 推測作成禁止）
- LOOP 宣言ノードへ変動値（周回数・成功率・verdict）を書き戻す画面導線
- DOM-6（承認 UI）の P3 前実装（A 軸逆転）
- dodoAI 本体機構（WF/TaskGraph/Agent/HIL）の Custom UI 再実装
- 本書への画面詳細（レイアウト・ブロック構成）の記載 — ED15/ED16 は所有 Feature の A02 で作る

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 新設（HIL 指摘の文書化）。OPS（ネットワーク管理・環境設定・Agent 実行管理）/ LOOP（Catalog・Run・Eval の 3 層分離）/ DOMAIN（運用ループ①〜⑥対応 7 画面）のカテゴリー構成・実装順・禁止事項を定義 |
