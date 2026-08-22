---
type: concept
title: なぜ「単純な自動運用アプリ」ではダメか（競合環境と差別化根拠）
tags: [concept, competitive-analysis, positioning, crypto-wealth-os]
---

# 07 — なぜ「単純な自動運用アプリ」ではダメか（Why Not Simple）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 本ドキュメントは「単に AI がレンディング・トレードを組み合わせて資産形成するアプリ」を作らない理由（競合環境の事実認識）と、そこから導かれるポジショニング（差別化根拠）の正本。[`00-overview.md`](00-overview.md) の Product Form・[`01-problem.md`](01-problem.md) の課題認識を補完する。
> **注意**: 本書の競合情報は 2026 年時点の公開情報に基づく Belief（外部観測）であり、Fact（自プロジェクトの実装状態）ではない。定期的に再検証する。

## 結論（先に要旨）

**「Agent が DeFi で自動的に稼ぐ」は既にレッドオーシャンである。** 「ノンカストディアル Wallet ＋ Agent ＋ リスク制約 ＋ 自動実行」は 2026 年に入り一気にコモディティ化した。したがって本プロジェクトを *Wallet + Swap + Lending + AI チャット* 程度の「単純なもの」として作ると、MetaMask・Phantom・Wayfinder・Giza の間に埋もれる。

まだ空いているのは、

> **すべての資産形成機会を「戦略ポートフォリオ」として比較し、予測の確度を継続的に校正し、ユーザー固有の投資知として学習する Sovereign Crypto CIO**

であり、本プロジェクトはここを主戦場とする。さらに v0.5 根本改訂（[00-overview.md](00-overview.md)）以降、この CIO は**生存原理**（生存制約下での幾何平均成長 + Optionality 最大化）を目的関数として持ち、競合が実装していない**不可逆性管理・Constraint Graph（誰が動かざるを得ないか）・Reflexivity（混雑）監視**を差別化の中核に加える。競合の Yield 最適化は「期待収益の最大化」に留まり、「二度と次の Action を取れなくなること」を第一のリスクとして扱う製品は存在しない。

## 1. 競合環境の事実認識（2026 年時点）

### 1.1 最も近い競合の一覧

| 競合 | 何を実現しているか | dodo 構想との近さ |
|---|---|---:|
| Giza | リスク調整済みイールド、複数プロトコル配分、制約付き自律実行 | 非常に近い |
| Wayfinder | マルチチェーン、現物・Perp・予測市場、Agent 戦略市場 | 非常に近い |
| Almanak | Python、Intent、バックテスト、EVM＋Solana、Safe 権限制御 | インフラ面で非常に近い |
| MetaMask Agent Wallet | Agent 専用 Wallet、支出上限、Allowlist、リスクスキャン | Wallet 層で直接競合 |
| OKX Agentic Wallet | 約 20 ネットワーク、自然言語実行、TEE 鍵管理 | Wallet 層で直接競合 |
| Phantom MCP | Solana＋EVM を Agent から操作、Swap、Perp、リバランス | Wallet/MCP 層で競合 |
| DeFi Saver | Lending、借入、レバレッジ、清算回避、自動化 | DeFi 運用で強い |
| Aera | 機関・DAO 向けリスク制約付き Treasury 運用 | B2B で近い |
| Drops/FarmDash | エアドロップ検知・Eligibility・ポイント追跡 | Airdrop 部分で競合 |

### 1.2 Giza — 最警戒の直接競合

Giza Agent（2026 年版）は既に以下を実装している:

- 複数プロトコルへの同時配分（APR だけでなく流動性・リスクを考慮）
- プロトコル別上限・最低分散数・除外プロトコル
- ガスを考慮したリバランス（**「APR 改善が移動コストを十分上回る場合だけリバランスする」設計を明示**）
- 報酬 Claim と自動再投資、判断理由の表示、異常時の退避
- Session Key による限定権限
- Optimizer API: 現在配分・対象プロトコル・制約を渡すと、最適配分・改善 APR・コスト・実行 Action・calldata まで返す（[Giza Optimizer](https://docs.gizatech.xyz/developers/guides/iaas-integration) / [機関向け Agent](https://www.gizatech.xyz/blog/re7-brings-the-first-wave-of-institutional-financial-agents)）

つまり本プロジェクトの「無駄に取引しない」「確度とコストで判断する」に相当する部分まで既に考えられている。ただし現状は Stablecoin Yield / Lending プロトコル間配分 / Base 中心 / Smart Account に預けた範囲が主で、**総合的な個人資産形成 OS にはなっていない**。

### 1.3 Almanak — インフラ面での正面衝突リスク

Almanak は Python SDK・高水準 Intent・Swap/LP/Borrow・EVM＋Solana・20 以上のプロトコル・バックテスト・Paper Trading・Parameter sweep・Safe＋Zodiac による限定権限・LLM Agent・緊急停止・Canary deployment・Strategy Container と秘密情報の分離まで提供している（[Almanak SDK](https://sdk.docs.almanak.co/)）。

```text
Python Strategy → Intent → Gateway → Simulation → Scoped Permission → On-chain Execution
```

この技術構造は dodoAI＋Rust Wallet 構成とかなり似ている。**dodoAI を「DeFi Agent 開発 SDK」として戦わせると Almanak と正面衝突する。**

### 1.4 Wayfinder — UI・マーケットプレイスの先行

Wayfinder は複数 Wallet・複数 Chain の統合 Portfolio、現物、Hyperliquid Perp、Polymarket、自然言語 Agent、自動戦略、デルタニュートラルな Funding capture、コミュニティ戦略のインストール、Strategy SDK まで打ち出している（[Wayfinder](https://wayfinder.ai/)）。「資産を一元表示し、Agent へ『BTC をヘッジして』と指示できる」だけでは差別化にならない。

### 1.5 Wallet 層は大手が急速に押さえた

- **MetaMask Agent Wallet**: 支出上限・Protocol Allowlist・Guard Mode・自律実行・Threat Scan・MEV Protection・2FA 承認（[発表](https://metamask.io/ja/news/introducing-metamask-agent-wallet)）
- **OKX Agentic Wallet**: 約 20 ネットワーク、TEE 内鍵隔離、Agent から Seed へアクセス不能な構造（[発表](https://www.okx.com/en-gb/help/okx-wallet-officially-launches-agentic-wallet)）
- **Phantom MCP Server**: AI Agent から Solana/EVM の送金・Swap・Perp・Portfolio Rebalance を操作可能（[docs](https://docs.phantom.com/phantom-mcp-server/index)）

したがって「EVM と Solana を透過的に扱える Agent Wallet」そのものはもう独立したモートにならない。**Rust Wallet Core は必要だが、主戦場にしてはいけない。**

## 2. 「単純なもの」が負ける理由（まとめ）

| 単純な構想 | なぜダメか |
|---|---|
| Agent Wallet を作る | MetaMask / OKX / Phantom / Coinbase が Wallet と Agent 実行層を押さえ始めており、モートにならない |
| Yield Aggregator / 自動リバランス | Giza が確度・コスト考慮の配分最適化まで実装済み |
| Trading Bot / 自然言語で売買指示 | Wayfinder が UI・戦略市場まで先行。価格予測αは再現性が最も低い（[01-problem.md](01-problem.md) §3） |
| DeFi Agent 開発 SDK | Almanak と正面衝突 |
| Airdrop Farmer | Drops / FarmDash 等が検知・Eligibility 追跡で先行 |
| Wallet + Swap + Lending + AI チャット | 上記すべての合成であり、各専業の間に埋もれる |

## 3. まだ空いている領域 — 戦略ポートフォリオを運営する CIO

既存サービスの多くは Yield 最適化 / Lending 管理 / Trading / Agent Wallet / Airdrop 検知 / Strategy Marketplace の**どれか一つ**に寄っている。市場は分断されており、それらを横断して同じリスク尺度で比較する層はまだ弱い。

本プロジェクトが狙うのは、資産の配分ではなく**戦略へのリスク予算配分**である。

| 戦略 | 期待収益 | 確度 | 最大損失 | 流動性 | 相関 |
|---|---:|---:|---:|---:|---:|
| BTC 長期保有 | 中 | 中〜高 | 高 | 高 | 市場β |
| Stablecoin Lending | 低〜中 | 高 | Protocol 依存 | 高 | 低〜中 |
| Staking | 低〜中 | 高 | Token 下落 | 中 | 市場β |
| Airdrop | 不明〜高 | 低〜中 | Gas＋時間 | 低 | 低 |
| Funding Capture | 中 | 中〜高 | Basis・清算 | 中 | 低 |
| LP | 中 | 中 | IL・Contract | 中 | 資産依存 |
| 方向性 Trading | 高 | 低 | 高 | 高 | 市場β |
| Risk-off | 収益なし | 高 | 機会損失 | 高 | 負相関 |

これらを同じ土俵で評価する製品はまだ成熟した形で存在しない。

### 3.1 最重要の差別化 —「確度」を本当に測る（Calibration）

LLM が「確信度 80%」と言っても意味はない。過去の予測と実績から、

> 70% と評価した Opportunity が、本当に約 70% の割合で成立したか

を検証する。Opportunity（[../2.sdt-design/02-data-model.md](../2.sdt-design/02-data-model.md) の Opportunity 空間）に次を持たせる:

```yaml
opportunity:
  type: lending
  expected_return:
    lower: 4.2
    median: 6.1
    upper: 8.0
  probability_of_positive_return: 0.84
  confidence_calibration: 0.77
  maximum_loss: 1.0
  liquidity_horizon: 24h
  protocol_risk: 2
  evidence_strength: 0.91
  correlation:
    crypto_beta: 0.18
    stablecoin_depeg: 0.72
  execution_cost: 12.50
  decision: allocate
```

そして実績を戻す:

```yaml
outcome:
  realized_return: 5.4
  unexpected_events:
    - reward_rate_reduction
  forecast_error: -0.7
  decision_quality: good
  counterfactual_return: 4.1
```

この蓄積により学習できるもの:

- どの Agent が正確か / どの情報源が正確か
- どの Protocol Risk を過小評価したか / Airdrop 期待値を過大評価していないか
- 売買した方が本当に得だったか（Counterfactual — [00-overview.md](00-overview.md) 問い 2 に直結）
- そのユーザーにどの戦略が合うか

これはまさに dodoAI の OI（Organizational Intelligence）であり、単純アプリでは構築できない蓄積型のモートになる。

## 4. 戦略的な役割分担 — 全部を自前で作らない

全プロトコル Adapter を自前で作る必要はない。役割を分ける:

```text
dodoAI
＝ CIO・World Model・Risk Budget・OI

Almanak / Giza / DeFi Saver
＝ Strategy Execution

dodo-wallet（自前）
＝ Signer・鍵管理・Session Key 統治・Policy Enforcement

Aave / Morpho / Jupiter / Hyperliquid
＝ Financial Venue
```

dodoAI はこれらの上位に立つ。すなわち、

> 「どこでどう実行するか」より、「そもそも何に、なぜ、どれだけ配分するか」を司る

製品である。

### 4.1 dodoAI が持つべき領域

- 全資産・全ポジションの World State
- Opportunity Graph（Web・GitHub・Governance・On-chain クロール）
- 期待収益分布・確度校正・最大損失推定・戦略間相関
- リスク予算配分・Counterfactual 評価
- 過去判断の OI（Agent / モデル / 情報源ごとの成績）
- Wallet を跨いだ Policy
- 人間の目的・期間・許容損失
- **Wallet（Signer / 鍵管理 / Session Key の発行・失効統治 / Policy Enforcement）= dodo-wallet + dodo クレデンシャル機構（CR-1 二層構成）**

### 4.2 外部に任せられる領域

- DEX Routing / Bridge Routing / Lending calldata / LP 構築 / Perp 注文
- Smart Account の基盤コントラクト（Safe 等）・一般的な Wallet UI

> ただし **Signer・鍵管理・Session Key の発行/失効統治・Policy Enforcement は dodo-wallet + dodo クレデンシャル機構（CR-1）が持つ**。外部に任せるのは実行の配管であって、鍵と権限の統治ではない。

## 5. dodoAI 防衛グレードへの寄与 — 本テーマは AI 統治の試金石

本テーマの位置づけは製品開発に留まらない。**dodoAI の Agent 統治（防衛グレード）を、最も過酷なゼロトラスト環境で検証する試金石**である（[00-overview.md](00-overview.md) §AI 統治の試金石）。

### 5.1 ゼロトラスト・クリプトが最過酷なテストベッドである理由

クリプトはゼロトラストが前提の環境である: 取引は不可逆・相手は匿名・コントラクトは敵対的・情報源は汚染済み（プロンプトインジェクション / 偽サイト / 偽トークン）・失敗は即座に定量化される。**ここで壊れない Agent 統治は、あらゆるドメインで壊れない。**

| dodoAI のセキュリティ・統治機構 | クリプトでの検証内容 |
|---|---|
| 鍵の分離統治（CR-1: DID/VC・`env://`・Desktop 署名 + ハードウェアモジュール二層） | **Agent 自身をゼロトラスト対象**とし、鍵に到達できない構造で自律実行させる |
| 決定論的 Policy Engine（LLM に最終可否を出させない） | LLM が乗っ取られても（インジェクション・誤情報）実害に至らない多層防御 |
| Session Key 失効・Kill Switch・権限の期限/用途限定 | 侵害を前提とし blast radius を限定する権限設計 |
| リスクレベル評価 + HIL 必須（Irreversibility Gate / H4） | 不可逆な Action は自律度に関わらず人間承認 — Capability Routing（CP8+ = human）の金融ドメイン実装 |
| CR-6（クロール内容を命令として解釈しない・SBOM/MCP 統制） | 敵対的入力に常時晒される Agent の入力境界防御 |
| Evidence 追記のみ・改変禁止 | 侵害後のフォレンジック可能性（改ざん不能な監査線） |
| Guardian の停止フロー（取引停止 → 権限停止 → Approval 解除 → 退避） | 自動化されたインシデントレスポンス |

### 5.2 我々はチェーンをやらない — 統治層に集中する

§4 の役割分担の通り、Swap Routing・Lending calldata・チェーン基盤は外部レイヤーに委任する。ただし **Wallet（Signer / 鍵管理 / Policy Enforcement）は dodoAI 自身のもの — dodo-wallet + dodo クレデンシャル機構（CR-1 二層構成）— を使う**。鍵と権限の統治は防衛グレードの中核であり、外部 Wallet に委任しない（外部 Wallet は §1.5 の通りコモディティ化しており、差別化の主戦場でもない）。本テーマが自前で作るのは**リスクレベルを評価し、HIL を必須とする統治層**であり、これは dodoAI 本体の Gate / Capability Routing / HIL 機構の直接応用である。競合が持てない差別化 4 層（生存原理・不可逆性管理・Constraint Graph・IG 校正）は、すべて dodoAI の World Model 5 不変条件と Gate 機構の応用であり、実行層のプレイヤーが後付けで真似るには dodoAI 相当の統治基盤を作り直す必要がある。

### 5.3 還流

実資産を賭けても壊れない統治を実証できれば、それは dodoAI 防衛グレードの最強の Evidence になる。ここで鍛えた Viability / Irreversibility / Crowding Gate・Fractional Kelly サイジング・自動インシデントレスポンスは、汎用化して dodoAI 本体の Agent 統治機構（自律 Agent の権限・資源・不可逆操作の扱い）へ還流する。

## 6. Concept への含意（本書が既存文書に課す制約）

1. **UC / Feature の追加時**: 「Swap 実行」「Yield 最適化」単体を主価値とする Feature を新設しない。それらは §4 の外部レイヤー統合（Adapter 委任）として定義する。Wallet / Signer 機能は dodo-wallet + dodo クレデンシャル機構（CR-1）への統合として定義する。
2. **データモデル**: Opportunity 空間は §3.1 の確度校正フィールド（`confidence_calibration` / `forecast_error` / `counterfactual_return` 等）を将来必須として設計する（詳細は [../2.sdt-design/02-data-model.md](../2.sdt-design/02-data-model.md) が所有）。
3. **評価軸**: 「稼げたか」ではなく「予測が校正されているか」「Counterfactual 比で増分があるか」を一次評価軸とする（[00-overview.md](00-overview.md) 問い 1・2 と整合）。
4. **競合再評価**: 本書の競合認識は Belief であり、四半期程度で再クロール・再評価する（E モニタリング型の観測対象に含める）。
5. **Personal Custom App Policy との整合**: 本書の CIO 構想は single-owner の個人 CIO であり、Strategy Marketplace や multi-tenant 化を含意しない（AGENTS.md / CR-8 に従う）。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.3.1 | 2026-08-22 | Wallet の扱いを訂正: Signer / 鍵管理 / Session Key 統治 / Policy Enforcement は dodo-wallet + dodo クレデンシャル機構（自前）が持ち、外部委任は実行の配管のみと明記（§4 / §5.2 / §6） |
| v0.3.0 | 2026-08-22 | §5「dodoAI 防衛グレードへの寄与」を新設: ゼロトラスト・クリプトが Agent 統治の最過酷テストベッドであること、チェーン（実行層）はやらず「リスクレベル評価 + HIL 必須」の統治層に集中すること、検証成果の dodoAI 本体への還流を明記 |
| v0.2.0 | 2026-08-22 | v0.5 根本改訂に追随: Sovereign Crypto CIO の目的関数を生存原理へ接続し、不可逆性管理・Constraint Graph・Reflexivity 監視を差別化の中核として明記 |
| v0.1.0 | 2026-08-22 | 新設。2026 年時点の競合環境（Giza / Wayfinder / Almanak / Agent Wallet 大手）を踏まえ、「単純な自動運用アプリ」を作らない理由と Sovereign Crypto CIO ポジショニングを記録 |
