# 04 — 概念データモデル（最重要）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **標準**: [`README.md`（コンセプト設計標準）](README.md) に従う。**全ノード型に不変条件必須**。Edge の別名を独立レイヤーにしない。
> **設計の起点**: タイプ A（前提条件つき仮説＋外部変化）＋ タイプ E（正本＋実態観測）の複合。

## グラフ空間の設計

> 起点・時間軸・更新サイクル・確度が根本的に異なる対象群のため、**2 空間 + Cross-Graph Edge** に分ける（C3）。

| グラフ空間 | 起点 | 性質 | 単位 |
|---|---|---|---|
| **Portfolio 空間**（内部・正本） | ユーザーの投資憲法（Policy）と保有資産 | 高確度（オンチェーン実測 = Fact 中心）。即時〜日次更新。正本（Policy・目標配分）と実態（残高・Position・Approval）の差分を監視するモニタリング構造 | Wallet / Position / Policy / Execution |
| **Opportunity 空間**（外部・仮説） | クロール・観測で発見される外部世界の機会とリスク | 低〜中確度（Belief / Hypothesis 中心、confidence 付き）。クロールサイクル（時間〜日次）で更新。前提条件つき仮説として成立/棄却が検証される | Protocol / Opportunity / RiskSignal / Source |

影響関係（例: Opportunity が Position を提案する、RiskSignal が Policy の停止条件を発火する）は **Cross-Graph Edge** として表現し、Edge 集合に別のグラフ空間名を与えない（C4）。

## ノード型

> 中核ノード型には「成立条件」と「見直し条件」を不変条件として含める（C1）。

### Portfolio 空間

| 概念 | 定義 | 不変条件（必須） |
|---|---|---|
| **Wallet** | 役割別に分離された資金の器（Vault=長期保全 / Earn=Lending・Staking / Explore=Airdrop・新規 / Trade=イベント・価格戦略）。Smart Account（Safe）を基本とする | 成立: 各 Wallet は必ず 1 つの役割と自律度（原則手動 / 制限付き自律 / 少額自律 / 厳格上限）を持つ。秘密鍵はノードに保持しない（鍵参照は dodo クレデンシャル機構 + 個人ハードウェアモジュールの外部参照のみ）。見直し: 役割外の資産・取引が観測されたら DRIFTED |
| **Asset** | 保有可能なトークン・ポジション原資産（BTC ラップ資産・ETH・USDC 等） | 成立: Allowlist に登録済みであること。価格は複数ソース照合済みであること。見直し: Allowlist から除外・デペッグ・上場廃止を観測したら保有見直し |
| **Position** | Wallet 内の具体的な保有・供給・LP 等の状態（数量・取得価格・取得理由参照付き） | 成立: オンチェーン実測（Fact）と一致していること。取得理由（Evidence 参照）を必ず持つ。見直し: 実測との乖離、参照する Opportunity の棄却、RiskSignal の発火 |
| **Policy（投資憲法）** | 機械実行可能な権限・制約の集合（日次金額上限・銘柄/プロトコル Allowlist・最大スリッページ・レバレッジ禁止・損失限度・回転数上限・権限失効期限・人間承認閾値） | 成立: 全項目が決定論的に検査可能な形式であること。変更は HIL のみ（Agent 自身による変更禁止）。有効期限を必ず持つ。見直し: 失効期限到来・損失限度到達・Guardian の停止発動 |
| **RiskBudget** | Wallet・戦略ごとの損失可能額の配分（投入額・平常時ボラティリティ・最大想定損失・流動性・相関・回収可能時間を別々に管理） | 成立: 全 Wallet の最大想定損失合計がユーザー設定の総損失限度以内。見直し: 相関上昇・ボラティリティ急変・想定損失超過の観測 |
| **Execution（Intervention）** | 提案 → ポリシー検査 → シミュレーション → 署名 → 執行の 1 回の介入。Observe/Approve/Autopilot のどの段階かを持つ | 成立: 許可済み Adapter・トランザクションデコード済み・複数価格ソース照合済み・fork シミュレーション通過・Policy 検査通過の全てを満たしてのみ署名に進む。結果（Observation）と必ず対になる（WM-4）。見直し: シミュレーションと実行結果の乖離 |
| **StrategyVersion** | リバランス・DCA・Yield 等の戦略の版。Canary 段階（バックテスト → Paper → 1万円 → 10万円 → 制限付き本番 → 増額）を持つ | 成立: 現在の Canary 段階と、その段階での増分利益（対「何もしない」ベンチマーク）の実績を持つ。見直し: 増分利益がベンチマーク（BTC 保持・ステーブル保持・不作為）を下回り続けたら降格/停止 |

### Opportunity 空間

| 概念 | 定義 | 不変条件（必須） |
|---|---|---|
| **Protocol** | 監視対象の外部プロトコル（Lending・DEX・Staking・新規プロジェクト）。監査状況・Admin key 構成・TVL・チーム/資金調達情報を持つ | 成立: 一次情報（公式コントラクト・公式ドキュメント・監査レポート）で存在と状態が裏付けられていること。見直し: Contract upgrade・Admin key 変更・TVL 急減・脆弱性報告の観測 |
| **Opportunity** | 前提条件つき仮説としての機会（Airdrop 期待・Yield 機会・リバランス条件成立・イベント）。期待純収益 =（基礎金利＋報酬＋インセンティブ期待値−ガス−スリッページ−ヘッジ費用−税務コスト−期待損失）を必ず持つ | 成立: ①期待純収益 > 0 ②優位性がコストの 3 倍以上 ③根拠 Source の信頼度が閾値以上 ④実行期限が明示されている、を満たすとき「実行候補」。見直し: 期限超過・前提 Source の失効・期待純収益の再計算でマイナス化・Protocol の RiskSignal 発火 |
| **RiskSignal** | 危険の兆候（デペッグ・Oracle 異常・TVL 急減・大口流出・Admin key 変更・Governance 攻撃・Bridge/Chain 停止・フロントエンド改ざん・Approval 異常・プロンプトインジェクション） | 成立: 発火条件が決定論的な閾値として定義され、一次情報の観測に基づくこと。見直し: 誤検知率の実績により閾値を HIL で調整（Agent 単独で緩和禁止） |
| **Source** | 情報源（公式コントラクト > 公式 Governance > 公式ドキュメント > 監査会社 > オンチェーン実測 > 一次情報メディア > SNS 投稿 > インフルエンサー の信頼度階層を持つ） | 成立: 信頼度階層のどこに属すか明示され、同じ重みで扱われないこと。見直し: 予測実績（正しかったか）により信頼度スコアを更新 |
| **Evidence** | 判断・評価の根拠記録（Intervention と Observation の対、参照 Source、使用 Agent・モデル・戦略バージョン） | 成立: すべての Execution・Opportunity 評価・RiskSignal 判定は Evidence 参照を必須とする（C2）。見直し: なし（追記のみ、改変禁止） |

## エッジ型

| 関係 | from → to | 意味 |
|---|---|---|
| `allocates` | Wallet → Asset / Position | Wallet が資産・ポジションを保有する |
| `governs` | Policy → Wallet / Execution | ポリシーが Wallet と全実行を拘束する（全 Execution は必ずいずれかの Policy に governs される） |
| `budgets` | RiskBudget → Wallet / StrategyVersion | 損失可能額を配分する |
| `proposes` | Opportunity → Execution | 機会が実行案を生む（Cross-Graph） |
| `targets` | Opportunity → Protocol / Asset | 機会の対象 |
| `threatens` | RiskSignal → Protocol / Position / Asset | 危険が対象を脅かす（Cross-Graph） |
| `halts` | RiskSignal → Policy | 危険がポリシーの停止条件を発火する（Cross-Graph） |
| `supports` / `contradicts` | Source → Opportunity / RiskSignal | 情報源が仮説を支持/反証する |
| `evidenced_by` | Execution / Opportunity / RiskSignal → Evidence | 根拠参照（必須） |
| `executed_as` | StrategyVersion → Execution | 戦略版が実行を生成した |
| `results_in` | Execution → Position / Observation | 実行が状態変化を生む（Intervention と Observation の対） |

## 観測（Signal / Source）

| 観測対象（ノード/前提） | 情報源（一次情報） | 頻度 | 検証するもの |
|---|---|---|---|
| Position・Wallet 残高・Approval | オンチェーン実測（RPC / インデクサ） | 即時〜時間毎 | 正本（目標配分・Policy）との乖離、不要 Approval、不審トークン |
| Asset 価格 | 複数価格オラクル・複数ソース照合（単一オラクル禁止） | 即時 | デペッグ・Oracle 異常・リバランス条件 |
| Protocol 健全性 | 公式コントラクト状態・TVL・金利曲線・監査レポート・脆弱性情報 | 時間〜日次 | Contract upgrade・Admin key 変更・TVL 急減・脆弱性 |
| Opportunity 前提 | 公式ドキュメント・Governance proposal・GitHub リリース/コミット | 日次 | Eligibility 条件・期限・報酬変更・仮説の成立/棄却 |
| Airdrop / Claim | 公式アナウンス・オンチェーン Claim コントラクト | 日次＋期限前強化 | Claim 可能検知・期限管理 |
| 市場・フロー | Token unlock・Treasury 移動・ブリッジ流出入・大口ウォレット・Stablecoin 供給量・CEX 入出金 | 時間〜日次 | イベントα・リスク回避αの兆候 |
| StrategyVersion 実績 | Evidence Ledger（自己の実行記録）＋ベンチマーク（BTC 保持・ステーブル保持・不作為） | 週次 | Agent 介入の増分利益・最大ドローダウン・Canary 昇格/降格判定 |
| Source 信頼度 | 過去の supports/contradicts の的中実績 | 月次 | 信頼度スコアの更新 |

## 共通概念 / 固有語彙の切り分け

| 分類 | 置き場 |
|---|---|
| 共通概念（ドメイン非依存）: Entity / State / Relation / Constraint / Goal / Intervention / Observation / Evidence / Fact / Belief / Hypothesis | 共通概念パッケージ（据え置き） |
| 固有語彙・固有値（テーマ固有）: Wallet 役割（Vault/Earn/Explore/Trade）、Policy 項目（スリッページ上限等）、信頼度階層、期待純収益の式、RiskSignal 種別、Canary 段階 | 写像 `mappings/crypto.mapping.json`（ここへ吸収） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.3.0 | 2026-08-22 | crypto.md を元に 2 グラフ空間・ノード/エッジ型・不変条件・観測を記入 |
| v0.2.0 | {{DATE}} | 汎用化: グラフ空間を「分割必須」から「必要時のみ分割」へ。観測（Signal/Source）セクションを追加 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
