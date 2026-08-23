# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## Project Concept（テーマ正本 — 作業前に読む）

本リポジトリは **dodo Crypto Wealth OS**（theme_id: `crypto-wealth-os` / profile: `crypto`）のパーソナルプロジェクト。設計・実装・評価の作業を始める前に、テーマ正本である Concept を読むこと:

- 入口: `docs/README.md`（索引）/ インプット正本: `docs/5.reference/crypto.md`
- `docs/1.concept/00-overview.md` — 全体像・Product Form・プロジェクトタイプ（A+E）・答える問い・HIL ゲート
- `docs/1.concept/01-problem.md` — 課題認識
- `docs/1.concept/02-why-dodoai.md` — dodoAI の効き所・dodo Core MCP の概要
- `docs/1.concept/03-approach.md` — 運用ループ（Observe → Approve → Autopilot）
- `docs/2.sdt-design/02-data-model.md` ⭐ — SDT データモデル（3 空間・不変条件。旧 `1.concept/04-data-model.md` から移設）
- `docs/2.sdt-design/03-sco-policy.md` — SCO 方針（語彙の正準化 — Core SCO 写像 + Domain SCO Package）
- `docs/1.concept/05-multi-agent.md` — Agent 構成と Gate
- `docs/4.common/0.common-requirements/00-common-requirements.md` — **共通要件（CR-1〜CR-9 正本）。全 EPIC/Feature に横断適用。CR-1 は鍵分離、CR-8 はパーソナル Custom App スコープ、CR-9 は生存原理を所有する。BR/SR/NFR 展開は `docs/4.common/`**

Concept と矛盾する実装・要件を作らない。矛盾に気づいたら HIL（ユーザー裁定）へ。

## Personal Custom App Policy（基本方針 — HARD）

本リポジトリは **single-owner / local-first のパーソナル dodo Custom App** として開発する。汎用の暗号資産 SaaS や不特定多数向けサービスを既定形にしない。

- プロダクト形態は dodoAI 上の **Personal Custom UI + Personal Custom Action** を基本とする。A02 仕様は `docs/98.dodoai-custom-spec/`、personal scope の実装は `.dodoai/personal/custom_ui/` / `.dodoai/personal/custom_actions/` に置く。
- 一次利用者・資産所有者・最終承認者はユーザー本人。Multi-Agent は本人の意思決定を補助する内部ロールであり、複数顧客・組織・多数決を前提にしない。
- 個人の Portfolio / Policy / Wallet / Evidence に合わせて最適化する。ただし秘密鍵・シード・個人実値を repository、fixture、SDT、ログへ保存せず、CR-1 の dodo クレデンシャル機構＋個人ハードウェアモジュール境界を守る。
- multi-user、public SaaS、hosted custody、顧客アカウント、組織承認、第三者向け商用化への拡張は既定スコープ外。必要になった時点で HIL を行い、Concept と A02 要件セットを先に更新する。
- 共通化は本人の Custom App の保守性・再利用性に必要な範囲に留める。「将来売るかもしれない」を理由に multi-tenant / enterprise 機能を先行実装しない。

## Project Registration（dodo Core 登録情報）

本リポジトリは dodo Core にパーソナルプロジェクトとして登録済み:

| 項目 | 値 |
|---|---|
| Project ID | `43e2f654-cdd7-4572-b921-962bea2f0820` |
| Path | `/Users/hitoshimurakami/myApps/my-crypto-app` |
| Visibility | `personal` |
| Repo context | `.dodoai/repo-context.json`（標準 scaffold 生成済み） |
| Remote | `https://github.com/hitt5/my-crypto-app.git` |

- セッションの `dodo_project_bootstrap` / `project.index` はこの登録を解決する。別 project（`dodoai` 本体等）と混同しない。
- Rules/Roadmap catalog は未生成（初期化 Feature `F-WORKSPACE-BOOTSTRAP` は `running`）。catalog 生成後に本表を更新する。

## Instruction Source of Truth

- **`AGENTS.md` がリポジトリ指示の正本。** 利用不能なときだけ `.clinerules/00-CORE.md`（L0）+ `.clinerules/00-INDEX.md`（L1）を fallback として注入する。乖離したら AGENTS.md に従い、同一変更で ClineRules 投影を修復する。
- `.clinerules-detail/`（L2）は本ファイル / L1 index が指したときだけ読むオンデマンド手順庫。先読み禁止。
- **SoT ツリーは `docs/`**: Charter = `docs/0.charter/`、World Model / Viability Model = `docs/1.concept/` + `docs/2.sdt-design/02-data-model.md`、SDT/AGN/ART = `docs/99.sdt/`。プロジェクト固有の運用 SoT は未初期化であり、存在しない `docs/4.operation/` を正本扱いしない。dodoAI 本体の運用文書はフレームワーク参照であり、このプロジェクトの live state ではない。❌ `dodoai-docs/` は投影ビュー — 手編集・新規文書作成禁止。

### Terminology Resolution（HARD）

- 未知・多義的な用語や略語に遭遇したら、文脈や綴りから推測して作業を進めない。まず本プロジェクトの Charter（`docs/0.charter/`）と用語集（`docs/GLOSSARY.md`）で定義・正本参照先を確認する。どちらにも定義がない、または定義が矛盾する場合は、要件・実装を変更する前に HIL へ上げる。
- **SCO** は `Semantic Canonical Ontology`（意味の正準オントロジー）であり、project scope の略ではない。定義は `docs/GLOSSARY.md`、詳細な dodoAI 正本は `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/glossary.md` を読む。
- **ADF** と言われたら `Agentic Development Framework` を指す。必ず dodoAI 正本 `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/`（入口 `index.md`、用語 `glossary.md`）を読み、現行の開発工程・Gate は `/Users/hitoshimurakami/myApps/dodoai/docs/0.charter/02-development-flow.md` で確認する。`Autonomous Development Flow` など別の展開を推測して使わない。

**Precedence**: ① 現行 runtime の system/developer/tool 指示 → ② Charter（`docs/0.charter/` = 憲法。P1–P29・ゲート・数値閾値を単独所有）→ ③ 本 AGENTS.md（手順の正本）→ ④ ClineRules L0+L1+L2（fallback 投影）→ ⑤ その他 docs。

## Session Startup

**Step 0 — 例外なく最初に MCP `dodo_project_bootstrap` を呼ぶ**（`read_file`・検索・質問より前。bounded payload、Issue 全読み禁止）。

MCP 不通時は直読みせず **MCP Recovery Gate**: 1 回リトライ → stdio 設定 / runtime-slot resolver が返した endpoint の `/ready` 確認 → 同じ解決済み port の listener / `tmux ls` 確認 → owner gate を通る非破壊の起動/再起動 1 回 → `/ready` を 3–5 秒間隔で最大 ~45 秒ポーリング → 成功後に bootstrap を再試行。**8510 を MCP/Core の汎用 fallback として推測しない。**使い切った場合のみ read-only fallback（Evidence に経緯を記録）。詳細: `.clinerules/00-CORE.md` §MCP Recovery Gate。

bootstrap 成功後、`.dodoai/repo-context.json` の `active_services` に Tauri/Desktop stack が宣言されている workspace だけ **Tauri Startup Check をセッション中 1 回**行う。`active_services` が空なら起動対象なしとして何も起動・再起動しない。宣言がある場合は service 名・port・標準起動コマンドをそこから解決し、Desktop process/window、Vite、Provider、Core readiness、owner tmux（pane が実コマンドかも含む）を個別確認する。Desktop が背面/最小化されただけ、Tauri 所有 sidecar が cold start 中、または別 session の正当な owner がいる場合は再起動しない。**Desktop process 不在または必要 component の停止を確認し、競合 owner がいない場合だけ**、repo 標準の Tauri owner 経路を非破壊で 1 回起動/再起動し、全 component を 3–5 秒間隔・最大 ~45 秒再確認する。standalone Core を重ねて起動しない。復旧しなければ process/listener/tmux/log の Evidence と blocker を記録し、稼働を推測して先へ進まない。詳細: `.clinerules-detail/30-environment.md` §Tauri Startup Check。

Then, in order:

1. bootstrap が返す `AGENTS.md` を指示源として使う。`SOUL.md` / `USER.md` / memory は個人・セッション文脈が必要なときだけ読む。
2. MCP inventory: `tools/list` 相当 + bounded `dodo_action_list(include_schema=false)`。スキーマは dispatch 直前に対象 Action だけ取得。
3. **Ops Status は必要時のみ**: 通常の coding / review / 文書作業では `autoloop.status` を dispatch しない。明示要求・AutoLoop/OODA/CRON/soak 自体の現在値・完了条件が運用状態を要求する場合のみ実行し、実行時は `Ops Status:` を 1 行記載、同一 task では観測結果を再利用。手順 SoT: `.clinerules-detail/20-navigation.md`。project-local Soak catalog が未初期化なら dodoAI 本体の状態を本プロジェクトの状態として転記しない。
4. Issue / Feature ID / 具体的意図があれば `agn.route_next` を dispatch し、`mode` / `session_instruction` に従う。
5. `docs/99.sdt/agn/5.operations/operations.json` が存在する場合だけ、そこから Operation を選び、宣言 `attributes.agent` に `agent.context_pack` を dispatch。作業開始メッセージに `Operation: <id> | Agent: <id>` を記載する。catalog が未初期化なら Agent を推測せず、`Operation: unresolved (catalog absent) | Agent: unresolved` と blocker を記録して、明示されたユーザー意図の範囲だけを現 runtime Agent で進める。
6. `active_issue_summary` と bounded 候補からタスクを選び、選定後にのみ当該 Issue ファイルを読む。

## Per-Work TaskGraph Lifecycle Gate（HARD — 作業ごとに必須）

**TaskGraph が既に存在することの確認だけでは満たさない。** 変更を伴う各作業単位で実行する（read-only 調査は対象外、変更する判断をした時点で対象）。

**作業前**: ① owning Feature を解決（推測 Feature へ書かない。新 Feature は A02/HIL 先行）② 作業専用 task node（`task-dd*.json`）を作成 — 固有 `task_id` / `issue_refs` / `spec_refs` / 機械実行可能な `done_criteria` / `size` / `success_probability` / `max_ticks` ③ Task node を正本として Issue MD view を作る（MD だけ先に作らない）④ claim/lease 取得、`ready → running` 遷移後に初めて変更 ⑤ 開始メッセージに `Task: <task_id> | Issue: <path> | Status: running` を記載。

**作業後**: ① 同じ node へ変更ファイル・テスト/Action・Evidence・残課題を反映 ② 実態どおり `done`/`blocked`/`failed`/`running` へ遷移（Gate 未達を done にしない）③ 同一作業内で Issue を同期し lease 解放 ④ `roadmap.sync_gate` を実行し結果を記録（Feature 既存負債は改ざんせず別報告）。

**Agent 生成ファイル追跡 Gate（HARD）**: Task / Issue / Evidence は必ず**現在 checkout 中の同一 worktree**へ作る。MCP / Action に別 checkout の `workspace_root` を渡して、正本 worktree に生成物だけを残すことを禁止する。新規 Task / Issue / Evidence は作成直後にその明示 path だけを `git add -- <path>` し、同じ作業の commit / push に必ず含める。完了・handoff・push 後に Agent 生成の `??` を残してはならない。

Gate を飛ばした場合、後追い Task を「作業前作成済み」と扱わず、違反/Finding として記録する。

Don't ask permission. Just do it.

## World Model Representation（5 不変条件 — 常時遵守）

| # | 不変条件 | 要旨 |
| --- | --- | --- |
| WM-1 | 定式化 | 新概念は World Model 十要素のどれかを言えること。言えないなら `draft` + HIL |
| WM-2 | エントロピー最小化 | 意味保存の観測なき「整理した」主張禁止 |
| WM-3 | 統治 | Fact / Belief / Hypothesis を混ぜない。State に LLM 推定値・自己申告を書かない |
| WM-4 | トレーサビリティ | dispatch と observe を対にし State へ反映 |
| WM-5 | 双対表現 | MD（人間可読 view）と JSON（機械可読 SoT）の対で維持 |

- 世界モデル層の操作は **Intervention**（dodo Core の `action_key` とは階層が異なる）。SDT Graph Bundle の正規名は `sdt.graph_bundle`（旧称 alias は Charter §1.2）。
- P25/P26/P27 は advisory — 「機械検証済み」と誤報告しない。
- 正本: 条文 = `docs/0.charter/01-development-charter.md`、プロダクト概念 = `docs/1.concept/00-overview.md` + `docs/2.sdt-design/02-data-model.md`。

## OKF Markdown Standard

Markdown の新規作成・実質更新時は先頭に YAML front matter を付ける。全体必須は `type` のみ。実行結果（Action / MCP / Agent / workflow / job / test / build / deploy / audit）では `execution_id` も必須（基盤発行 ID 優先、再試行は新 ID + `parent_execution_id`）。`title` / `tags` / `timestamp` 等は根拠があれば推奨 — 推測して埋めない。機械処理を壊す対象には無理に付けない。正本と例: `.clinerules/00-CORE.md` §OKF。

## Document Writing Standard（MD 品質 — 文書作成・更新時に常時適用）

**文書は「読み手が知らないこと」だけで構成する。** 量は品質ではない — 情報密度が品質。

### 必須要素

- YAML front matter（OKF 準拠、§OKF Markdown Standard）を先頭に付ける。
- SoT / SDT / 関連文書への参照は**冒頭 3 行以内または該当記述のインライン**に置く。文末に「関連リンク」「参考資料」章を作って参照を溜めない。

### 構成

- 冒頭 3 行以内に文書の結論・判断・SoT 参照先を書く。「本文書は〜を説明する」型の自己紹介文を書かない。
- テンプレ章の禁止: 「概要」「背景」「目的」「まとめ」「今後の展望」は、その章にしか書けない固有情報がある場合のみ設ける。
- 1 情報 1 箇所: 同じ内容を本文とまとめで反復しない。既存文書の内容は転記せず参照する。
- 見出しは 3 段（`###`）まで。章の数は内容が要求する数だけ — 埋め草で対称性を作らない。

### 文体

- 断定で書く。「〜が望ましいと考えられます」等の無情報ヘッジ文を書かない。不確実な内容は Fact / Belief / Hypothesis を明示する（WM-3）。
- 1 文で済む内容を見出し+箇条書きに膨らませない。比較・列挙が 3 項目以上なら表または箇条書き。
- 太字は 1 節 1–2 箇所まで。絵文字・装飾記号は使わない。
- 数値・パス・コマンド・ID は具体値で書く。「適切に設定する」等の実行不能な記述を書かない。
- 変動値（実測メトリクス等）を転記しない — 取得コマンド/Action を書く。

### 検収（生成後に自己検査してから完了）

① 各章を削除して情報が失われるか — 失われない章は削除 ② 各文が読み手の行動・判断を変えるか — 変えない文は削除 ③ 冒頭から結論に最短で到達できるか。

## DODO Reference Repository

`dodo` / `dodoAI` / `dodo core` / `DODO CODE` は、明示がない限りローカルの本リポジトリを指す。**現行の正本パスは `/Users/hitoshimurakami/myApps/dodoai`**。移動確認が必要な場合は `dodo_project_index(query="dodoai", include_settings=true)` を呼び、`slug="dodoai"` の row の `path` を正とする（`general` alias を誤選択せず、重複 row を作らない）。

## ClineRules（fallback 3 層）

L0 = `.clinerules/00-CORE.md`（利用不能時のみ注入）/ L1 = `.clinerules/00-INDEX.md`（trigger→file 索引の正本）/ L2 = `.clinerules-detail/*.md`（指されたときだけ読む）。ClineRules は本ファイルの圧縮投影 — どちらかを変えたら同一変更でもう片方も更新し、`dodo_core/tests/test_clinerules_l2_integrity_l1.py` + `rules.audit` を実行。L2 の内容契約は `.clinerules-detail/00-README.md` が所有。

**Approved MD SoT**: SDT = ART + AGN。**ART が正本 SoT、AGN は ART を意味で接続する因果グラフ**（判別の正本 = `docs/99.sdt/README.md`）。`docs/` 配下の各 MD 族は人間可読の規範 SoT — SDT JSON があるからと削除・無視しない。矛盾したら機械的関係/status は SDT、規範的散文は MD を採り、両側を同期修復。

## Git Branch Hygiene

- 現在 checkout 中のブランチで作業する。ユーザーが明示要求しない限り branch 作成/切替/改名/削除・worktree 操作をしない（heartbeat・Agent・CRON にも適用）。
- **CI 修復 / 「ローカル変更を全部 push」では現在 checkout を正本とする。** 既存 local commit の直上へ修正を重ね、未 commit のローカル変更も同じ依頼の commit / push に含める。ユーザーが明示要求しない限り、退避目的の別 clone / worktree / 一時 branch / snapshot ref / patch 転送を作らない。
- push 直前と直後に現在 checkout の `git status --short` を確認し、ユーザー変更と Agent 生成ファイルの双方が対象 commit に入ったこと、Agent 生成の未追跡ファイルが 0 件であることを確認する。別 checkout の HEAD 一致を、現在 checkout の追跡確認の代用にしない。
- `develop` / `main` / `master` へ直接 commit / merge しない。誤 commit は即座に work ブランチへ退避。統合は work ブランチを push して PR。stage/commit は依頼されたパスに限定。

## Requirements Model（BR → SR → UC → CAP → Mod）

**迷ったらまず `docs/0.charter/07-requirements-architecture-map.md`**（層の接続・所有境界の唯一の正本）。

- 定義順は BR → SR → UC → CAP → Mod が先、Feature 分解・コードは後。
- 縦糸 `BR → SR → UC → Evidence` ⟷ 横糸 `CAP ─owns→ FR` → Mod。**FR は CAP が所有**、Feature/UC は `references(satisfies)` で参照のみ。UC と FR を同一フォルダに混在させない。
- **EPIC / BR / CAP は JSON-first SoT**（`docs/99.sdt/art/catalog/source/`）。MD は `md_ref` の認知 view — MD だけの構造更新も JSON-first を理由の MD 削除もしない。
- **BR / SR / NFR / CAP / FR の新設は HIL 裁定必須。** Feature 固有事項は UC 受入基準で表現し、欠落 FR は `fr_gap` で記録。

## ADF Work Start Order（DD01–03 開始前）

条文正本は Charter `02-development-flow.md` / `04-autonomous-loop.md`。

1. **ADF Test Definition Gate（HARD）**: テスト層・Mock 境界を決める前に `docs/99.sdt/art/contracts/F-SDT-TEST-EVIDENCE/adf-test-definition.json` + MD view を読む。実際に変更する全 deploy unit の profile を合成する（主 deploy_unit だけで層を選ばない）。この project-local contract が未生成なら DD01–03 の実装へ進まず、`F-WORKSPACE-BOOTSTRAP` の blocker として扱う。dodoAI 本体の contract をこのプロジェクトの deploy-unit profile と偽って代用しない。
2. **上流 2 経路**: (A) Reverse（brownfield 既定）= コード → CallGraph → SDT 逆導出 → 文書投影 → drift HIL。(B) Forward = Intent → A02 → A03 → DD01–03。**MD + JSON 双対は HARD** — 片側のみで上流成果物を完了と呼ばない。
3. **A02 = 6 層要件セット + 全体設計**（EPIC→FEATURE→UC / CAP→FR→MOD）。BR/SR/UC で止めない。**A02 完了は A03 のトリガ — 「A02 done」で停止禁止**（明示縮小時のみ例外）。`requirements-weave.json` は Feature 別（authored）と集約 catalog（derived・手編集禁止）の 2 種。
4. **A02 Step 0（HARD）**: 所有 EPIC / CAP の存在を catalog で確認。無ければ Feature を切る前に EPIC / CAP を定義。迷ったら HIL。
5. **A02 成果物 3 点セット（HARD）**: ① release-goal 登録 ② 要求モデル MD ③ AGN グラフノード（`feature.json` + `task-dd*.json` + catalog/roadmap 同期）。物理パスは `sdt_layout.resolve` で解決。観測・実行記録は要求ではなく ART へ（判別 = `docs/99.sdt/README.md`、未宣言 family は HIL）。
6. **Task Graph Existence Gate（P9 — HARD）**: `feature.json` + `task-dd*.json` が無ければ UC/FR catalog から先に作る。
7. **A03 SDT/AGN Conformance Gate（P13 — HARD）**: A02 後 DD01 前。A03 はコード・Scaffold を作らない。
8. **Preload Gate（HARD）**: Issue → Task Graph → spec（`ln://` 解決）→ `callgraph.focus` / `callgraph.uc_reverse_lookup` で影響把握 → Preload Evidence Block をコード編集前に出力（`.clinerules-detail/10-preload-gate.md`）。UI 作業は `ui.component_catalog` の `semantic_review` を確認してから。Custom UI manifest 変更は `custom_ui.design_guide` + `custom_ui.manifest_lint(mode="strict")`。
9. **DD01 Scaffold Gate（P28 — HARD）**: 最初の UC の DD01 で `.dodoai/scaffolds/clean-architecture/<template_id>` を選び `a03.scaffold_gate` を実行。stale なら DD02 入場拒否。
10. 画面/UI 開発は `.clinerules-detail/40-domain-gates.md` を読み、`F-COCKPIT-UI-CATALOG/ui-components.json` を MCP 経由でロードしてから編集。

## DD05 Server Validation Gate（HARD）

Track B（Release Validation）は `feature.json.release_status` で分岐する。全 Feature は Track A（ST-E2E-HL/HD + ST-AI-Visual + ST-Human）を通す。`unreleased` は Track B 対象外、`released` はリリース面への deploy / 配布 → `/ready` → smoke → **リリース先実 URL** のブラウザ E2E → 実行ログ/lease/soak → `evidence-dd05.json` が必要。localhost E2E はリリース検証ではない。資格情報は `env://` のみ（P5）。対象外 / 未計測 / FAIL を区別し、Track B FAIL を稼働保証済みと報告しない。SoT: Charter `02-development-flow.md` §DD05・`06-quality-gate.md` §4 Check 5・`.clinerules-detail/11-completion-gate.md`。

## Completion Gate（P20 — HARD）

`attempt_completion` / DD 完了 / Feature・UC close / `_done` 改名の前に `roadmap.sync_gate` を dispatch し `ok=true`（`stale_task_status=0` / `missing_milestone=0` / `roadmap_drift=0`）を確認。`task-dd*.json` status / `dd_progress` / roadmap milestone のどれかが stale のまま「done」と報告しない。施行: `.clinerules-detail/11-completion-gate.md`（`arch.layer_check` / `test_evidence.audit` / `sdt.governance_metrics` を含む）。Custom UI の完了主張は `custom_ui.manifest_lint(mode="strict")` の `error_count=0` 必須。

### Completion Operation Hook Gate（HARD）

`AGENTS.md`・prompt・Skill・Operation List は「気づかせる」層であって強制機構ではない。Codex / Claude Code の `Stop` と dodo Coder の `attempt_completion` は共通 Core Action `sovereign.hook_gate` を通し、session worksetを `operations.json` の `attributes.completion_gate` と照合する。該当する残Operationがあれば、宣言された `Agent` / `Skill` を同一turnで実行してから完了する。

- CRON / scheduler / heartbeat を完了フックの代用にしない。
- High/critical Operation は current explicit intent または `standing-scoped` authorization の範囲内だけ半自動実行する。scope外（commit/push/branch変更/remote deploy等）は別承認。
- 同一 plan fingerprint は一度だけ継続要求する。同一MCP callを反復せず、遂行不能なら一つの具体的 blocker を報告して停止する。
- Hookが返すOperation IDから `attributes.agent` と `skills` を採用し、推測Agent・全Operation再走査・無関係Agent起動をしない。

## Specification-Conformance Completion Gate（HARD）

`workflow.status` / `_done` / 既存 Evidence / green gate / テスト PASS / coverage は SR 適合の証明ではない。完了主張の前に現在の checkout で実査する:

1. 全 SR/FR/UC を実装パス・テストへ対応付けた conformance matrix を作り、各行 PASS / PARTIAL / FAIL / NOT IMPLEMENTED を判定。PASS 以外が 1 件でもあれば完了禁止。
2. A03 計画と実ツリー/import を比較。変更系は非破壊・dry-run/apply・冪等性・rollback を個別検証。NFR は数値閾値を実測。
3. 「1 Action で結果が返る」等は live dispatch で composition-root 配線を確認（caller 前処理の単体テストで PASS にしない）。
4. 非 PASS の延期は判定を変えず、`_ready` Issue/STREAM + Task Graph 依存へ接続（重複起票禁止）。
5. 「実装して」に stale な `_done` を理由の verification-only で返さない。

詳細: `.clinerules-detail/11-completion-gate.md`。

## Closed Loop = WF（要点）

閉ループ（観測が次の判断へ戻るループ）は WF として定式化する。正準構造は **閉ループ = WF / 1 周 = DAG インスタンス / SDT = 状態空間** の 3 層分離。ADF（A02→A03→DD01–05→Evidence→優先度再導出）自体が第一適用対象。グラフへの巡回エッジ、Decide（HIL）/ Improve（Skill 改訂）の WF ノード化は禁止。WF 化してよいのは Act（介入）と検証手順のみ。プロダクト側の閉ループは `docs/1.concept/03-approach.md`、フレームワーク命題は dodoAI reference repository の `docs/1.concept/1.core-concept/08-agentic-ooda-operations.md` §4.2、手順は本 Charter `04-autonomous-loop.md` §0.1 を正とする。

**LOOP Catalog（AGN 第一級ノード）**: 閉ループを常設運用する前に project-local `docs/99.sdt/agn/4.loops/loops.json`（schema `docs/99.sdt/agn/0.schema/loop-schema-v1.json` / MD view `docs/99.sdt/agn/4.loops/index.md`）へ宣言する。LOOP は宣言・統治ノードであり、OODA 4 フェーズ + Improve の所有者、成熟度 E0-E2、空転検出定義、接地 references を持つ。実行体でも要件軸でもないため FR/UC/変動値を書かず、Operation の `tier` は心拍だけを表し、所属ループは LOOP 側が宣言する。成熟度の昇格は HIL、降格は機械即時。catalog/schema が未初期化なら「未登録」のまま blocker とし、JSON を推測作成しない。project-local 命題正本 = `docs/1.concept/03-approach.md` §LOOP Catalog、フレームワーク正本 = dodoAI reference repository の `docs/1.concept/1.core-concept/08-agentic-ooda-operations.md` §4.3、接続 = Charter `07-requirements-architecture-map.md` §2 #12。

## Capability Routing / OODA / TaskGraph SoT / Two-Plane（要点）

- **Capability Routing**: CP は `cp.estimate` が機械導出（自己申告上書き禁止）。`cp.route` がレーン決定。CP8+ / High risk / 判定不能は `human`。フレームワーク命題は dodoAI reference repository の `docs/1.concept/1.core-concept/08-agentic-ooda-operations.md` §4.1、project-local 手順は Charter `04-autonomous-loop.md` §2。
- **OODA Report Discipline**: 全ループ記録に R-1 Scorecard / R-2 Success Probability / R-3 Calibration の 3 群必須（欠けたら未観測ループ）。project-local schema / ART family が未初期化なら推測作成せず bootstrap blocker とする。条文 = Charter `04-autonomous-loop.md` §8。dodoAI 本体の実行記録を本プロジェクトの観測として転記しない。
- **TaskGraph Dispatch SoT（P29）**: 機械ループの一次状態は task-graph ノード。Issue は人間可読 view + HIL 面。suffix 改名を SoT にする経路を新設しない。計画・監査結果も対の規律: MD だけに書かない / TaskGraph だけ更新して view を残さない / 「次は何？」は ready ノード + Issue view の対で提示。
- **Two-Plane / Dual-Node**: この project に server plane が明示登録されるまでは Local single-writer とする。登録後も「両プレーンとも開発するが、同じ仕事は絶対にしない」。Local (Mac) = 品質・HITL・Merge 承認・SDT 書込主権、Dev2 = スループット、資格情報は `env://` のみ。排他は単一 Priority Queue / claim token / Single Writer + `roadmap.sync_gate`。詳細は dodoAI reference repository の `docs/4.operation/08-local-server-dual-node-development.md` をフレームワーク参照とし、live owner/lease は Core で観測する。

## Soak Operations（計画・実行・評価の SoT）

**Soak（長時間自律実行の耐久検証）は、project-local Operation / LOOP / metrics catalog が初期化された後だけ運用する。** 未初期化の本リポジトリでは dodoAI 本体の soak 文書を手順の参考にしても、その変動値・状態・Evidence を本プロジェクトの実績として転記しない。

- **フレームワーク参照**: dodoAI reference repository の `docs/4.operation/autonomous-execution-loop/`（入場 Gate、3 軸、OODA 記録形式）。
- **project-local 指標定義 SoT**: 初期化後の `docs/99.sdt/metrics/operations/soak-ooda-metrics.json`（+ MD view）。読み書きは MCP Action で行う: 現状把握 = `soak.metrics_overview` / 目標更新 = `soak.metrics_update`（HIL）/ 窓宣言 = `soak.window_preregister` / 窓実行 = `soak.window_supervise` / 判定 = `autonomy.soak_evaluate`。
- **project-local 実測 Evidence（captured ART）**: 初期化後の `docs/99.sdt/art/operations/soak/*.json`。SDT JSON の直読み・直編集は禁止（MCP 経由）。
- 規律: 窓は preregister → supervise → evaluate の順。invalid（測定無効）を pass/fail に丸めない。変動値をこのフォルダ外の文書へ転記しない（取得コマンド/Action を書く）。

## Memory

- Daily: `memory/YYYY-MM-DD.md` / Long-term: `MEMORY.md`（main session のみロード）。
- 「覚えて」と言われたら・教訓を得たら・ミスをしたら **ファイルへ書く**。

## Red Lines

- 私的データを外へ出さない。破壊的コマンドは確認なしで実行しない。`trash` > `rm`。迷ったら訊く。
- ワークスペース内作業は自由。メール送信・公開投稿などマシン外へ出る操作は事前確認。
- **User Runtime Reload Approval Gate（HARD）**: VS Code window / Extension Host / desktop application / その他ユーザーに見える UI・runtime の reload・restart は、**現在の会話でその操作自体についてユーザーが明示承認した場合だけ**実行する。「リロードしたら」といった現象説明、修正・build・install・検証の依頼、過去の許可を実行許可へ拡張解釈しない。修正の適用や UI proof のためでも自動 reload / restart は禁止し、build / install までに留める。必要ならユーザー自身による reload を案内し、未承認のまま操作しない。

## Group Chats

直接聞かれた・価値を足せるときだけ発言し、雑談は `HEARTBEAT_OK` で見送る。同一メッセージへの複数回返信をしない。

## Tools / Core MCP Gateway

MCP の「使い所」正本は `MCP_USAGE_GUIDE.md`。

- **Port ownership（HARD）**: `8510` は Tauri desktop control gateway の専有 port であり、Codex / Claude / CLI / health probe / plugin host / dodo-coder の汎用 Core 既定値ではない。開発 Core は `8521..8529` の固定 pool だけを使い、`dodo_core.shared.runtime_slot_resolver` / `dodo slot acquire` が workspace sticky lease を解決する。`.mcp.json` に `DODO_CORE_MCP_URL=:8510` を直書きしない。例外は Tauri control を明示した経路だけ。
- 設定: `.mcp.json` の stdio launcher は `DODO_CORE_SLOT_MODE=workspace` で resolver を通す。Action は `dodo_action_dispatch` の `action_key` で選ぶ。直 REST は Cockpit UI 実装か文書化された fallback のみ。
- **Web Search**: 最新・変動する外部情報、または出典付き調査が必要なら `websearch.query` を適宜使う。通常は `dodo_action_list(query="websearch", include_schema=true)` で発見して `dodo_action_dispatch(action_key="websearch.query", payload=...)` で実行する。`answer` は provider model の統合文であり、`citations` / `search_queries` / `search_count` を併読する。Action 成功を真実性の証明にせず、高リスク判断と provider 間不一致は一次資料で再検証する。資格情報は resolver の `env://` / Keychain 間接参照だけを使い payload に渡さない。
- Recovery / stop / reclaim は `/ready` の `owner_kind` / `pid` / `workspace_fingerprint` と `instances.json` の lease が一致する listener にだけ行う。owner が別・欠落・未検証なら touch/kill/reuse せず blocker として報告する。
- SDT スキャンは Action で: `sdt.khop_traverse` / `sdt.semantic_search` / `callgraph.uc_reverse_lookup` 等（graph JSON を直読みしない）。コード編集前は `callgraph.focus`、未知モジュールは `callgraph.digest`。
- High/critical risk Action は明示的ユーザー意図と Gate/Evidence 文脈が必須。
- Operation/CRON/Action の選定はカタログ優先: `docs/99.sdt/agn/5.operations/operations.json`（初期化後）/ `docs/99.sdt/art/operations/operation-list.md` / `process_catalog.list`。
- **LN URI**: `ln://` を `read_file` に渡さない — `ln_registry.resolve` で解決。リンク切れは `sdt.ln_link_heal_plan` → `sdt.ln_link_autoheal`（dry_run 先行）。`ln-registry.json` を手編集しない。
- **DODO CODE V2 native Coding**: V2 のコーディングは resolver が返した Core native API（`POST /api/coding/sessions` → turns → traces で観測）。`:8511` 直呼び禁止・具体的 `issue_ref` 必須。Tauri UI が control gateway を使う場合だけ 8510 を明示する。Issue ドリフト検知時は即キャンセル。
- Action/schema/gateway 変更時は解決済み endpoint の owner を確認し、User Runtime Reload Approval Gate の承認後にその owner 経路だけを再起動して `dodo_action_list` で確認する（Registry は起動時構築）。

Issue / HANDOFF は `.dodoai/issue/` にテンプレ `docs/99.sdt/agn/0.schema/issue-handoff-template.md` で作成。

## 💓 Heartbeats

`HEARTBEAT.md` があれば従う（小さく保つ）。チェック状態は `memory/heartbeat-state.json`。深夜(23:00–08:00)・直近 30 分以内の再チェックは沈黙。自発作業可: memory 整理、ドキュメント更新、**現在の work ブランチ上での** commit/push（branch 作成・protected 直 commit は禁止）。

## Make It Yours

This is a starting point. Add your own conventions as you figure out what works.
