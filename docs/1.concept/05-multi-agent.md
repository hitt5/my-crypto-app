---
type: concept
---

# 05 — マルチ Agent（評価・レビューの中核）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **標準**: [`README.md`（コンセプト設計標準）](README.md) の品質バーに従う。各 Gate が何を守るかを明記する。
> **上位原理**: Agent は [`00-overview.md`](00-overview.md) の三要素（World Model / Viability Model / Agentic Settlement）に写像される。発想専任の「Creative Agent」は置かない — Opportunity は W.M.×V.M. の差分から機械生成される。

## Agent 構成

標準 5 役（Orchestrator / Researcher / Analyst / Critic / Integrator）をテーマに写像し、ドメイン Agent を追加する。**複数 Agent の多数決にはしない。最終可否は LLM ではなく決定論的な Policy Engine（Gate）が判断する。**

| Agent | 三要素の写像 | 標準役割の写像 | 役割 |
|---|---|---|---|
| Orchestrator | 全体 | Orchestrator | 司会・論点割当・収束。Observe / Approve / Autopilot の段階管理 |
| World Model Agent | World Model | Researcher | 境界変数（BoundaryVariable）の観測・分布更新。単一予測値を出さない（分布必須）。ファンダ・テクニカル・Positioning の 3 軸を統合する |
| Constraint Agent | World Model | Researcher | Constraint Graph の構築・更新。「誰が・いつ・なぜ動かざるを得ないか」（清算・Unlock・償還・Governance 日程）を構造化し、Constraint イベントを予告する（H-2） |
| Crowding Agent | World Model | Researcher | 同一予測・同一 Policy の混雑度（CrowdingSignal）を観測。自戦略が混雑側にいるときは該当 Opportunity の再評価を発火する（H-4 Reflexivity） |
| Opportunity Agent | W.M.×V.M. 差分 | Researcher | Web・GitHub・オンチェーンを横断クロールし、W.M. の予測分布と V.M. の要求の差分から Opportunity（Airdrop / Yield / Constraint イベント / 退避）を Source 信頼度・`derives_from` 付きで Intervention 空間へ登録 |
| Viability Agent | Viability Model | Analyst | 生存制約の常時評価: ruin 距離・流動性準備率・不可逆性エクスポージャ・Ω（OptionalitySet）の増減を実測し、目標配分との乖離（DRIFTED）を検知。リバランス/DCA 提案は相場を当てず「条件成立」の機械判断のみ |
| Yield Agent | 評価（Convexity） | Analyst | 期待純収益（ガス・スリッページ・ヘッジ費用・期待損失込み）と分布ベースの Convexity で Lending / Staking / LP を評価。表面 APY 比較を禁止 |
| Airdrop Agent | 評価（Convexity） | Analyst | Eligibility 構造化・期待値分布・期限管理・Claim 検知。Sybil farming は行わない（正規利用の最適化のみ） |
| Risk Agent | Viability Model | Critic | 不可逆性・因果相関・Fractional Kelly サイズ・VaR・ドローダウン・デペッグ・プロトコルリスクの評価。「この介入は将来の意思決定能力を毀損しないか」を第一の問いとする |
| Red Agent | 反証 | Critic | 「その取引が失敗する条件」を攻撃的に検証（操作相場・誤情報・プロンプトインジェクション耐性・混雑時の退避可能性を含む） |
| Guardian Agent | Viability Model（常駐） | Critic（常駐監視） | RiskSignal（不可逆性イベント）と ruin 距離の常時監視。発火時は 新規取引停止 → Agent 権限停止 → Approval 解除 → 退避案作成 → 人間へ緊急承認依頼 |
| Execution Agent | Agentic Settlement | Integrator | Gate を全通過した取引のみを、許可済み Adapter・限定権限（Session Key / Safe Module）で執行 |
| Auditor Agent | 学習（IG） | Integrator | 根拠・署名・結果を Evidence Ledger へ記録。増分利益（対・不作為ベンチマーク）・forecast error（予測校正）・ΔΩ を測定し、両モデルへ較正フィードバックを返す |

## Gate（議論を資産にする仕組み）

| Gate | 守るもの |
|---|---|
| 引用 Gate | 出典なき判定をリジェクト。Source の信頼度階層（公式コントラクト > … > SNS > インフルエンサー）未満の根拠だけでは実行候補にしない。SNS 投稿を直接売買シグナルにしない |
| **Viability Gate（生存制約）** | すべての実行候補に対し P(ruin) < ε・最低流動性準備率・不可逆性エクスポージャ上限を決定論的に検査。生存制約を毀損する介入は期待収益に関わらずリジェクト（H-1） |
| **Irreversibility Gate（不可逆性）** | 不可逆性レベル（可逆 / 条件付き可逆 / 不可逆）を全 Execution に付与。不可逆な Action（資金ロック・権限付与・Bridge・理解不能 Contract）は自律度に関わらず HIL 必須。ΔΩ が負の Action を厳格化 |
| **No-action Counterfactual Gate** | 「何もしない場合」との比較を全実行候補に強制。優位が示せない介入はリジェクト。デフォルトは「何もしない」 |
| **Sizing Gate（Fractional Kelly）** | 資金量を確信度ではなく不確実性で制限。分布の不確実性が大きいほどサイズを縮小。同一因果（同じ Stablecoin・Bridge・Oracle・担保）への配分は合算上限で検査（見かけ上の分散の排除） |
| **Crowding Gate（Reflexivity）** | CrowdingSignal が自 Policy の混雑を示す Opportunity / 退避経路の実行を保留し再評価を強制。「皆と同じモデルで皆と同じ行動」を構造的に抑制（H-4） |
| **Policy Gate（決定論的 Policy Engine）** | 最終可否を LLM に出させない。金額上限・Allowlist・スリッページ・レバレッジ禁止・損失限度・権限失効を機械検査。Agent 自身による Policy 変更を禁止 |
| **Key Gate（鍵の分離）** | 秘密鍵を Agent に渡さない。鍵は dodo クレデンシャル機構＋個人ハードウェアモジュールの二層で保持し、Agent は期限付き Session Key / Safe Module 権限のみ。任意 calldata の生成・署名を禁止 |
| **Simulation Gate** | 署名前に許可済み Adapter → トランザクションデコード → 複数価格ソース照合 → fork シミュレーション → Policy 検査のパイプラインを固定。未検証コントラクト呼び出しを遮断 |
| **回転数 Gate** | 1日取引回数・月間売買代金・ガス予算・スリッページ予算・同一戦略の再実行間隔に上限。市場ノイズへの反応し続けを防ぐ |
| **Canary Gate** | 新戦略はバックテスト → Paper → 少額 → 制限付き本番 → 増額の段階でのみ昇格（Canary = IG を少額で買う実験）。増分利益がベンチマーク未満なら降格/停止 |
| HIL Gate | 人間承認まで結論を SoT に書かない。Approve 段階の全取引・閾値超過取引・不可逆 Action・緊急退避・Policy / ViabilityConstraint 変更は人間承認必須 |
| Risk Gate | 高リスク自動実行を防止。Guardian の RiskSignal 発火中は新規取引を全停止 |
| 更新経路 Gate | 成果物（Policy・Position・Evidence）の更新は正規経路のみ。Evidence は追記のみで改変禁止 |
| 増殖 Gate | 再評価は旧成果物を置換（Opportunity の重複起票・無限増殖を防ぐ） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.3.0 | 2026-08-22 | **根本改訂**: Agent を三要素（World Model / Viability Model / Agentic Settlement）へ写像。World Model / Constraint / Crowding / Viability Agent を新設（14 Agent）。Viability / Irreversibility / No-action Counterfactual / Sizing / Crowding Gate を新設（15 Gate）。Auditor に予測校正・ΔΩ 測定を追加 |
| v0.2.0 | 2026-08-22 | crypto.md を元に Agent 構成（10 Agent）と Gate（10 Gate）を記入。Key Gate に鍵の二層構成を明記 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
