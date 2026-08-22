# 05 — マルチ Agent（評価・レビューの中核）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **標準**: [`README.md`（コンセプト設計標準）](README.md) の品質バーに従う。各 Gate が何を守るかを明記する。

## Agent 構成

標準 5 役（Orchestrator / Researcher / Analyst / Critic / Integrator）をテーマに写像し、ドメイン Agent を追加する。**複数 Agent の多数決にはしない。最終可否は LLM ではなく決定論的な Policy Engine（Gate）が判断する。**

| Agent | 標準役割の写像 | 役割 |
|---|---|---|
| Orchestrator | Orchestrator | 司会・論点割当・収束。Observe / Approve / Autopilot の段階管理 |
| Opportunity Agent | Researcher | Web・GitHub・オンチェーンを横断クロールし、機会（Airdrop / Yield / イベント）を Source 信頼度付きで Opportunity 空間へ登録 |
| Base Portfolio Agent | Analyst | 目標配分との乖離検知・リバランス/DCA 提案。相場を当てず「条件成立」の機械判断のみ |
| Yield Agent | Analyst | 期待純収益（ガス・スリッページ・ヘッジ費用・期待損失込み）で Lending / Staking / LP を評価。表面 APY 比較を禁止 |
| Airdrop Agent | Analyst | Eligibility 構造化・期待値計算・期限管理・Claim 検知。Sybil farming は行わない（正規利用の最適化のみ） |
| Risk Agent | Critic | VaR・ドローダウン・デペッグ・プロトコルリスクの評価。提案への構造的批判 |
| Red Agent | Critic | 「その取引が失敗する条件」を攻撃的に検証（操作相場・誤情報・プロンプトインジェクション耐性を含む） |
| Guardian Agent | Critic（常駐監視） | RiskSignal の常時監視。発火時は 新規取引停止 → Agent 権限停止 → Approval 解除 → 退避案作成 → 人間へ緊急承認依頼 |
| Execution Agent | Integrator | Gate を全通過した取引のみを、許可済み Adapter・限定権限（Session Key / Safe Module）で執行 |
| Auditor Agent | Integrator | 根拠・署名・結果を Evidence Ledger へ記録。増分利益（対・不作為ベンチマーク）を測定 |

## Gate（議論を資産にする仕組み）

| Gate | 守るもの |
|---|---|
| 引用 Gate | 出典なき判定をリジェクト。Source の信頼度階層（公式コントラクト > … > SNS > インフルエンサー）未満の根拠だけでは実行候補にしない。SNS 投稿を直接売買シグナルにしない |
| **Policy Gate（決定論的 Policy Engine）** | 最終可否を LLM に出させない。金額上限・Allowlist・スリッページ・レバレッジ禁止・損失限度・権限失効を機械検査。Agent 自身による Policy 変更を禁止 |
| **Key Gate（鍵の分離）** | 秘密鍵を Agent に渡さない。鍵は dodo クレデンシャル機構＋個人ハードウェアモジュールの二層で保持し、Agent は期限付き Session Key / Safe Module 権限のみ。任意 calldata の生成・署名を禁止 |
| **Simulation Gate** | 署名前に許可済み Adapter → トランザクションデコード → 複数価格ソース照合 → fork シミュレーション → Policy 検査のパイプラインを固定。未検証コントラクト呼び出しを遮断 |
| **回転数 Gate** | 1日取引回数・月間売買代金・ガス予算・スリッページ予算・同一戦略の再実行間隔に上限。市場ノイズへの反応し続けを防ぐ。デフォルトは「何もしない」 |
| **Canary Gate** | 新戦略はバックテスト → Paper → 少額 → 制限付き本番 → 増額の段階でのみ昇格。増分利益がベンチマーク未満なら降格/停止 |
| HIL Gate | 人間承認まで結論を SoT に書かない。Approve 段階の全取引・閾値超過取引・緊急退避・Policy 変更は人間承認必須 |
| Risk Gate | 高リスク自動実行を防止。Guardian の RiskSignal 発火中は新規取引を全停止 |
| 更新経路 Gate | 成果物（Policy・Position・Evidence）の更新は正規経路のみ。Evidence は追記のみで改変禁止 |
| 増殖 Gate | 再評価は旧成果物を置換（Opportunity の重複起票・無限増殖を防ぐ） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.0 | 2026-08-22 | crypto.md を元に Agent 構成（10 Agent）と Gate（10 Gate）を記入。Key Gate に鍵の二層構成を明記 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
