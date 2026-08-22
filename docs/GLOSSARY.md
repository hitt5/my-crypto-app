---
type: glossary
title: 用語集（Glossary）— dodo Crypto Wealth OS
tags: [glossary, crypto-wealth-os, terminology]
---

# 用語集（Glossary）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 本プロジェクトの略語・ドメイン用語・固有概念の定義集（人間可読の参照 view）。各用語の**正本は定義元ドキュメント**であり、本書と定義元が矛盾した場合は定義元を正とし本書を同一変更で追随する。
> **記載範囲**: ①要件・開発プロセスの略語 ②コンセプト固有概念 ③データモデルのノード/概念 ④crypto ドメイン用語。個別 Feature の詳細仕様はここに書かない。

## 1. 要件・開発プロセスの略語

| 用語 | 正式名称 | 定義 | 正本 |
|---|---|---|---|
| **BR** | Business Requirement（ビジネス要件） | 事業背景・ゴールから導出される要件。要件 ID は `BR-n`。新設・変更は HIL 裁定必須 | [`3.common/1.business-requirements/`](3.common/1.business-requirements/02-business-requirement.md) |
| **SR** | System Requirement（システム要件） | BR を実現するためのシステム要件。要件 ID は `SR-XXX-n`（XXX = 領域コード: KEY / POL / EXE / EVD / VIA） | [`3.common/2.system-requirements/`](3.common/README.md) |
| **NFR** | Non-Functional Requirement（非機能要件） | セキュリティ・規制・スコープ等の非機能要件。要件 ID は `NFR-XXX-n`（SEC / REG / SCOPE） | [`3.common/2.system-requirements/nfr/`](3.common/README.md) |
| **UC** | Use Case（ユースケース） | Feature 固有の利用シナリオと受入基準。BR → SR → UC の順で定義する。UC と FR は同一フォルダに混在させない | AGENTS.md §Requirements Model |
| **CAP** | Capability（能力） | システム能力の単位。**FR は CAP が所有**し、Feature/UC は `references(satisfies)` で参照のみ | `docs/0.charter/07-requirements-architecture-map.md` |
| **FR** | Functional Requirement（機能要件） | CAP が所有する機能要件。欠落 FR は `fr_gap` で記録。新設は HIL 裁定必須 | 同上 |
| **Mod** | Module（モジュール） | 実装単位。定義順は BR → SR → UC → CAP → Mod が先、コードは後 | 同上 |
| **EPIC** | — | Feature をまとめる最上位の要件グループ。JSON-first SoT（`docs/99.sdt/art/catalog/source/`） | AGENTS.md §Requirements Model |
| **Feature** | — | EPIC 配下の機能単位（例: `F-CRYPTO-PORTFOLIO-DASHBOARD`）。`feature.json` + `task-dd*.json` で TaskGraph 管理する | `docs/99.sdt/agn/1.workflows/` |
| **CR** | Common Requirement（共通要件） | 全 EPIC / Feature に横断適用される共通要件 CR-1〜CR-9。正本は `3.common/0.common-requirements/`、同フォルダ内で BR/SR/NFR へ展開 | [`3.common/0.common-requirements/00-common-requirements.md`](3.common/0.common-requirements/00-common-requirements.md) |
| **HIL** | Human-in-the-Loop | 人間（ユーザー本人）による裁定・承認。BR/SR/NFR/CAP/FR 新設、Policy 変更、不可逆 Action、スコープ拡張等で必須 | [`1.concept/00-overview.md`](1.concept/00-overview.md) §HIL ゲート |
| **HARD / SOFT** | — | HARD = 違反したら実装・実行を拒否する要件 / SOFT = 逸脱時に Finding として記録する要件 | [`3.common/README.md`](3.common/README.md) §記法 |
| **SoT** | Source of Truth（正本） | 唯一の正とするデータ・文書。docs/ ツリーが SoT、`dodoai-docs/` は投影ビュー | AGENTS.md §Instruction Source of Truth |
| **SDT** | — | ART + AGN で構成される機械可読の設計・実行記録ツリー（`docs/99.sdt/`）。ART が正本 SoT、AGN は ART を意味で接続する因果グラフ | `docs/99.sdt/README.md` |
| **SCO** | Semantic Canonical Ontology（意味の正準オントロジー） | SDT の項目と ADF 文書の項目が共通参照する「意味のマスター」。呼称や project 固有語を同じ正準概念へ接続し、ART / AGN / ADF 間で意味を一貫させる。project **scope** の略ではない。新しい正準概念を推測で追加せず、既存概念への写像を優先する | dodoAI `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/glossary.md` §SCO / `docs/99.sdt/agn/0.schema/ontology/` |
| **AGN** | — | SDT のうち、Workflow / Feature / Task / Agent / Skill / Operation を接続する因果グラフ層 | 同上 |
| **ART** | — | SDT のうち、catalog / context / knowledge / operations / test-results 等の成果物（Artifact）層 | 同上 |
| **A02 / A03** | — | ADF の上流工程。A02 = 6 層要件セット + 全体設計（EPIC→FEATURE→UC / CAP→FR→MOD）、A03 = SDT/AGN Conformance Gate（コードを作らない） | AGENTS.md §ADF Work Start Order |
| **DD01–DD05** | Detailed Development phase | ADF の実装工程。DD01 = Scaffold、DD02–03 = 実装、DD04/DD05 = Feature 単位の検証・サーバ検証ゲート | Charter `02-development-flow.md` |
| **ADF** | Agentic Development Framework | AI Agent による開発を構造的に統治し、品質・トレーサビリティ・監査可能性を担保するフレームワーク。本プロジェクトで ADF と言われたら dodoAI の日本語正本を読み、現行工程・Gate は dodoAI Charter の開発フローで確認する | dodoAI `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/` / `/Users/hitoshimurakami/myApps/dodoai/docs/0.charter/02-development-flow.md` |
| **OODA** | Observe–Orient–Decide–Act | 自律実行ループの基本サイクル。全ループ記録に R-1 Scorecard / R-2 Success Probability / R-3 Calibration が必須 | Charter `04-autonomous-loop.md` §8 |
| **Evidence（開発文脈）** | — | Gate 通過・検証結果の証跡。完了主張は Evidence を伴う | AGENTS.md §Completion Gate |
| **Finding** | — | Gate 逸脱・シミュレーション乖離・SOFT 要件違反などの記録。done の代用にしない | AGENTS.md |
| **WM-1〜WM-5** | World Model 不変条件 | 定式化 / エントロピー最小化 / 統治（Fact・Belief・Hypothesis 分離）/ トレーサビリティ / 双対表現（MD + JSON） | AGENTS.md §World Model Representation |

## 2. コンセプト固有概念（大原則・目的関数）

| 用語 | 定義 | 正本 |
|---|---|---|
| **大原則（Prime Directive）** | 不可逆的な損失を避けながら、将来取り得る選択肢（介入可能性）を最大化する。形式: `max E[Δlog W + α·ΔΩ + β·IG] s.t. P(ruin) < ε` | [`1.concept/00-overview.md`](1.concept/00-overview.md) |
| **W** | 資本（金銭的資本）。`Δlog W` は幾何平均成長を表す | 同上 |
| **Ω（Omega / OptionalitySet）** | 将来実行可能な Action 集合（Optionality）。流動性・知識・Reputation・Governance 権限・Protocol access・実験可能性を含む。`ΔΩ` はその増減 | 同上 / [`2.sdt-design/02-data-model.md`](2.sdt-design/02-data-model.md) |
| **IG** | Information Gain（情報利得）。新しい知識・モデル精度・確度校正の改善。Canary は「IG を少額で買う実験」 | [`1.concept/00-overview.md`](1.concept/00-overview.md) |
| **ruin** | 回復不能な破綻（資本・鍵・権利・流動性の不可逆な喪失）。`P(ruin) < ε` が生存制約 | 同上 |
| **ε（epsilon）** | ユーザーが HIL で定義する ruin 確率の上限。ViabilityConstraint の中核数値 | 同上 |
| **α・β** | 目的関数における ΔΩ / IG の係数（テーマ固有値。`mappings/crypto.mapping.json` が置き場） | [`2.sdt-design/02-data-model.md`](2.sdt-design/02-data-model.md) §切り分け |
| **三要素アーキテクチャ** | World Model（何が起こるか）× Viability Model（何を守り増やすか）× Agentic Settlement（契約・署名・決済）。Opportunity は前二者の差分から発生する | [`1.concept/00-overview.md`](1.concept/00-overview.md) |
| **World Model** | 何が起こり得るかを確率分布 × 損益分布 × 不可逆性で予測するモデル。実体経済の Digital Twin ではなく **Minimal Causal World Model**（境界変数のみ） | 同上 |
| **Viability Model（Viability / Value Model）** | どの未来なら生存でき選択肢が増えるかを評価するモデル。Ruin 上限管理・不可逆性最小化・Ω 蓄積を司る | 同上 |
| **Agentic Settlement** | 選択した介入を実際に契約・署名・決済する層。決定論的 Policy Engine と Gate に拘束される | 同上 |
| **Counterfactual Planning** | World Model の「可能な未来」と Viability Model の「望ましい未来」の差分から介入を計画すること。No-action（何もしない）との比較を常に行う | 同上 |
| **H-1 Survival Premium** | 仮説1: 破綻しなかった資本だけが次の大きな機会を取れる。行動可能性の保有自体に価値がある | 同上 §4つの仮説 |
| **H-2 Constraint Alpha** | 仮説2: 収益機会は情報差より「他者が動かざるを得ない地点」（清算・Unlock・償還期限等）に発生する | 同上 |
| **H-3 Convexity** | 仮説3: 正解率より Payoff 構造が重要。確率分布 × 損益分布 × 不可逆性で評価する | 同上 |
| **H-4 Reflexivity** | 仮説4: Agent の予測が行動になり、行動が市場を変える。同一モデル・同一 Policy の混雑がモデル自身の危機を作る | 同上 |
| **不可逆性（Irreversibility）** | 本プロジェクトのリスク第一軸。リスク＝価格変動ではなく「将来の意思決定能力を失うこと」。レベルは 可逆 / 条件付き可逆 / 不可逆 の 3 段階 | 同上 §リスクの再定義 / CR-9.2 |
| **Non-custodial, policy-custodied autonomy** | 資産（秘密鍵）はユーザーが持ち、Agent は期限付き・用途限定の権限と決定論的 Policy Engine に拘束される、という統治形態 | [`1.concept/00-overview.md`](1.concept/00-overview.md) |
| **Observe → Approve → Autopilot** | 自律度の 3 段階。段階昇格は HIL 承認必須（CR-2.5）。Approve（実行前承認）が標準設定 | [`1.concept/03-approach.md`](1.concept/03-approach.md) / CR-2 / CR-7.2 |
| **Fractional Kelly** | サイジング原則: 資金量は確信度ではなく不確実性で制限する。分布の不確実性が大きいほどサイズを縮小する（CR-9.4） | [`2.sdt-design/02-data-model.md`](2.sdt-design/02-data-model.md) RiskBudget |
| **因果分散** | 分散を Token の数ではなく因果の異なりで測る。同一の Stablecoin 発行体・Bridge・Oracle・担保に依存する Position は合算して上限管理する（CR-9.5） | CR-9 |
| **オペレーショナルα** | 数百プロトコルの巡回・期限管理・Claim・Approval 解除など、人間が継続できない運用作業から得られる収益機会 | [`1.concept/00-overview.md`](1.concept/00-overview.md) Before/After |

## 3. データモデルのノード型・概念

> 正本: [`2.sdt-design/02-data-model.md`](2.sdt-design/02-data-model.md)（不変条件を含む完全定義はそちらを参照）

### World Model 空間（外部・予測）

| 用語 | 定義 |
|---|---|
| **BoundaryVariable（境界変数）** | Crypto の State Transition を変える最小限の因果変数（ドル流動性・金利・Stablecoin 供給・Collateral 価値・機関フロー・規制・Protocol 実収益・Unlock・Compute/Energy・決済需要・法人/国家保有）。将来は確率分布で保持（単一点推定禁止） |
| **ConstraintNode** | 市場参加者が「動かざるを得ない」構造的制約（清算水準・Unlock スケジュール・償還期限・Governance 日程等）。Constraint Graph の構成単位。観測可能性等級（`direct` / `proxy` / `structural-prior`）を必ず持つ |
| **Constraint Graph** | ConstraintNode の集合が構成する「誰が・いつ・なぜ強制的に動くか」の構造（H-2 の実装） |
| **CrowdingSignal** | 同一の予測・Policy を持つ参加者の混雑度（H-4 の実装）。TVL 集中度・清算マップ・担保重複・資金フロー相関で観測 |
| **Protocol** | 監視対象の外部プロトコル（Lending・DEX・Staking 等）。理解できない Contract は投資対象にしない |
| **RiskSignal** | 不可逆性イベントの兆候（デペッグ・Oracle 異常・TVL 急減・Admin key 変更等）。発火条件は決定論的な閾値。各シグナルは不可逆性レベルを持つ |
| **Source** | 情報源。信頼度階層: 公式コントラクト > 公式 Governance > 公式ドキュメント > 監査会社 > オンチェーン実測 > 一次情報メディア > SNS > インフルエンサー |

### Viability 空間（内部・正本）

| 用語 | 定義 |
|---|---|
| **ViabilityConstraint（生存制約）** | `P(ruin) < ε` の正本。総損失限度・不可逆性エクスポージャ上限・最低流動性準備・レバレッジ禁止をユーザーが HIL で定義 |
| **Wallet** | 役割別に分離された資金の器: **Vault**（長期保全）/ **Earn**（Lending・Staking）/ **Explore**（Airdrop・新規）/ **Trade**（イベント・価格戦略）。Smart Account（Safe）を基本とする |
| **Asset** | 保有可能なトークン・ポジション原資産。Allowlist 登録済み・複数ソース価格照合済み・因果依存明示が成立条件 |
| **Position** | Wallet 内の具体的な保有・供給・LP 等の状態。オンチェーン実測（Fact）と一致し、取得理由（Evidence 参照）と不可逆性プロファイルを必ず持つ |
| **Policy（投資憲法）** | 機械実行可能な権限・制約の集合（金額上限・Allowlist・スリッページ・レバレッジ禁止・損失限度・回転数上限・失効期限・承認閾値・不可逆性上限）。変更は HIL のみ |
| **RiskBudget** | ε を Wallet・戦略ごとに配分したもの。サイズは Fractional Kelly（不確実性ベース）で制限。同一因果への配分は合算上限管理 |
| **ruin 距離** | 現状態から破綻までのバッファ実測値。閾値を割ったら Guardian 発火 |

### Intervention 空間（差分・実行）

| 用語 | 定義 |
|---|---|
| **Opportunity** | World Model の予測と Viability Model の要求の**差分から機械的に発生する介入仮説**。Convexity 評価・No-action との Counterfactual 比較・期待純収益 > 0 かつ優位性がコストの 3 倍以上、が実行候補の条件 |
| **Execution（Intervention）** | 提案 → ポリシー検査 → シミュレーション → 署名 → 執行の 1 回の介入。結果（Observation）と必ず対になる |
| **StrategyVersion** | 戦略の版。Canary 段階（バックテスト → Paper → 少額 → 制限付き本番 → 増額）を持つ |
| **Canary** | 新戦略の段階的昇格プロセス。IG を少額で買う実験と位置づける。Canary 以外の経路で本番資金に触れない（CR-5.3） |
| **Evidence（投資文脈）** | 判断・評価の根拠記録（Intervention と Observation の対・Source 参照・使用 Agent/モデル/戦略版・予測分布と実績の対）。Ledger は追記のみ・改変禁止 |
| **Fact / Belief / Hypothesis** | 情報の確度分類。Fact = オンチェーン実測等の一次観測 / Belief = 推定 / Hypothesis = 構造的傾向のみ。混ぜて記録しない（WM-3・CR-4.3） |
| **Cross-Graph Edge** | 3 グラフ空間（World Model / Viability / Intervention）をまたぐ影響関係のエッジ。Edge 集合に別のグラフ空間名を与えない |

## 4. crypto ドメイン用語

| 用語 | 定義 |
|---|---|
| **Airdrop** | プロトコルがユーザーへトークンを無償配布すること。Eligibility（受給資格）条件・Claim 期限の管理が Explore Wallet の主対象 |
| **Allowlist** | 取引・呼び出しを許可する銘柄・コントラクトの明示リスト。Allowlist 外の呼び出しは禁止（CR-3.2） |
| **Approval** | ERC-20 等でコントラクトにトークン操作権限を与えること。不要 Approval は攻撃面となるため監視・解除対象 |
| **Bridge** | チェーン間の資産移動機構。停止・ハッキングが不可逆リスクの代表例。Bridge 操作は HIL 必須（CR-9.2） |
| **calldata** | コントラクト呼び出しのエンコード済みデータ。任意 calldata の生成・署名は禁止（CR-3.1、許可済み Adapter 経由のみ） |
| **Claim** | Airdrop・報酬等をオンチェーンで受け取る操作。期限管理と可能検知を Agent が担う |
| **DCA** | Dollar-Cost Averaging（定額積立）。戦略（StrategyVersion）の一種 |
| **DEX** | Decentralized Exchange（分散型取引所） |
| **DID / VC** | Decentralized Identifier / Verifiable Credential。dodo クレデンシャル機構が Agent・承認者の識別に使う |
| **デペッグ（Depeg）** | Stablecoin 等が目標価格（ペッグ）から乖離すること。RiskSignal の代表例 |
| **fork シミュレーション** | チェーン状態を複製した環境でトランザクションを事前実行する検証。署名前に必須（CR-3.4） |
| **ガス（Gas）** | トランザクション実行手数料。期待純収益の控除項・回転数上限の予算項 |
| **Governance** | プロトコルの意思決定機構（proposal・投票）。日程は ConstraintNode、権限は Ω の構成要素 |
| **Kill Switch** | 緊急停止機構。Session Key を即時無効化する（CR-1.4） |
| **Lending** | 貸付プロトコルへの資産供給（Earn Wallet の主対象） |
| **LP** | Liquidity Provider / Liquidity Position。DEX への流動性供給ポジション |
| **Oracle** | オンチェーンに外部価格等を供給する仕組み。単一 Oracle での判断は禁止（CR-3.3）。Oracle 異常は RiskSignal |
| **RPC / インデクサ** | オンチェーンデータの読み取り経路。Position・残高・Approval の実測（Fact）の情報源 |
| **Safe（Smart Account）** | マルチシグ / モジュール拡張可能なスマートコントラクトウォレット。Wallet の基本形。Safe Module 経由で Agent に限定権限を付与 |
| **Session Key** | 期限付き・用途限定の実行権限鍵。Agent が持てる唯一の権限形態（CR-1.1）。必ず失効期限を持つ |
| **Slippage（スリッページ）** | 注文時と執行時の価格乖離。Policy の最大スリッページで制限 |
| **Stablecoin** | 法定通貨等に価値を連動させたトークン。供給量は BoundaryVariable、発行体は因果分散の管理単位 |
| **Staking** | トークンをロックしてネットワーク検証等に参加し報酬を得ること |
| **Sybil farming** | 大量ウォレットによる機械的エアドロップ収穫。本プロジェクトでは行わない（CR-6.4） |
| **Token Unlock** | ロックされたトークンの解除スケジュール。ConstraintNode の代表例（売り圧の予告） |
| **TVL** | Total Value Locked。プロトコルに預けられた資産総額。健全性・混雑度の観測プロキシ |
| **Vesting** | トークンの段階的付与。Vesting コントラクトは Unlock の一次情報源 |
| **Yield** | 利回り機会（Lending 金利・Staking 報酬・インセンティブ等） |

## 5. 統治・運用の固有語（dodoAI 由来）

| 用語 | 定義 | 正本 |
|---|---|---|
| **dodo クレデンシャル機構** | DID/VC による識別 + `env://` 間接参照 + Desktop 内署名処理からなる資格情報の統治層（CR-1 の基本層） | CR-1 |
| **個人ハードウェアモジュール** | ユーザーが物理保持する署名デバイス（ハードウェアウォレット等）。Vault 移動・Policy 変更・高額取引の最終署名に必須（CR-1 の補完層） | CR-1 |
| **`env://` 参照** | 資格情報の間接参照形式。平文直書き禁止（CR-1.2 / P5） | CR-1 |
| **Policy Engine** | 実行可否を決定論的に判断するエンジン。LLM の多数決・確信度ベース判断を用いない（CR-2.4） | CR-2 |
| **Guardian（Agent）** | RiskSignal を監視し、発火時に 新規取引停止 → 権限停止 → Approval 解除 → 退避案 → 人間緊急承認 のフローを実行する内部ロール | [`1.concept/05-multi-agent.md`](1.concept/05-multi-agent.md) / CR-5.6 |
| **Gate** | 工程・実行の通過条件（HARD の場合、未達なら先へ進めない）。開発（Preload / Completion 等）と投資実行（Policy 検査・不可逆性検査等）の両文脈で使う | Charter / AGENTS.md |
| **Personal Custom UI / Custom Action** | dodoAI personal scope（`.dodoai/personal/custom_ui/` / `custom_actions/`）に置く本人専用の UI・Action。本プロダクトの提供形態（CR-8.1） | CR-8 |
| **DRIFTED** | 正本（Policy・目標配分・Wallet 役割）とオンチェーン実態の乖離が検知された状態（モニタリング型 E の検知結果） | [`1.concept/00-overview.md`](1.concept/00-overview.md) §プロジェクトタイプ |
| **Evidence Ledger** | 全判断・実行・リスク判定の根拠を追記のみで記録する台帳。税務記録（取得価格・取引理由）を兼ねる（CR-4） | CR-4 |
| **H0–H4** | HIL ゲートの番号（H0 = Product Form 承認 〜 H4 = 実行承認）。CR の H-1〜H-4（仮説）とは別物 | [`1.concept/00-overview.md`](1.concept/00-overview.md) §HIL ゲート |

---

## 運用ルール

1. **正本優先**: 本書は参照 view。定義の変更はまず正本ドキュメント（Concept / 3.common / Charter）で行い、本書を同一変更で追随させる
2. **追加基準**: 複数ドキュメントにまたがって使われる略語・概念のみ追加する。単一 Feature 内の局所語は Feature 仕様側に書く
3. 新しい概念を追加するときは WM-1（World Model 十要素のどれかを言えること）を確認する

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.0 | 2026-08-22 | SCO を Semantic Canonical Ontology として追加し、ADF の誤った展開を Agentic Development Framework へ修正。dodoAI 正本パスを明記 |
| v0.1.0 | 2026-08-22 | 初版。要件略語（BR/SR/NFR/UC/CAP/FR 等）・コンセプト固有概念（大原則・三要素・4仮説）・データモデルノード型・crypto ドメイン用語・統治固有語を収録 |
