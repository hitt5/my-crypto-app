---
type: design
title: SDT データモデル（3 空間・ノード型・エッジ型・観測）
tags: [crypto-wealth-os, data-model, sdt-design, personal-scope]
---

# 02 — SDT データモデル（最重要）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 本書は **SDT として何を作るか**を定義するデータモデルの正本。`1.concept/` から `2.sdt-design/` へ移設した（旧: `1.concept/04-data-model.md`。concept 側はポインタのみ残す）。
> **標準**: [`../1.concept/README.md`（コンセプト設計標準）](../1.concept/README.md) の C1〜C6 に従う。**全ノード型に不変条件必須**。Edge の別名を独立レイヤーにしない。
> **設計の起点**: [`../1.concept/00-overview.md`](../1.concept/00-overview.md) の三要素アーキテクチャ。タイプ A（前提条件つき仮説＋外部変化）＋ タイプ E（正本＋実態観測）の複合。
> **語彙の統治**: 本書のノード型・エッジ型を SDT の実ノード型として使うための正準化方針は [`03-sco-policy.md`](03-sco-policy.md)（SCO 方針）が所有する。

## グラフ空間の設計

> 起点・時間軸・更新サイクル・確度が根本的に異なる対象群のため、三要素アーキテクチャに対応する **3 空間 + Cross-Graph Edge** に分ける（C3）。

| グラフ空間 | 対応する要素 | 起点 | 性質 | 単位 |
|---|---|---|---|---|
| **World Model 空間**（外部・予測) | World Model | Crypto 市場へ因果的に流入する境界変数と、市場参加者の制約構造 | 低〜中確度（Belief / Hypothesis 中心、**単一予測値禁止・分布必須**）。時間〜日次更新。実体経済の Digital Twin ではなく **Minimal Causal World Model**（境界変数のみ） | BoundaryVariable / ConstraintNode / Protocol / RiskSignal / Source |
| **Viability 空間**（内部・正本） | Viability / Value Model | ユーザーの生存制約（ε）・投資憲法（Policy）と保有資産 | 高確度（オンチェーン実測 = Fact 中心）。即時〜日次更新。正本（Policy・生存制約・目標配分）と実態（W・Ω・ruin 距離・Approval）の差分を監視するモニタリング構造 | Wallet / Position / Policy / RiskBudget / OptionalitySet |
| **Intervention 空間**（差分・実行） | Counterfactual Planning + Agentic Settlement | World Model の「可能な未来」と Viability Model の「望ましい未来」の差分 | Opportunity は Belief（分布・Convexity・校正付き）、Execution は Fact（Intervention/Observation の対）。差分発生〜執行完了のライフサイクルで更新 | Opportunity / Execution / StrategyVersion / Evidence |

影響関係（例: BoundaryVariable の分布変化が Opportunity を発生させる、ConstraintNode が Execution のタイミングを規定する、RiskSignal が Policy の停止条件を発火する）は **Cross-Graph Edge** として表現し、Edge 集合に別のグラフ空間名を与えない（C4）。

## ノード型

> 中核ノード型には「成立条件」と「見直し条件」を不変条件として含める（C1）。

### World Model 空間

| 概念 | 定義 | 不変条件（必須） |
|---|---|---|
| **BoundaryVariable** | Crypto の State Transition を変える最小限の因果変数（世界のドル流動性 / 金利・資金調達コスト / Stablecoin 供給量 / Collateral 価値 / 機関資金流入出 / 規制による行動制約 / Protocol 実収益 / Token Unlock / Compute・Energy 需要 / 決済需要 / 法人・国家の保有動向）。**この集合の外の実体経済変数はモデル化しない**（Minimal Causal 原則） | 成立: Crypto 市場の State Transition への因果経路が明示されていること。現在値は一次情報で観測可能であること。将来は**確率分布**で保持し単一点推定を禁止。見直し: 因果経路が 2 四半期観測されない変数は削除候補（HIL）。新変数の追加は因果経路の立証＋HIL |
| **ConstraintNode** | 市場参加者（Agent・ファンド・Treasury・Market Maker・Protocol・国家）が「動かざるを得ない」構造的制約（清算水準・Unlock スケジュール・Incentive 終了・償還期限・Governance 日程・資本規制・在庫義務・税務期限）。**Constraint Graph の構成単位** — 「何が正しいか」ではなく「誰が・いつ・なぜ強制的に動くか」を保持する（H-2 Constraint Alpha） | 成立: 主体・トリガ条件（価格/日時/量）・強制される行動・推定規模が構造化されていること。**観測可能性等級**（`direct`=オンチェーン一次観測 → Fact / `proxy`=集計値・ラベリングからの推定 → Belief / `structural-prior`=非公開・構造的傾向のみ → Hypothesis。[`../1.concept/01-problem.md`](../1.concept/01-problem.md) §2 補足参照）を必ず持ち、等級と WM-3 分類を混ぜないこと。`direct` のトリガ条件は決定論的に監視可能であること。見直し: トリガの消滅（返済・延期・解除）を観測したら失効。的中実績で ConstraintNode 種別ごとの信頼度を更新（`proxy` / `structural-prior` は的中実績なしに等級を昇格させない） |
| **CrowdingSignal** | 同一の予測・Policy を持つ参加者の混雑度（H-4 Reflexivity）。同じ Protocol への資金集中・同じ価格帯の Stop/清算集中・同じ担保の共有・同型 Agent 戦略の普及度 | 成立: 混雑の観測プロキシ（TVL 集中度・清算マップ・担保重複・資金フロー相関）が定義されていること。見直し: 自身の Policy が混雑側にいると判定されたら該当 Opportunity / Position の再評価を強制発火 |
| **Protocol** | 監視対象の外部プロトコル（Lending・DEX・Staking・新規プロジェクト）。監査状況・Admin key 構成・TVL・実収益・チーム/資金調達情報を持つ | 成立: 一次情報（公式コントラクト・公式ドキュメント・監査レポート）で存在と状態が裏付けられていること。**モデルが理解できない Contract は投資対象にしない**（不可逆性）。見直し: Contract upgrade・Admin key 変更・TVL 急減・脆弱性報告の観測 |
| **RiskSignal** | 不可逆性イベントの兆候（デペッグ・Oracle 異常・TVL 急減・大口流出・Admin key 変更・Governance 攻撃・Bridge/Chain 停止・フロントエンド改ざん・Approval 異常・プロンプトインジェクション・流動性枯渇・混雑発の連鎖清算） | 成立: 発火条件が決定論的な閾値として定義され、一次情報の観測に基づくこと。各シグナルは**不可逆性レベル**（可逆 / 条件付き可逆 / 不可逆）を持つ。見直し: 誤検知率の実績により閾値を HIL で調整（Agent 単独で緩和禁止） |
| **Source** | 情報源（公式コントラクト > 公式 Governance > 公式ドキュメント > 監査会社 > オンチェーン実測 > 一次情報メディア > SNS 投稿 > インフルエンサー の信頼度階層を持つ） | 成立: 信頼度階層のどこに属すか明示され、同じ重みで扱われないこと。見直し: 予測実績（正しかったか）により信頼度スコアを更新 |

### Viability 空間

| 概念 | 定義 | 不変条件（必須） |
|---|---|---|
| **ViabilityConstraint（生存制約）** | 大原則の制約項 `P(ruin) < ε` の正本。総損失限度・不可逆性エクスポージャ上限・最低流動性準備（暴落時に行動可能であるための Liquidity — H-1 Survival Premium）・レバレッジ禁止をユーザーが HIL で定義する | 成立: ε・最低流動性準備率・不可逆性上限が数値で定義され決定論的に検査可能であること。変更は HIL のみ。見直し: ruin 距離（現状態から破綻までのバッファ実測）が閾値を割ったら Guardian 発火 |
| **OptionalitySet（Ω）** | 将来実行可能な Action 集合の棚卸し。金銭的資本以外の介入資源 — 流動性・知識（校正済みモデル）・Reputation・Governance 権限・Protocol access・実験可能性 — を列挙し、増減を追跡する | 成立: 各要素は観測可能なプロキシ（例: 即時換金可能額・access 済み Protocol 数・校正スコア）を持つこと。LLM の自己申告値を書かない（WM-3）。見直し: 介入の事前評価で ΔΩ が負となる Action は Irreversibility Gate の対象 |
| **Wallet** | 役割別に分離された資金の器（Vault=長期保全 / Earn=Lending・Staking / Explore=Airdrop・新規 / Trade=イベント・価格戦略）。Smart Account（Safe）を基本とする | 成立: 各 Wallet は必ず 1 つの役割と自律度（原則手動 / 制限付き自律 / 少額自律 / 厳格上限）を持つ。秘密鍵はノードに保持しない（鍵参照は dodo クレデンシャル機構 + 個人ハードウェアモジュールの外部参照のみ）。見直し: 役割外の資産・取引が観測されたら DRIFTED |
| **Asset** | 保有可能なトークン・ポジション原資産（BTC ラップ資産・ETH・USDC 等） | 成立: Allowlist に登録済みであること。価格は複数ソース照合済みであること。**因果依存（発行体・担保・Bridge・Oracle）が明示されていること**（見かけ上の分散の排除）。見直し: Allowlist から除外・デペッグ・上場廃止を観測したら保有見直し |
| **Position** | Wallet 内の具体的な保有・供給・LP 等の状態（数量・取得価格・取得理由参照付き） | 成立: オンチェーン実測（Fact）と一致していること。取得理由（Evidence 参照）と**不可逆性プロファイル**（ロック期間・出口流動性・清算条件）を必ず持つ。見直し: 実測との乖離、参照する Opportunity の棄却、RiskSignal の発火 |
| **Policy（投資憲法）** | 機械実行可能な権限・制約の集合（日次金額上限・銘柄/プロトコル Allowlist・最大スリッページ・レバレッジ禁止・損失限度・回転数上限・権限失効期限・人間承認閾値・不可逆性上限） | 成立: 全項目が決定論的に検査可能な形式であること。変更は HIL のみ（Agent 自身による変更禁止）。有効期限を必ず持つ。見直し: 失効期限到来・損失限度到達・Guardian の停止発動 |
| **RiskBudget** | Ruin 制約（ε）を Wallet・戦略ごとに配分したもの（投入額・平常時ボラティリティ・最大想定損失・流動性・**因果相関**・回収可能時間を別々に管理） | 成立: 全 Wallet の最大想定損失合計が ViabilityConstraint の総損失限度以内。サイズは確信度ではなく不確実性で制限する（**Fractional Kelly**: 分布の不確実性が大きいほど小さく）。同一因果（同じ Stablecoin・Bridge・Oracle・担保）への配分は合算して上限管理する。見直し: 因果相関上昇・ボラティリティ急変・想定損失超過の観測 |

### Intervention 空間

| 概念 | 定義 | 不変条件（必須） |
|---|---|---|
| **Opportunity** | World Model が予測する「可能な未来」と Viability Model が求める「望ましい未来」の**差分から機械的に発生する介入仮説**（Airdrop 期待・Yield 機会・リバランス条件成立・Constraint イベント・退避）。独立した発想 Agent の自由生成物ではない | 成立: ①発生元の差分（W.M. 予測 × V.M. 要求）が明示されている ②**Convexity 評価**（確率分布 × 損益分布 × 不可逆性）を持ち、単一の期待値・的中率で表現しない ③**No-action との Counterfactual 比較**で優位である ④根拠 Source の信頼度が閾値以上 ⑤実行期限が明示されている ⑥期待純収益（基礎金利＋報酬＋インセンティブ期待値−ガス−スリッページ−ヘッジ費用−税務コスト−期待損失）> 0 かつ優位性がコストの 3 倍以上 — を満たすとき「実行候補」。見直し: 期限超過・前提 Source の失効・分布の再推定で Convexity 消失・CrowdingSignal の混雑判定・Protocol の RiskSignal 発火 |
| **Execution（Intervention）** | 提案 → ポリシー検査 → シミュレーション → 署名 → 執行の 1 回の介入（Agentic Settlement）。Observe/Approve/Autopilot のどの段階かを持つ | 成立: 許可済み Adapter・トランザクションデコード済み・複数価格ソース照合済み・fork シミュレーション通過・Policy 検査通過・**不可逆性レベル検査通過**（不可逆な Action は HIL 必須）の全てを満たしてのみ署名に進む。結果（Observation）と必ず対になる（WM-4）。見直し: シミュレーションと実行結果の乖離 |
| **StrategyVersion** | リバランス・DCA・Yield 等の戦略の版。Canary 段階（バックテスト → Paper → 1万円 → 10万円 → 制限付き本番 → 増額）を持つ。Canary は **IG（情報利得）を少額で買う実験**として位置づける | 成立: 現在の Canary 段階と、その段階での増分利益（対「何もしない」ベンチマーク）・予測校正実績（forecast error）を持つ。見直し: 増分利益がベンチマーク（BTC 保持・ステーブル保持・不作為）を下回り続けたら降格/停止。CrowdingSignal が同型戦略の混雑を示したら再評価 |
| **Evidence** | 判断・評価の根拠記録（Intervention と Observation の対、参照 Source、使用 Agent・モデル・戦略バージョン、予測分布と実績の対 = 校正データ、Counterfactual 実績） | 成立: すべての Execution・Opportunity 評価・RiskSignal 判定は Evidence 参照を必須とする（C2）。予測を伴う Evidence は事後に forecast error と counterfactual_return を追記する（IG の測定単位）。見直し: なし（追記のみ、改変禁止） |

## エッジ型

| 関係 | from → to | 意味 |
|---|---|---|
| `causes` | BoundaryVariable → BoundaryVariable / Protocol / Asset | 因果経路（Minimal Causal World Model の骨格） |
| `forces` | ConstraintNode → Protocol / Asset / CrowdingSignal | 制約が強制行動を生む（Constraint Graph の骨格） |
| `crowds` | CrowdingSignal → StrategyVersion / Opportunity | 混雑が自戦略・機会の前提を脅かす（Cross-Graph） |
| `binds` | ViabilityConstraint → RiskBudget / Policy | 生存制約が予算とポリシーを拘束する |
| `allocates` | Wallet → Asset / Position | Wallet が資産・ポジションを保有する |
| `governs` | Policy → Wallet / Execution | ポリシーが Wallet と全実行を拘束する（全 Execution は必ずいずれかの Policy に governs される） |
| `budgets` | RiskBudget → Wallet / StrategyVersion | Ruin 制約配分を割り当てる |
| `expands` / `contracts` | Execution / Position → OptionalitySet | 介入・保有が Ω を増減させる（ΔΩ の追跡、Cross-Graph） |
| `derives_from` | Opportunity → BoundaryVariable / ConstraintNode / ViabilityConstraint | 機会がどの差分から発生したか（発生元必須、Cross-Graph） |
| `proposes` | Opportunity → Execution | 機会が実行案を生む（Cross-Graph） |
| `targets` | Opportunity → Protocol / Asset | 機会の対象 |
| `threatens` | RiskSignal → Protocol / Position / Asset / OptionalitySet | 不可逆性イベントが対象を脅かす（Cross-Graph） |
| `halts` | RiskSignal → Policy | 危険がポリシーの停止条件を発火する（Cross-Graph） |
| `supports` / `contradicts` | Source → Opportunity / RiskSignal / BoundaryVariable | 情報源が仮説を支持/反証する |
| `evidenced_by` | Execution / Opportunity / RiskSignal → Evidence | 根拠参照（必須） |
| `executed_as` | StrategyVersion → Execution | 戦略版が実行を生成した |
| `results_in` | Execution → Position / Observation | 実行が状態変化を生む（Intervention と Observation の対） |

## 観測（Signal / Source）

| 観測対象（ノード/前提） | 情報源（一次情報） | 頻度 | 検証するもの |
|---|---|---|---|
| BoundaryVariable（ドル流動性・金利・Stablecoin 供給・Collateral 価値・機関フロー・規制・Protocol 実収益・Unlock・Compute/Energy・決済需要・法人/国家保有） | 中央銀行統計・金利市場・Stablecoin 発行体・オンチェーン供給量・ETF フロー・規制当局発表・Protocol 決算・Unlock カレンダー | 日次〜週次 | 因果変数の分布更新。World Model の予測分布の前提 |
| ConstraintNode（清算水準・Unlock・Incentive 終了・償還期限・Governance 日程・在庫義務） | 清算マップ（Lending Protocol 実測）・Vesting コントラクト・Incentive 告知・Governance カレンダー | 時間〜日次 | 「誰が・いつ・なぜ動かざるを得ないか」の予告と的中検証 |
| CrowdingSignal（混雑度） | TVL 集中度・清算価格帯分布・担保重複・資金フロー相関・同型戦略の普及観測 | 日次 | 自 Policy の混雑側判定・Reflexivity リスク |
| Position・Wallet 残高・Approval・ruin 距離 | オンチェーン実測（RPC / インデクサ） | 即時〜時間毎 | 正本（目標配分・Policy・ViabilityConstraint）との乖離、不要 Approval、不審トークン |
| Asset 価格・因果依存 | 複数価格オラクル・複数ソース照合（単一オラクル禁止） | 即時 | デペッグ・Oracle 異常・リバランス条件・因果相関の変化 |
| Protocol 健全性 | 公式コントラクト状態・TVL・金利曲線・監査レポート・脆弱性情報 | 時間〜日次 | Contract upgrade・Admin key 変更・TVL 急減・脆弱性（不可逆性イベント） |
| Opportunity 前提 | 公式ドキュメント・Governance proposal・GitHub リリース/コミット | 日次 | Eligibility 条件・期限・報酬変更・仮説の成立/棄却 |
| Airdrop / Claim | 公式アナウンス・オンチェーン Claim コントラクト | 日次＋期限前強化 | Claim 可能検知・期限管理 |
| StrategyVersion 実績・予測校正 | Evidence Ledger（自己の実行記録・予測分布と実績の対）＋ベンチマーク（BTC 保持・ステーブル保持・不作為） | 週次 | 増分利益（対 No-action）・forecast error・最大ドローダウン・Canary 昇格/降格判定 = IG の実測 |
| OptionalitySet（Ω） | 即時換金可能額・access 済み Protocol・権限一覧・校正スコア | 週次 | ΔΩ の実測（介入可能性が増えているか — 00 問い 3） |
| Source 信頼度 | 過去の supports/contradicts の的中実績 | 月次 | 信頼度スコアの更新 |

## 共通概念 / 固有語彙の切り分け

> 本節の切り分けを SDT の実ノード型・写像として統治する具体的方針（Core SCO / Domain SCO Package / STM mapping・lifecycle・検証 Action）は [`03-sco-policy.md`](03-sco-policy.md) が所有する。

| 分類 | 置き場 |
|---|---|
| 共通概念（ドメイン非依存）: Entity / State / Relation / Constraint / Goal / Intervention / Observation / Evidence / Fact / Belief / Hypothesis | 共通概念パッケージ = **Core SCO**（据え置き・変更しない） |
| 固有語彙・固有値（テーマ固有）: 目的関数の係数（α・β・ε）、境界変数リスト、ConstraintNode 種別、不可逆性レベル、Wallet 役割（Vault/Earn/Explore/Trade）、Policy 項目、信頼度階層、期待純収益の式、Convexity 評価式、Fractional Kelly 係数、RiskSignal 種別、Canary 段階 | 写像 `mappings/crypto.mapping.json`（STM mapping）+ **Domain SCO Package**（`crypto-wealth-sco-package` — [`03-sco-policy.md`](03-sco-policy.md) 参照） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.5.0 | 2026-08-22 | `1.concept/04-data-model.md` から `2.sdt-design/` へ移設（SDT 設計の正本化）。SCO 方針（03-sco-policy.md）への接続を追加 |
| v0.4.1 | 2026-08-22 | ConstraintNode に観測可能性等級（direct / proxy / structural-prior）を不変条件として追加（01-problem.md §2 補足と対、WM-3 準拠） |
| v0.4.0 | 2026-08-22 | **根本改訂**: 2 空間 → 三要素対応の 3 空間（World Model / Viability / Intervention）へ再設計。BoundaryVariable（Minimal Causal）・ConstraintNode（Constraint Graph）・CrowdingSignal（Reflexivity）・ViabilityConstraint（P(ruin)<ε）・OptionalitySet（Ω）を新設。Opportunity を W.M.×V.M. の差分生成に再定義し Convexity / Counterfactual を不変条件化。RiskBudget に Fractional Kelly と因果相関を導入 |
| v0.3.0 | 2026-08-22 | crypto.md を元に 2 グラフ空間・ノード/エッジ型・不変条件・観測を記入 |
| v0.2.0 | {{DATE}} | 汎用化: グラフ空間を「分割必須」から「必要時のみ分割」へ。観測（Signal/Source）セクションを追加 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
