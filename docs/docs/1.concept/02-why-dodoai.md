# 02 — なぜ dodoAI か（dodoAI の強みと使い方のポイント）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **標準**: [`README.md`（コンセプト設計標準）](README.md) の品質バーに従う。
> ⚠️ 本ファイルの「dodoAI の強み」「使い方のポイント」は **テーマに依らず固定**。書き換えるのは「このテーマでの効き所」「この手段が最適である理由」のみ。
> 出典: dodoAI 本体リポジトリの一次情報（開発憲章・World Model 正本群）に基づく。テーマ固有の運用語彙はここに書かず、下部の「このテーマでの効き所」へ隔離する。

---

## dodoAI の強み（他の手段との違い）

| dodoAI 能力 | 何ができるか | 表計算・静的レポートとの違い |
|---|---|---|
| **SDT（Semantic Digital Twin）** | 対象（仮説・前提条件・要因・関係）を Entity/State/Relation/Constraint/Goal を持つ意味的な状態として保持し、構造そのものを更新し続ける | 表やスライドは書いた瞬間から古くなる。SDT は「今どうなっているか」を常に指し示す一次構造そのもの |
| **Fact / Belief / Hypothesis の分離統治** | 観測済みの事実・確度（confidence）付きの推定・未検証の仮説を明確に区別して記録する | 「なんとなく確からしい」情報がいつの間にか事実として扱われるリスクを構造的に排除する |
| **Evidence = Provenance（介入と観測の対）** | すべての判断・変更（Intervention）とその結果（Observation）を一次情報の参照込みで記録する | 「なぜそう判断したか」を後から遡れる。記録は監査ログではなく、次の判断のための材料になる |
| **Multi-Agent（役割分担レビュー）** | 影響評価・妥当性検証を役割分担した複数 Agent の議論として実行する | 1人・1視点のレビューに依存せず、反証・批判の視点を構造的に組み込める |
| **HIL（Human override）** | 最終的な承認・停止・修正の権限を常に人間に残す | 「AI がなんとなく決めた」を防ぎ、AI の提案と人間の意思決定の境界を明確に分離する |
| **Domain Universality（適用対象を選ばない）** | 状態・目標・制約・因果という同じ表現構造を、対象領域が変わっても使い回せる | テーマごとに評価の型をゼロから作り直さずに済む。戦略検討・業務改善・リサーチ・プロダクト開発・モニタリングなど幅広く転用できる（ルート README §1.1 のプロジェクトタイプ参照） |

---

## 使い方のポイント

- **前提条件・仮説は必ず Constraint（守るべき条件）と Goal（目標状態）を明示して登録する。** 「いつまでに成立させるべきか」「何を満たせなくなったら見直すか」が言語化されていない前提は、崩れても誰も気づけない。
- **観測（Observation）の元になる情報源を先に決めてから運用を始める。** どの情報を見て前提を検証するかが曖昧なまま運用を始めると、判断の根拠が積み上がらない。
- **Multi-Agent の議論は評価軸を決めて終わらせる。** 曖昧な合議で終わらせず、SDT に書き戻せる形（関係の追加・状態変更の提案）に必ず着地させる。
- **HIL ゲートを飛ばさない。** Agent が出すのはあくまで意思決定の「案」。確定は人間が行う運用を崩さない。
- **根拠（Evidence）のない判断・評価は正本データに混ぜない。** 根拠不明の情報が構造に混入すると、後から真偽の切り分けができなくなる。

---

## dodo Core MCP の概要（このテーマの実行基盤）

dodoAI の能力には **dodo Core の MCP（Model Context Protocol）Gateway** を通じてアクセスする。エディタ / Agent / CLI は MCP クライアントとして dodo Core に接続し、Action Registry に登録された Action を `dodo_action_dispatch` で実行する。

| MCP 構成要素 | 概要 | このテーマでの位置づけ |
|---|---|---|
| **`dodo_project_bootstrap`** | セッション開始時に 1 回呼ぶ一括ブートストラップ。ワークスペース文脈・ルール（AGENTS.md）・アクティブ Issue 候補を bounded payload で返す | 本プロジェクト（パーソナルプロジェクト登録済み）の文脈・ルール読み込みの入口 |
| **Action Registry（`dodo_action_list` / `dodo_action_dispatch`）** | dodo Core が提供する数百の Action の目録と実行口。スキーマは dispatch 直前に対象 Action だけ取得。high/critical risk Action は明示的ユーザー意図が必須 | Opportunity クロール・SDT 書込・評価・Gate 検査などの運用処理を Action として実装・実行する |
| **SDT Action 群**（`sdt.semantic_search` / `sdt.khop_traverse` / `sdt.graph_bundle` 等） | SDT グラフの検索・トラバース・バンドル取得。**graph JSON の直読み・直編集は禁止（必ず MCP 経由）** | Portfolio 空間 / Opportunity 空間（04 参照）の読み書き経路。Fact/Belief/Hypothesis の統治は Action 側で強制される |
| **Agent / Skill / Operation**（`dodo_agent_list` / `dodo_skill_get` / `agent.context_pack` 等） | SDT に定義された Agent（役割）・Skill（手順）・Operation（作業単位）を MCP 経由でロード・起動する | 05 の Agent 構成（Opportunity / Yield / Guardian 等）をこの機構の上に定義する |
| **クレデンシャル統治（`env://` 参照）** | 資格情報は平文で持たず `env://` 間接参照のみ。DID/VC で Agent・承認者を識別。署名処理は Desktop（ユーザー環境内）に残す | CR-1（鍵管理二層構成）の実装面。RPC キー・API キーも同機構に載せ、秘密鍵は MCP に通さない |
| **HIL / Gate 機構**（completion gate・staging approve 等） | Action の実行前検査・人間承認・Evidence 記録を Gate として強制する | Policy Gate・HIL Gate（05 参照）の実行面。「LLM に最終可否を出させない」を機構として担保 |

運用上の規律（AGENTS.md §Tools / Core MCP Gateway に準拠）:

- セッションは例外なく `dodo_project_bootstrap` から始める（bounded、Issue 全読み禁止）
- Action の選定はカタログ優先。直 REST は文書化された fallback のみ
- SDT スキャン・更新は必ず Action 経由（JSON 直読み・手編集禁止）
- 本テーマの Concept（`docs/docs/1.concept/00〜06`）は、セッション開始時に読むべきテーマ正本として AGENTS.md から参照される

---

## このテーマでの効き所（→ 01-problem.md）

| dodoAI 能力 | どの課題に効くか |
|---|---|
| SDT（Semantic Digital Twin） | 課題1・5: 市場状態・ポートフォリオ・Opportunity・Policy（投資憲法）・取引結果を Opportunity Graph / Portfolio State として構造化し、常に「今どうなっているか」を保持する。数百プロトコルの巡回結果が静的レポートでなく更新され続ける一次構造になる |
| Fact / Belief / Hypothesis の分離統治 | 課題2・3: 「オンチェーン実測（Fact）」「APY 推定・エアドロップ可能性（Belief, confidence 付き）」「新プロトコルの将来性（Hypothesis）」を分離し、SNS 投稿やインフルエンサー発言が事実として売買に接続される事故を構造的に排除する。情報源ごとの信頼度階層を強制する |
| Evidence = Provenance | 課題5: 全取引の Intervention（提案→検査→署名→執行）と Observation（結果）を対で Evidence Ledger に記録。「なぜ投資したか」「どの情報源が正しかったか」「何もしない方がよかったか」を遡れる。税務用の取得価格・取引理由の記録も兼ねる |
| Multi-Agent | 課題2・4: Strategy Agent の提案を Risk Agent（VaR・デペッグ・プロトコルリスク）と Red Agent（その取引が失敗する条件の攻撃的検証）が構造的に批判する。多数決にせず、最終可否は決定論的 Policy Engine が判断する |
| HIL | 課題3・4: Observe → Approve → Autopilot の3段階で人間承認の範囲を段階的に縮小。重大取引・緊急退避・権限変更は常に人間承認。Agent 自身に権限上限を変更させない |
| Domain Universality | Airdrop / Yield / リバランス / Guardian という異なるドメインの機会・リスクを、同一の「リスク予算付き Opportunity Portfolio」構造（状態・目標・制約・因果）で統合管理できる |

## この手段が最適である理由

このプロダクトの価値は「どの通貨が上がるか（予測精度）」ではなく、**Agent の統治と投資判断の組織知**にある。

1. **統治が本質だから**: 「暴走しない・説明できる・権限を奪えない AI」は、権限制御（Agent Governance）・判断根拠追跡（Evidence）・人間の最終権限（HIL）を基盤に持つ dodoAI でなければ、後付けで実現できない。単なる LLM + 取引 API では API キー丸渡しのブラックボックスに退行する。
2. **秘密鍵の分離統治**: 秘密鍵は AI に渡さない。鍵管理は dodo のクレデンシャル機構（DID/VC・`env://` 参照・Desktop によるユーザー環境内の署名処理）を基本とし、**個人のハードウェアモジュール（ハードウェアウォレット等）で補完する二層構成**。Agent が持つのは Session Key / Safe Module 経由の期限付き・用途限定の実行権限のみ（詳細 = [06-common-requirements.md](06-common-requirements.md) CR-1）。
3. **組織知の蓄積装置だから**: どの Opportunity・情報源・戦略バージョンが正しかったかという投資判断の知は、Fact/Belief/Hypothesis 分離 + Evidence の SDT にだけ蓄積できる。個人で使えば Personal Investment Intelligence、法人・DAO で使えば Organizational Investment Intelligence になる。
4. **「何もしない」を正当化できるから**: デフォルト不作為・回転数上限・増分利益測定という規律は、Goal/Constraint を明示した SDT と決定論的 Gate があって初めて機械的に強制できる。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v1.2.0 | 2026-08-22 | 「dodo Core MCP の概要」セクションを追加（bootstrap / Action Registry / SDT Action / Agent 機構 / クレデンシャル統治 / Gate）。固定部分は変更せず |
| v1.1.0 | 2026-08-22 | crypto.md を元にテーマ固有の効き所・最適理由を記入。秘密鍵の二層構成（dodo クレデンシャル機構＋個人ハードウェアモジュール）を明記 |
| v1.0.0 | {{DATE}} | 雛形から生成（「dodoAI の強み」「使い方のポイント」は固定、テーマ固有部分は未記入 ⬜） |
