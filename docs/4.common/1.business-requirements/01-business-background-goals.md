---
type: common-requirement
title: ビジネス背景・ゴール
tags: [common, business-requirement, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 入力正本 | [`../../1.concept/00-overview.md`](../../1.concept/00-overview.md) / [`01-problem.md`](../../1.concept/01-problem.md) / [`07-why-not-simple.md`](../../1.concept/07-why-not-simple.md) |

# ビジネス背景・ゴール

## 1. 本文書の目的

本文書は、dodo Crypto Wealth OS のビジネス要件（BR-1〜BR-7、[`02-business-requirement.md`](02-business-requirement.md)）を導出するにあたり、その前提となる背景・目的関数・市場環境・ポジショニングを定義する。Concept（`1.concept/`）の要約であり、正本は Concept 側にある。

## 2. プロダクトの位置づけ

dodo Crypto Wealth OS は、**single-owner / local-first のパーソナル dodo Custom App** である。dodoAI 上の Personal Custom UI + Personal Custom Action として実装され、ユーザー本人の暗号資産形成を支援する。

- 「AI に相場を当てさせるアプリ」ではなく、**World Model（何が起こり得るか）と Viability Model（どの未来なら生存でき選択肢が増えるか）の差分から介入機会を発見し、生存制約下で Agentic Settlement（契約・署名・決済）を積み重ねるパーソナル AI 資産形成 OS**
- 資産（秘密鍵）はユーザーが持ち、Agent は期限付き・用途限定の権限と決定論的な Policy Engine に拘束される — **Non-custodial, policy-custodied autonomy**
- 同時に、**dodoAI の Agent 統治（防衛グレード）を最も過酷なゼロトラスト環境で検証する試金石**である

## 3. 大原則（Prime Directive — 全 BR の上位原理）

> **不可逆的な損失を避けながら、将来取り得る選択肢（介入可能性）を最大化する。**

```text
max_π  E[ Δlog W + α·ΔΩ + β·IG ]
subject to  P(ruin) < ε
```

- **W**: 資本 / **Ω**: 将来実行可能な Action 集合（Optionality）/ **IG**: 情報利得 / **ruin**: 回復不能な破綻
- リスクは価格変動（ボラティリティ）ではなく**不可逆性（将来の意思決定能力の喪失）**を第一軸として管理する
- セキュリティ侵害（鍵流出・権限奪取・任意 calldata 署名）は ruin の具体形であり、P(ruin) < ε はゼロトラスト設計を内包する

## 4. 根底に置く 4 仮説（BR の根拠）

| # | 仮説 | 要旨 |
|---|---|---|
| H-1 Survival Premium | 破綻しなかった資本だけが次の大きな機会を取れる。行動可能性の保有自体に価値がある |
| H-2 Constraint Alpha | 収益機会は情報差より「他者が動かざるを得ない地点」に発生する |
| H-3 Convexity | 正解率より Payoff 構造。確率分布 × 損益分布 × 不可逆性で評価する |
| H-4 Reflexivity | 同一モデルの混雑がモデル自身の危機を作る。混雑度を観測対象に含める |

## 5. 市場環境とポジショニング（要約 — 正本 = 07-why-not-simple.md）

- 「ノンカストディアル Wallet ＋ Agent ＋ リスク制約 ＋ 自動実行」は 2026 年時点でコモディティ化（Giza / Wayfinder / Almanak / MetaMask / OKX / Phantom）
- 空いているのは**戦略ポートフォリオを同一リスク尺度で比較し、予測確度を継続校正し、ユーザー固有の投資知として学習する Sovereign Crypto CIO** の層
- 差別化 4 層 = 生存原理・不可逆性管理・Constraint Graph・IG 校正。いずれも dodoAI の統治基盤（SDT・Gate・Evidence・HIL）の応用であり、実行層プレイヤーが後付けで真似るには統治基盤の再構築が必要
- チェーン（実行層 = Swap Routing / Lending calldata）は外部に委任するが、**Wallet（Signer / 鍵管理 / Session Key 統治 / Policy Enforcement）は dodo-wallet + dodo クレデンシャル機構（自前）が持つ**

## 6. ゴール（何を達成したら成功か）

| # | ゴール | 測定 |
|---|---|---|
| G-1 | 生存制約（P(ruin) < ε）の逸脱ゼロで運用が継続していること | Policy / Viability Gate の逸脱件数 = 0 |
| G-2 | 介入の増分利益が No-action ベンチマーク（BTC 保持・ステーブル保持・不作為）に対し正であること | Evidence Ledger の counterfactual_return |
| G-3 | 予測確度が校正されていくこと（IG の蓄積） | forecast error / confidence_calibration の推移 |
| G-4 | Ω（介入可能性）が縮小していないこと | OptionalitySet の実測（即時換金可能額・access 済み Protocol 数等） |
| G-5 | 鍵・権限の統治逸脱ゼロ（秘密鍵非接触・任意 calldata 署名ゼロ・Session Key 失効管理） | 監査（Evidence / audit event） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。Concept v0.5（生存原理・三要素・4仮説・CIO ポジショニング）を BR 導出の前提として要約 |
