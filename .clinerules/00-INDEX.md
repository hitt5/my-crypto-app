# 📇 L1 — ClineRules INDEX（索引のみ・本文なし）

> リポジトリ指示の正本は `AGENTS.md`。本索引はその fallback projection であり、
> `AGENTS.md` が利用できない場合だけ `00-CORE.md` と共に注入される。用途は L2 手順の解決と、
> `AGENTS.md` 不在時の権威的 fallback。
> 廃止済みの `.dodoai/rules` は指示元として扱わない。

> トリガー → 読むべき L2 ファイルの対応表。常時遵守は **`00-CORE.md`（L0）**。
> L2 の収録基準と再腐敗防止契約は **`.clinerules-detail/00-README.md`**。

## SoT の分担

| 領域 | SoT |
|---|---|
| セッション起動・ルール配信・Issue 候補・Action 一覧・AGN コンテキスト | **MCP**（`dodo_project_bootstrap` / `dodo_action_list` / `dodo_agn_context`） |
| 禁止事項・DD 反復・A02/A03・テスト戦略・品質ゲートの**条文** | **Charter**（`docs/0.charter/`） |
| 成果物の中身（要求・契約・カタログ・CallGraph・Evidence・観測記録） | **ART**（`docs/99.sdt/art/`） |
| 成果物どうしの関係（接続 / trace / status / workflow / findings） | **AGN**（`docs/99.sdt/agn/`） |
| ART / AGN のどちらに置くかの**判別基準** | **`docs/99.sdt/README.md`**（単独所有・再掲禁止） |
| SDT 横断 Graph Bundle の Action key | **`sdt.graph_bundle`**（`agn.graph_bundle` は旧称の deprecated compatibility alias） |
| 人間可読の概念・要求・運用・テスト・手順 | **`docs/` 配下の MD**（`dodoai-docs/` は凍結アーカイブ） |
| ポート・パス・サービス一覧などの**事実** | **`.dodoai/repo-context.json`** / catalog / `dodo_action_list` |
| 上記で代替できない **HARD GATE 施行手順**のみ | **L2**（`.clinerules-detail/`） |


---

## 🎯 トリガー → 読むべきファイル

| こういう時 | 読む |
|---|---|
| 未知・多義的な用語や略語に遭遇した | `docs/0.charter/` + `docs/GLOSSARY.md`。未定義・矛盾時は HIL |
| SCO の意味を確認したい | `docs/GLOSSARY.md` + dodoAI `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/glossary.md` |
| ADF と言われた / ADF の工程・Gate を確認したい | dodoAI `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/` + `/Users/hitoshimurakami/myApps/dodoai/docs/0.charter/02-development-flow.md` |
| **層の関係が分からない / どこに書けばよいか迷った / 新しい BR・SR・FR・CAP を作ってよいか** | Charter `07-requirements-architecture-map.md` |
| World Model → Strategy → BR → EPIC/UC → CAP/FR → Code → Evidence の接続を確認したい | Charter `07-requirements-architecture-map.md` §1 |
| 縦糸（UC）と横糸（FR）のどちらに書くか判断したい | Charter `07-requirements-architecture-map.md` §3 / §5 |
| セッション開始 / MCP 接続設定 | `.clinerules/00-CORE.md` §STEP 0 |
| MCP が繋がらない / connection refused / bootstrap 失敗 | `.clinerules-detail/30-environment.md` §MCP Recovery Gate |
| 新規 Action が `Action not found` になる | `.clinerules-detail/30-environment.md` §Action Registry が stale な場合 |
| **コード変更の前**（Preload / CallGraph 影響調査 — HARD GATE） | `.clinerules-detail/10-preload-gate.md` |
| 実装フロー（SQ）/ Module 横断（AC）/ Designed UC・Feature・EPIC 影響を区別したい | `.clinerules-detail/10-preload-gate.md` §Step 4 |
| **完了報告 / DD Phase 完了 / HANDOFF `_done` の前**（HARD GATE） | `.clinerules-detail/11-completion-gate.md` |
| テスト層 / 旧 L 番号 / Mock 境界 / DD Phase 配置を決める | `.clinerules-detail/11-completion-gate.md` §Test Definition Gate |
| 仕様適合を実査したい / status を追認してよいか迷った | `.clinerules-detail/11-completion-gate.md` §Check 1 |
| DD05 サーバーデプロイ検証 / 実 URL ブラウザ E2E | `.clinerules-detail/11-completion-gate.md` §DD04/DD05 |
| ロードマップ / タスクグラフ status 同期（P20） | `.clinerules-detail/11-completion-gate.md` §Check 4 |
| 次に何をやるべきか / 優先度キュー / 「次のタスクは？」 | `.clinerules-detail/20-navigation.md` |
| セッション開始時の改善状況把握 / 「OODA回して」「改善の続き」 | `.clinerules-detail/20-navigation.md` §Ops Status |
| 標準WF / 探索モードの判定（`agn.route_next`） | `.clinerules-detail/20-navigation.md` §Route 判定 |
| Operation / Agent の選定 | `.clinerules-detail/20-navigation.md` §Operation / Agent の選定 |
| 開発環境の起動 / サービス・ポートを知りたい | `.clinerules-detail/30-environment.md` §事実の取得先 |
| Dev2 / サーバー面 / Two-Plane / どちらのノードで作業するか | `.clinerules-detail/30-environment.md` §環境の位置付け |
| Git ブランチ運用 / 保護ブランチに commit してしまった | `.clinerules-detail/30-environment.md` §Git ブランチ衛生 |
| Issue / HANDOFF の作成と命名 | `.clinerules-detail/30-environment.md` §作業管理 |
| Clean Architecture / DD01 Scaffold / P28 / LCOM4 | `.clinerules-detail/40-domain-gates.md` §1 |
| SDT/AGN/ART データの生成・補修（schema 束縛） | `.clinerules-detail/40-domain-gates.md` §2 |
| Graph Bundle の正規名 / `agn.graph_bundle` を見つけた | Charter §1.2 + `.clinerules-detail/40-domain-gates.md` §2 |
| **新種の成果物を SDT へ追加したい / ART か AGN か迷った**（記録・計測・観測データを含む） | `docs/99.sdt/README.md`（判別の正本）+ `.clinerules-detail/40-domain-gates.md` §2 新種の成果物 |
| 概念（SCO）の追加・変更 / canonical 昇格 | `.clinerules-detail/40-domain-gates.md` §2 概念（SCO） |
| 新しい概念が十要素のどれか分からない / World Model 不変条件 | `.clinerules/00-CORE.md` §World Model Representation → 正本 Charter `11-world-model-representation.md` |
| 「整理した」「削減した」と報告したい / エントロピー主張 | `.clinerules-detail/11-completion-gate.md` §Check 6 |
| 画面 / UI / Atomic Design component の変更 | `.clinerules-detail/40-domain-gates.md` §3 |
| Agent / Skill / CRON catalog の棚卸し | `.clinerules-detail/40-domain-gates.md` §4 |
| **ルール自体を変更する時** | `.clinerules-detail/00-README.md` + `40-domain-gates.md` §5 |
| 禁止事項の条文確認（P1–P27） | `.clinerules/00-CORE.md` §絶対禁止 → 正本は Charter `01-development-charter.md` |
| Feature / UC / FR / CAP / Module の所有関係 | Charter `07-requirements-architecture-map.md` §3 → 正本は `adf/.../09-requirements-model.md` |
| DD01→DD05 反復 / A02・A03 Gate の定義 | Charter `04-iteration-protocol.md` |
| テスト定義・層選択 | SDT `docs/99.sdt/art/contracts/F-SDT-TEST-EVIDENCE/adf-test-definition.json` + ADF `adf/docs/ja/3.process/5.test/`。数値閾値は Charter `01-development-charter.md` §3 |
| ファイル移動で `ln://` / spec_refs が解決できない | `.clinerules-detail/10-preload-gate.md` §Step 3 |


CallGraph 影響調査（P18）は `10-preload-gate.md` §Step 4。

---

## 🗺️ 3層構造

```
.clinerules/
  L0  00-CORE.md     ← AGENTS.md 不在時だけ注入される fallback core
  L1  00-INDEX.md    ← 同条件で注入される L2 索引
.clinerules-detail/  ← L2（規約は 00-README.md）
```

> **2026/08/01 全面再構築**: 旧 L2 はエントロピー破綻（参照先不在 / 実行不能な起動手順 /
> ポート宣言と実態の乖離 / Action キー誤記 / 索引の自己矛盾）により**全件削除**した。
> 経緯と実測値は `.clinerules-detail/00-README.md`（旧内容は git 履歴のみ・復元して使わない）。
> 根本原因は内容の古さではなく、L2 が監査対象に登録されておらず
> **壊れても誰も気づかない場所にあったこと**。
> 再構築版は「事実を本文に書かない（N/R/E 分類）」＋「実在する Action だけを名指しする」を契約とし、
> `dodo_core/tests/test_clinerules_l2_integrity_l1.py` で機械保証する。
> ルールを追加/改名/削除した時は **この索引** と **`AGENTS.md`** を同じ変更で更新する。
