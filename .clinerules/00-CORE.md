# ⛔ L0 — FALLBACK CORE

> リポジトリ指示の正本は **`AGENTS.md`**。このファイルは同じ方針の
> **fallback projection** であり、`AGENTS.md` が存在し内容がある場合は注入しない。
> `AGENTS.md` が利用できない場合だけ本ファイルと `00-INDEX.md` を注入し、
> `source = clinerules` とする。
> 両者が乖離した場合は `AGENTS.md` を優先し、同一変更で本投影を修復する。
> 独自仕様 `.dodoai/rules` は廃止済み。指示元として読込・作成・移行しない。
> 詳細ルールは本文を持たない。トリガーが来たら **`00-INDEX.md`（L1）** を引いて該当 L2 ファイルを読む。
> Charter（`docs/0.charter/`）が憲法、本ファイルはその施行要点の最小核。

---

## 🔄 Docs Tree

**`dodoai-docs/` は凍結アーカイブ。Active SoT ツリーは `docs/` へ移行した。**

- SDT/AGN/ART = `docs/99.sdt/`、Charter = `docs/0.charter/`、World Model / Viability Model = `docs/1.concept/` + `docs/2.sdt-design/02-data-model.md`
- project-local Operation runbook / LOOP / metrics catalog は未初期化。dodoAI 本体の運用文書は framework reference であり、この project の live state ではない。
- `dodoai-docs/` 旧パスや互換 symlink の存在を仮定しない。
- ❌ `dodoai-docs/` 配下への手編集・新規 EPIC/CAP/Feature ドキュメント作成は禁止（投影対象ビュー / HIL 裁定 baseline のみ）

---

## 🔤 Terminology Resolution（HARD）

- 未知・多義的な用語や略語は推測せず、まず `docs/0.charter/` と `docs/GLOSSARY.md` で定義と正本参照先を確認する。未定義・矛盾時は要件や実装の変更前に HIL へ上げる。
- **SCO** = `Semantic Canonical Ontology`。project scope の略ではない。詳細は `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/glossary.md`。
- **ADF** = `Agentic Development Framework`。言及されたら `/Users/hitoshimurakami/myApps/dodoai/ADF/docs/ja/` を読み、現行工程・Gate は `/Users/hitoshimurakami/myApps/dodoai/docs/0.charter/02-development-flow.md` で確認する。別の展開を推測しない。

---

## 🧩 Personal Custom App Policy（基本方針）

my-crypto-app は **single-owner / local-first のパーソナル dodo Custom App** として開発する。

- dodoAI 上の Personal Custom UI + Personal Custom Action を既定形とする。A02 仕様は `docs/98.dodoai-custom-spec/`、personal scope の実装は `.dodoai/personal/custom_ui/` / `.dodoai/personal/custom_actions/`。
- 一次利用者・資産所有者・最終承認者はユーザー本人。Multi-Agent は本人を補助する内部ロールであり、複数顧客・組織・多数決を前提にしない。
- 個人最適化を行っても、秘密鍵・シード・個人実値を repository、fixture、SDT、ログへ保存しない。鍵は dodo クレデンシャル機構＋個人ハードウェアモジュールの境界内に置く。
- multi-user、public SaaS、hosted custody、顧客アカウント、組織承認、第三者向け商用化はスコープ外。着手前に HIL を行い、Concept と A02 要件セットを更新する。
- 将来の外販だけを理由に multi-tenant / enterprise 機能を先行実装しない。

---

## 📝 OKF Markdown（YAML風ヘッダ）を標準とする

新規作成または実質的に更新する Markdown は、可能な限り先頭に `---` で囲んだ YAML front matter を持つ **OKF（Object Knowledge Format）** とする。Codex、Claude Code、Clineのいずれが作成する場合も同じ規約を適用する。

- 唯一の必須フィールドは `type`。文書の知識オブジェクト種別を短い機械可読値で記載する。
- `title`、`description`、`resource`、`tags`、`timestamp` は内容に応じて推奨する。値を推測して埋めず、不明なら省略する。
- **実行結果の条件付き必須項目**: Action、MCP、Agent、workflow、job、test、build、deploy、auditなどの実行結果を記録するOKFでは `execution_id` を必須とする。実行基盤が返したIDを優先し、返さない基盤では実行前にUUIDまたはULIDを発行して、入力、ログ、成果物、Evidenceへ同じIDを引き回す。IDを推測・再利用しない。
- 再試行や子実行では新しい `execution_id` を発行し、元実行との関係を示す必要がある場合は `parent_execution_id` を併記する。
- `resource` は対象リソースを一意に示せる場合にURI形式で記載する。`timestamp` はISO 8601形式とする。
- 既存front matterがある文書では破壊せず統合する。生成器・外部仕様・互換性・投影先テンプレートが別形式を要求する場合は、その正本仕様を優先する。
- README、コード生成物、外部から同期した文書など、OKF化が不適切または機械処理を壊す文書へは無理に追加しない。「極力」は互換性を壊さない範囲を意味する。

```md
---
type: table
title: 顧客テーブル
description: 顧客の基本情報を格納するマスタ
resource: bigquery://project.dataset.customers
tags: [master, customer, pii]
timestamp: 2026-01-15T00:00:00Z
---
```

実行結果の例:

```md
---
type: execution-result
title: SDT整合性監査結果
execution_id: 01JQXYZ8M7C4N2K6V9A3B5D1EF
timestamp: 2026-01-15T00:00:00Z
tags: [sdt, audit]
---
```

---

## ✍️ Document Writing Standard（MD 品質 — 文書作成・更新時に常時適用）

**文書は「読み手が知らないこと」だけで構成する。** 量は品質ではない — 情報密度が品質。正本: `AGENTS.md` §Document Writing Standard。

- 必須: YAML front matter（§OKF）を先頭に付ける。SoT / SDT / 関連文書への参照は冒頭 3 行以内または該当記述のインラインに置き、文末に「関連リンク」「参考資料」章を作らない。
- 構成: 冒頭 3 行以内に結論・判断・SoT 参照先。「本文書は〜を説明する」型の自己紹介文禁止。テンプレ章（概要/背景/目的/まとめ/今後の展望）は固有情報がある場合のみ。1 情報 1 箇所（既存文書は転記せず参照）。見出しは `###` まで。
- 文体: 断定で書く（無情報ヘッジ文禁止。不確実は Fact / Belief / Hypothesis 明示 = WM-3）。1 文で済む内容を膨らませない。太字は 1 節 1–2 箇所、絵文字・装飾禁止。数値・パス・コマンドは具体値。変動値は転記せず取得コマンド/Action を書く。
- 検収: ① 削除して情報が失われない章は削除 ② 読み手の行動・判断を変えない文は削除 ③ 冒頭から結論に最短到達できるか自己検査してから完了。

---


## 🌍 World Model Representation — 状態表現の 5 不変条件（常時遵守）

> **SDT は「意味を保存したまま最小状態へ還元された世界の表現」である。**
> dodoai の全条文は $\min H(S)$ s.t. $Meaning(S) = Meaning(World)$ という一つの原理から導出される。

| # | 不変条件 | 常時守ること |
|---|---|---|
| WM-1 | **定式化** | 新しい SDT ノード種別・概念は World Model 十要素（Entity / State / Relation / Constraint / Goal / Intervention / Observation / Reward / Dynamics / Provenance）のどれかを**言えること**。言えないなら定義が曖昧か World Model 側の見直し → `draft` + HIL |
| WM-2 | **エントロピー最小化** | $H$ と $Meaning$ は**同時に**測る。「整理した」「削減した」「統合した」を $H$ 単独で主張しない。文書・ルールは意味を保つ最小十分記述とし、重複・脚色・推測を加えない |
| WM-3 | **統治** | Fact（決定論的計測）/ Belief（confidence 付き）/ Hypothesis を混ぜない。State に LLM 推定値・自己申告を書かない |
| WM-4 | **トレーサビリティ** | 観測されない介入を作らない。dispatch と observe を対にし、結果を SDT の State へ反映する。**Evidence は監査ログではなく世界モデルの訓練データ** |
| WM-5 | **双対表現** | MD（人間可読 view）と JSON（機械可読 SoT）の**対**で維持する。MD-only / JSON-only を正本と呼ばない |

**用語規約（HARD RULE）**: 世界モデル層で「世界を変える操作」は **Intervention（介入 $I_t$）**。
dodo Core の実装カタログ「Action Registry / Core Action / `action_key`」とは階層が異なる（Intervention = 抽象型、Core Action = その実装形態の一つ）。

**SDT Graph Bundle Action**: 正規名は `sdt.graph_bundle`。`agn.graph_bundle` は旧称の
deprecated compatibility alias に限る。新規コード・規範・手順は正規名を使い、過去 Evidence の
実行時キーは改変しない。MD で旧称を参照する場合は「旧称」と明記する（条文正本: Charter §1.2）。

禁止 P25（十要素アンカー未宣言の概念を `canonical` 使用）/ P26（意味保存の観測なきエントロピー改善主張）/
P27（Fact・Belief・Hypothesis 混在 State 書き込み）は現在 **advisory**（機械検査の実装をもって HARD GATE 昇格）。
測れないゲートを HARD と宣言しないための段階導入であり、**「機械検証済み」と誤認して報告しない**。

> 正本: Charter `docs/0.charter/01-development-charter.md`（5 不変条件・段階導入・指標）
> プロダクト概念正本: `docs/1.concept/00-overview.md` + `docs/2.sdt-design/02-data-model.md`

---

## 🚦 STOP — コード/仕様変更の前に自己申告せよ


コード（`.py/.ts/.rs/.tsx`）や `approved/` 仕様を**変更する前に**、以下を声に出して確認する。
1つでも「未」があるなら**手を止めて先にそれをやる**。

- [ ] **MCP起点で開始したか？** → `dodo_project_bootstrap`（bounded payload）→ MCP が落ちた時は §MCP Recovery Gate を試してから fallback したか → 必要時のみ `agn_session_startup`（dashboard→context）を叩いたか
- [ ] **MCP一覧を取得したか？** → bootstrap 後、`tools/list` 相当 + `dodo_action_list(include_schema=false)`（必要時 `dodo_agent_list` / `dodo_skill_list`）で利用可能 MCP/Action を list-only 確認したか。schema は dispatch 直前に対象 Action だけ `query=<target>, include_schema=true` で見る。
- [ ] **Adaptive WF Route を取得したか？** → active Issue / Feature ID / user intent が見えたら `agn.route_next` を呼び、`standard` / `adaptive` / `exploratory` と `session_instruction` を作業ナビとして扱ったか
- [ ] **Ops Status が本当に必要か判定したか？** → 通常の coding / review / 文書作業では `autoloop.status` を実行しない。明示要求・AutoLoop/改善/OODA/CRON/scheduler/soak 自体の現在値・完了条件が要求する運用状態・観測後の状態変化確認に限って実行し、実行時だけ Ops Status を 1 行明記する。同一 task では task state / 会話履歴の観測結果を再利用する。改善系で必要な場合は `autonomy.rate_compute`（DD02 後は `selfimprove.evaluate`）+ 最新 soak レポート（`99.sdt/art/operations/soak/` 最新1件）も読む → `.clinerules-detail/20-navigation.md`
- [ ] **Task Graph は在るか？**（P9）→ なければ UC/FR から先に作る
- [ ] **今回の作業専用Task nodeを作成・claimしたか？**（Per-Work TaskGraph Lifecycle Gate / P29）→ 既存Feature/既存TaskGraphの存在確認では代替不可。最初の変更より前に `task-dd*.json` + Issue viewを作り、claim/lease付きで `ready → running` にする。`task_id` / Issue / `status=running` が無ければコード・文書・ルール・設定・テスト・DB/Action stateを変更しない。`task_graph.create_manual` のDB overlayは開発TaskGraphの代替ではない。
- [ ] **ロードマップは最新か？**（P20）→ A02 開始・AGN 登録時 / Feature 依存 / 新 Epic に変化があれば同一作業内で `roadmap.derive` を実行し `roadmap-graph.json` を更新。「次何やる？」なら Priority Intelligence（下記 🧭）で決める

- [ ] **A02・A03 を通したか？**（P13/P15/P16/P17 / HARD GATE）→ DD01 着手前に A02（全体設計 AG-02）+ A03（SDT/AGN Conformance）を PASS させたか。DD02 着手前に DD01 Scaffold + ドメイン凝集性 + Architecture Invariant baseline（P28）を PASS させたか
- [ ] **CallGraph 影響調査したか？**（P18 / HARD GATE）→ `callgraph.focus`（編集前ブリーフィング1コール）または `callgraph.uc_reverse_lookup` を実行したか

- [ ] **画面/UI開発なら `ui.component_catalog` を dispatch して `semantic_review` を読んだか？** → `.clinerules-detail/40-domain-gates.md`
- [ ] **新しい概念・ノード種別を導入するなら、World Model 十要素のどれか言えるか？**（WM-1 / P25）→ 言えないなら `draft` に留めて HIL へ。十要素は §World Model Representation
- [ ] **「整理・削減・統合」をするなら、意味保存側も測る用意があるか？**（WM-2 / P26）→ $H$ 単独の改善主張は禁止。仕様・Evidence・trace を削って数値を良くしていないか
- [ ] **Preload Evidence Block を出力したか？** → 出すまでコード変更開始は禁止


> **完了報告の前にも自己申告せよ（STOP — Completion）**: `attempt_completion`・DD Phase 完了・Feature/UC close・HANDOFF `_done` の**前に**、まず現在の checkout で全 SR/FR/UC と実装・acceptance test の対応、A03 計画と実レイヤ/import、mutation safety、数値 NFR を実査し、全行 PASS を確認する。`workflow.status` / `_done` / 既存 Evidence / green MCP gate / tests PASS は SR・A03 適合の証明ではない。その後 MCP で①ガバナンス登録（`sdt.governance_metrics`）②テストエビデンス（`test_evidence.audit` で `gaps=0`/`broken_links=0`）③テスト PASS + Coverage ≥80% ④**ロードマップ/タスクグラフ status 同期（`roadmap.sync_gate` で `stale_task_status=0`/`missing_milestone=0`/`roadmap_drift=0`）**を確認し、**Completion Gate Evidence ブロックを出すまで「完了」と言わない**（HARD GATE #7 / Charter P3/P20）。詳細 → `.clinerules-detail/11-completion-gate.md`

> **DD05 Release Validation（HARD GATE）**: 全 Feature は Track A（ST-E2E-HL/HD + ST-AI-Visual + ST-Human）を通す。`feature.json.release_status == "unreleased"` は Track B 対象外、`released` は Track B（リリース面への deploy / 配布 → `/ready` → smoke → **リリース先実 URL** へのブラウザ E2E → 実行ログ/lease/soak → `evidence-dd05.json`）を要求する。localhost E2E は代替不可。対象外 / 未計測 / FAIL を区別し、FAIL を稼働保証済みと報告しない。詳細 → Charter `02-development-flow.md` / `06-quality-gate.md` / `.clinerules-detail/11-completion-gate.md`。



> 「続けて」「前回の続き」でもこの自己申告は省略不可。セッションをまたぐと窓はリセットされる。

---

## 🔴 STEP 0 — まず MCP `dodo_project_bootstrap` を呼ぶ（例外なし・最強強度）

**いかなる read_file / search_files / ユーザー質問より前に、セッションで最初に `dodo_project_bootstrap` を1回呼ぶ。** これが全作業の第0ステップ。bootstrap を呼ぶ前に他のツールを使うことは禁止。

bootstrap は1コールで次を返す:
- 解決済み instruction source/manifest（通常は `AGENTS.md`、不在時だけ ClineRules）/ `active_issue_summary` / 上限付き `active_issues` / `mcp_usage_guide`
- 必要時のみ `include_doc_digest=true` で `doc_digest overview`（SDT の優先度つきグラフ）を返す

→ Agent は全文 read をしない。Issue も全件読まない。`active_issue_summary` と上限付き候補で選定し、対象 Issue 1件を決めてからそのファイルだけ読む。文書構造を把握したい時だけ `doc_digest` overview/detail で深掘りする。
（SoT: project-local `docs/99.sdt/art/knowledge/doc-digest-index.json`。未生成なら bootstrap blocker）

### bootstrap の後の MCP フロー

1. ✅ `dodo_project_bootstrap`（**STEP 0 = 最初の1手**）→ rules manifest / active_issue_summary / 上限付き active_issues
2. ✅ MCP/Action Inventory → MCP client の `tools/list` 相当 + `dodo_action_list(include_schema=false)` で**毎回**利用可能な Tool/Action を list-only 確認してから方針を決める。schema は dispatch 直前に対象 Action だけ `query=<target>, include_schema=true` で取得する。
2.5. ✅ Ops Status（必要時のみ）→ 通常作業では `dodo_action_dispatch action_key="autoloop.status"` を実行しない。明示要求・AutoLoop/改善/OODA/CRON/scheduler/soak 自体の現在値・完了条件が要求する運用状態・観測後の状態変化確認に限って実行し、実行時は結果を 1 行明記する。同一 task では既存観測を再利用する。改善系タスクは `.clinerules-detail/20-navigation.md` の該当 Step を実施。
3. ✅ Adaptive WF Route → active Issue / Feature ID / user intent が見えたら `dodo_action_dispatch action_key="agn.route_next"` を呼び、`session_instruction` と `mode` を作業ナビにする。`standard` は `workflow.status`、`adaptive` / `exploratory` は `recommended_probes` を優先。
4. （マルチリポ時）`workspace_context.load` → 返った `clinerules_paths` を読む
5. Issue対応時だけ、上限付き `active_issues` から対象を選び、その1ファイルだけ読む。不足時は `active_issue_limit` を小さく増やして再bootstrapするか `dodo_agn_context command=tasks` で絞る。
6. `agn_session_startup command=dashboard` → AGN 概況（**JSON 全件 read 禁止**）
7. `agn_session_startup command=context target_id=<ID>` → `SPEC FILES`（解決済み物理パス）を取得
8. その物理パスだけを `read_file`

## 🚀 セッション開始時の Agent 選定（MANDATORY）

作業着手前に、変更対象から Operation を特定し、Operation が宣言する Agent を機械的に採用する。

1. `docs/99.sdt/agn/5.operations/operations.json` が存在する場合だけ、作業種別・変更対象から Operation を特定する。未初期化なら Agent を推測せず、catalog blocker と現 runtime Agent を明記する。
2. Operation の `attributes.agent` を使用 Agent とする。
3. `agent.context_pack(agent_id=<選定ID>)` を呼び、`persona` / `skills` / `guard.recommended_action_keys` / `context_pack_prompt` を一括取得する。
4. `context_pack_prompt` を初期メモリとして利用する。
5. 作業開始メッセージに `Operation: <operation-id> | Agent: <agent-id>` を明記する。

`agent.context_pack` が利用不能な場合のみ、`docs/99.sdt/agn/2.agents/<id>/agent.json` の直接参照へ fallback する。

❌ Operation を特定せず勘で Agent を選ぶ / `dodo_agent_list` を全件読んで目視選定する / context pack 未取得で作業開始する / `guard.module_scope` 外を理由なく編集する

### Tauri Startup Check（`active_services` 宣言時のみ）

`dodo_project_bootstrap` 成功後、`.dodoai/repo-context.json` の `active_services` に Tauri/Desktop stack が宣言されている場合だけ、セッション中 1 回確認する。`active_services` が空なら起動対象なしとして何も起動・再起動しない。宣言がある場合は service / port / 標準起動コマンドをそこから解決し、Desktop process/window、Vite、Provider、Core readiness、owner tmux の実 pane command を個別確認する。背面/最小化、Tauri sidecar の cold start、別 session の正当な owner は停止とみなさない。実停止と競合 owner 不在を確認した場合だけ owner 経路を非破壊で 1 回起動/再起動し、最大 45 秒再確認する。standalone Core を重ねない。

### MCP Recovery Gate（接続不能時も即直読みしない）

MCP endpoint は `.mcp.json` の stdio launcher / runtime-slot resolver が返した workspace lease を正とする。Tauri control port を generic Core fallback として推測・直書きしない。listener の停止・再利用は `/ready` owner と lease が一致するときだけ許可し、未検証 owner は touch しない。

`dodo_project_bootstrap` / `dodo_action_list` / `dodo_action_dispatch` が `gateway unavailable`、connection refused、timeout、空の tool list などで失敗しても、すぐに `read_file` / grep / 直接 JSON 参照へ降りてはいけない。まず bounded recovery を実施する。

1. 2〜3秒待って、同じ MCP 呼び出しを **1回だけ再試行**する（既に ready 済みで即復旧するケースを拾うための軽い一手。同一ツール×同一引数の乱打は禁止）。
2. まだ失敗する場合、resolver が返した endpoint の `/ready` を先に確認し、非 2xx の場合だけ `/health` で liveness と readiness failure を区別する。併せて同じ解決済み port の listener、`tmux ls`、`/ready` owner を確認する。sandbox 内の loopback refusal だけで process 死亡と断定しない。
3. listener が無い、または `/ready` が失敗する場合、同じ workspace lease の owner 経路で **非破壊に1回だけ** 起動・再起動を試す。別 owner / 未検証 listener は停止・再利用しない。`--ensure-sidecar` の cold-start は tmux session が無くても detached sidecar を自動起動するため、tmux session が存在しないこと自体は失敗シグナルではない。
4. cold boot（FastAPI + SQLAlchemy + Action registry 全体の import）は 10 秒を超えることが多い。起動/再起動トリガー後は単発チェックで諦めず、`/ready` を **3〜5秒間隔で最大45秒まで poll** してから次に進む。
5. `/ready` 成功後に `dodo_project_bootstrap` → `dodo_action_list(include_schema=false)` を再実行し、MCP 復帰を確認してから作業を続ける。
6. 45秒の poll window を使い切っても復旧しない場合のみ fallback として `doc-digest-index.json` や必要最小限のローカルファイルを read-only 参照する。Evidence には、最初の MCP エラー、復旧試行（health/listener/tmux/再起動有無/poll結果）、再試行結果、fallback 理由を必ず明記する。

---

## 🔌 MCP サーバー接続設定（外部 AI Agent 用）

**Claude Code / Codex / Cline など外部 AI Agent が dodoAI に接続する場合の必須設定**

### dodo / DODO 略称

ユーザーが `dodo` / `DODO` / `dodoAI` / `dodoAI Core` / `dodo core` / `DODO CODE` と言った場合は、特に断りがない限り、ローカルの **dodoAI Core リポジトリ**を指す。Codex / Claude / Cline / ClineRules の dodo 関連作業でもこの解釈を共有する。

**現行の DODO Reference Repository 正本パスは `/Users/hitoshimurakami/myApps/dodoai`**。移動確認が必要な場合は `dodo_project_index(query="dodoai", include_settings=true)` を呼び、`slug="dodoai"` の row の **`path` をリポジトリルートとして採用**する。`general` alias を正本 dodoAI row と誤認せず、重複 row を作らない。Core 実装・MCP 起動・参照ドキュメント・ランタイム状態の確認は、この解決済みパスを第一候補にする。MCP が接続不能な場合のみ、現在のワークスペースルートを fallback とし、降りた事実を Evidence に明記する。

### 接続エンドポイント

- **HTTP MCP / REST API**: runtime-slot resolver が返した workspace endpoint。Tauri control endpoint は desktop 明示経路だけ。
- **Frontend / Provider**: `.dodoai/repo-context.json` の `active_services` に宣言がある場合だけ、その値を使う。

### Agent MCP 設定

Claude Code / Codex / Cline はリポジトリの `.mcp.json` にある stdio launcher を使う。HTTP URL を各 Agent 設定へ複製せず、`DODO_CORE_SLOT_MODE=workspace` から sticky slot を解決する。固定 control port を generic default として残さない。

### 利用可能な MCP ツール（11個）

| ツール | 用途 | 主要パラメータ |
|-------|------|---------------|
| `dodo_project_bootstrap` | セッション初期化（最優先実行） | `include_rules`, `include_active_issues`, `active_issue_limit` |
| `dodo_action_list` | Action 一覧取得 | `include_schema`, `query`, `tag` |
| `dodo_action_dispatch` | Action 実行 | `action_key`, `payload`, `allow_high_risk` |
| `dodo_agn_context` | AGN コンテキスト取得 | `command` (dashboard/context/tasks/graph/schema) |
| `dodo_agent_list` | Agent 定義一覧 | `workspace_root`, `query` |
| `dodo_agent_get` | Agent 詳細取得 | `agent_id`, `include_markdown` |
| `dodo_skill_list` | Skill 定義一覧 | `workspace_root`, `query` |
| `dodo_skill_get` | Skill 詳細取得 | `skill_id`, `include_markdown` |
| `dodo_project_index` | プロジェクト一覧 | `query`, `include_settings` |
| `dodo_project_rules` | プロジェクトルール取得 | `project_id`, `sections`, `format` |
| `dodo_project_create` | 新規プロジェクト登録 | `name`, `slug`, `settings` |

最新・変動する外部情報または出典付き調査には Registry Action `websearch.query` を使う。`dodo_action_list(query="websearch", include_schema=true)` で schema を取得して `dodo_action_dispatch` で実行する。`answer` は provider model の統合文なので、`citations` / `search_queries` / `search_count` を併読し、高リスク判断と provider 間不一致は一次資料で再検証する。資格情報を payload に含めない。

### 接続確認コマンド

```bash
# workspace slotを解決して MCP サーバー疎通確認
resolved_port=$(dodo slot acquire --workspace "$PWD" | jq -r '.result.port')
curl -X POST "http://127.0.0.1:${resolved_port}/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Action 一覧確認
curl "http://127.0.0.1:${resolved_port}/api/actions/"
```

---

## 🚫 絶対禁止（Charter P1–P29 圧縮）

**User Runtime Reload Approval Gate（HARD）**: VS Code window / Extension Host / desktop application / その他ユーザーに見える UI・runtime の reload・restart は、**現在の会話でその操作自体についてユーザーが明示承認した場合だけ**実行する。修正・build・install・検証の依頼や過去の許可は実行許可ではない。必要ならユーザー自身による reload を案内する。

| # | 禁止 |
|---|------|
| P1 | Git 操作（commit/push/merge）— 専用 Harness 以外。特に `develop` / `main` / `master` への直コミット・直 merge 禁止。必要な場合は先に `feat/*` 等の作業ブランチへ切り替える |
| P2 | Mock data フォールバック（DD02 以降は実機結合） |
| P3 | **テスト失敗のまま完了報告** |
| P4 | CONTRACT.md なしの実装着手 |
| P5 | シークレット / 顧客実値のハードコード（テスト・fixture・Harness・golden dataset 含む） |
| P6 | 同一ツール×同一引数の 2 回以上呼び出し |
| P7 | Feature から Task Graph 直接生成（UC/FR から生成。IUC は廃止） |
| P8 | Charter 9 ファイル未読での開発着手 |
| P9 | **Task Graph JSON なしの開発着手** |
| P10 | SDT データの SQLite 永続化（SDT は JSON First） |
| P11 | `system-requirements.md` の NFR 適用判断に未確定を残したまま A02 完了・A03 着手（固有要件 / 共通 NFR 継承 / 対象外＋理由のいずれかを明示。現状は ADVISORY + HIL） |
| P12 | A02 完了時の `agn.multi_agent_review` 未実施、または3ロール approved 未達で A03 着手 |
| P13 | **Scaffold（A03）なしで DD01 着手**（S-A Gate AG-03） |
| P14 | Contract JSON なしで DD02 着手（S-A Gate DD01-CJ） |
| P15 | コンテキストフロー JSON 機械検証なしで DD Phase 着手（S-A Gate AG-02a） |
| P16 | 循環依存が残った状態で DD Phase 着手（S-A Gate AG-02b） |
| P17 | Architecture Invariant baseline 未凍結（A03 AG-04）で DD01 着手 |
| P18 | **CallGraph 影響調査なしのコード変更** |
| P19 | **CallGraph 巨大 JSON の直読み**（`callgraph.uc_reverse_lookup` 等 Action 経由で走査。JSON 丸読みは Action 不能時の fallback のみ → `callgraph.focus` / `callgraph.uc_reverse_lookup` Action（L0 HARD GATE #4）） |
| P20 | **ロードマップ / タスクグラフ status 未同期での完了報告**（完了主張の前に `roadmap.sync_gate` で `stale_task_status=0`/`missing_milestone=0`/`roadmap_drift=0` を確認。task-dd*.json status と feature.json dd_progress、roadmap-graph.json milestone が欠損/不同期のまま「完了」と言わない → `.clinerules-detail/11-completion-gate.md`） |
| P29 | **機械ループの SoT を Issue MD に置くこと**（自律ループの Select / Claim / status 遷移 / Close の正は**タスクグラフノード**（`task-dd*.json` / `feature.json`）。Issue（`.dodoai/issue/`）は人間可読 view + HIL 承認 + dispatch envelope であり、`_ready`/`_in-progress`/`_done` のファイル名 rename を一次 SoT とする経路を新設・拡張しない。既存経路は段階移行で縮退（所有 = `F-TASKGRAPH-DISPATCH-SOT`）。正本 = Charter 01 P29 / 04 §1.1） |


運用禁止の要点: Docker リビルド禁止 / 長いインラインスクリプト禁止（ファイルに書く）/ `rm -rf` 確認なし禁止（`trash` 優先）/ 長い出力は `| head` 制限 / `_in-progress` 放置で新タスク開始禁止 / 未登録外部 MCP 禁止 / テスト・fixture・Harness に秘密鍵・個人実値・実 credential/env/keychain 名を書かない / CRON レポート MD を変動状態の別正本として増殖させない / resolver を迂回して固定 port へ向けない。Tauri control port は desktop 明示経路だけに使う。

---

## 🧬 要件モデル定義順（BR → SR → UC → CAP → Mod）

> 📍 **層の関係が分からない / どこに書けばよいか迷った / 新しい BR・SR・FR・CAP を作ってよいか判断するときは、まず Charter [`07-requirements-architecture-map.md`](../docs/0.charter/07-requirements-architecture-map.md) を開く。**
> World Model → Core Concept → Strategy → 共通 BR/SR → 縦糸 EPIC/Feature/UC ⟷ 横糸 CAP/FR/MOD/DFR → Code → SQ/AC → Evidence の**接続・所有者境界・判断フロー**を単独所有する（各層の定義は再掲せず正本を指す）。

仕様・Feature 分解・コード作業の前に、**必ず BR → SR → UC → CAP → Mod の順で定義**する。**IUC は廃止**（IUC ノードを新設しない）。

- **BR** = Business Requirement（事業要求）
- **SR** = System Requirement（システム要求）
- **UC** = Use Case（ユースケース・最小の検証単位、IUC 下層なし）
- **CAP** = Capability（能力・FR を OWNS）
- **Mod** = Module（コード境界 = `dodo_core/module/<name>`）

縦糸 `BR → SR → UC → Evidence`（Feature は UC の束＝成果物）／横糸 `CAP（OWNS FR）→ Mod → Layer`。Feature/UC は FR を所有せず `references(label="satisfies")` で参照する。
縦糸と横糸は、Feature/UC の project-local A02 spec・TaskGraph と、`docs/4.common/3.capability-requirements/` + CAP/FR catalog に**責務分離**する。**1 フォルダに UC と FR を混載しない。** 物理 path は `sdt_layout.resolve` で解決し、未初期化なら推測配置しない。

**BR / SR / NFR / CAP / FR の新設は HIL 裁定を要する。** 共通 BR は `docs/4.common/1.business-requirements/`、共通 SR/NFR は `docs/4.common/2.system-requirements/`、CAP/FR の人間可読 view は `docs/4.common/3.capability-requirements/`、構造 SoT は各 JSON catalog が所有する。Feature 側で勝手に生やさない。Feature 内の具体は **UC の受入基準**で表現し、不足 FR は `fr_gap`（`proposed_id: null`）として裁定へ回す。

**EPIC / FEATURE / UC / CAP / FR / MOD は JSON First SoT。** 正本は `docs/99.sdt/agn/1.workflows/epic-catalog/epic-catalog.json`、`docs/99.sdt/agn/1.workflows/br-catalog/br-catalog.json`、`docs/99.sdt/agn/1.workflows/capability-catalog/capability-catalog.json`、`docs/99.sdt/agn/1.workflows/capability-catalog/capability-requirement-model.json`、および各 Feature の `feature.json`。MD は `md_ref` でつながる人間認知用ビューであり、JSON First を理由に物理削除しない。EPIC/FEATURE/UC/CAP/FR/MOD 構造変更を MD だけで済ませることは禁止。

**`requirements-weave.json` は同名で 2 種類ある。混同するとどちらかを壊す（2026/08/05 是正）。** どちらも ART だが `derivation` が逆であり、置き場で判別する。

| 対象 | パス | 契約 | 編集可否 |
| --- | --- | --- | --- |
| **Feature 単位の要求モデル本体** | `docs/99.sdt/art/requirements/{EPIC}/{FEATURE}/requirements-weave.json` | AUTH-R70 `agent` / **`source`** | ✅ Agent が起案・編集する。A02 の成果物そのもの。project-local MD view は `docs/98.dodoai-custom-spec/{FEATURE_ID}/`（WM-5 の対） |
| **全体集約カタログ** | `docs/99.sdt/art/catalog/requirements-weave.json` | AUTH-R27F `derived` | ❌ 手編集しない。上記カタログと `feature.json` から機械生成される。直すときは入力側を直して再生成する |

Feature 単位の weave は ART、集約 catalog は derived projection として分ける。project-local layout contract が未初期化なら物理 path を推測せず、`F-WORKSPACE-BOOTSTRAP` blocker とする（ART=成果物の正本 / AGN=ART を接続する因果グラフという `docs/99.sdt/README.md` の定義を反転させない）。
❌ 集約 weave を手編集して要求を変えない。❌ Feature 単位 weave を「生成物だから触るな」と誤読して A02 を止めない。


### Approved MD SoT（v2.1）

SDT = ART + AGN。**ART（成果物そのもの）が正本 SoT、AGN は ART を意味で接続する因果グラフ**（graph structure / traceability / task status / governance evidence / `md_ref`）。判別基準の単独所有は `docs/99.sdt/README.md`（ここへ再掲しない）。`docs/` 配下の人間可読ポリシー・概念・要求・手順も規範 SoT として扱い、SDT JSON があることを理由に draft 扱い・削除・無視しない。

- `approved/0.charter/` — 開発憲章、禁止事項、DD反復、Gate、テスト戦略。
- `approved/1.concept/` — プロダクト概念、アーキテクチャ概念、戦略。
- `approved/2.common/` — 共通 BR/SR、システムアーキテクチャ、glossary、module/reference docs。
- `approved/3.system/` — system epics、Feature docs、Capability docs。
- `approved/4.operation/` — autonomous execution loop、運用 runbook、運用ポリシー。
- `docs/5.test/` — test architecture、screen scenario definitions（2026/08/04 に凍結アーカイブから移設。`screens/*.json` が画面別 L7/L8 シナリオ SoT、対になるスキーマは `screen-test-scenarios.schema.json`）。
- `approved/6.manual/` — user manual、implementation-verification procedures。
- `approved/99.sdt/README.md` / `approved/99.sdt/art/**/*.md` — SDT/ART の人間向け説明・生成ドキュメント view。`approved/99.sdt/` 配下の JSON は引き続き機械可読 graph/data SoT。

SDT JSON と approved MD が矛盾する場合は、機械関係・status は SDT、規範文・意図・手順・読者向け要求は approved MD を優先し、片方を黙殺せず両方を同期補修する。

---

## 🏗️ 開発フェーズ順序（二経路 → A02 → A03 → DD01 → … 不可逆）

**コードや CONTRACT.md を書く前に、必ず A02（要件モデル6層 + 全体設計）→ A03（SDT/AGN Conformance Gate）を順に通してから DD01 に入る。Scaffold は DD01 内で生成し、検証なしに DD02 へ進めない。**この順序は逆転・スキップ不可。

```
Reverse: 既存資産 → CallGraph → SDT逆導出 → 文書投影 → drift裁定
                                                        │
Forward: Intent ────────────────────────────────────────┴→ A02 → A03 → DD01 → DD02 → DD03 → DD04 → DD05
                         （新EPIC/CAPを作る場合だけ A01）   ↑     ↑
                                                        AG-02  AG-01/03/04
```

- **A02 = 要件モデル6層（EPIC→FEATURE→UC / CAP→FR→MOD）を1セットで定義する + 全体設計（コンテキストフロー JSON + CallGraph 品質）→ AG-02 PASS。**
  - **A02 Step 0: EPIC / CAP 所有者存在ゲート（HARD RULE — Charter `02-development-flow.md` が正本）**: Feature 単位の A02 着手前に `epic-catalog.json` / `capability-catalog.json` で所属 EPIC・owning CAP の存在を確認する。新しい関心事が既存 EPIC / CAP に収まらない場合、**Feature を先に切らず EPIC / CAP の新設・改訂から始める**。既存 EPIC 拡張 vs 新設で迷う場合は HIL。❌ 所属 EPIC / owning CAP 未登録のまま Feature 単発 A02 禁止。
  - 「BR/SR/UC を定義して」「A02 をやって」はいずれも **EPIC→FEATURE→UC / CAP→FR→MOD の6層 1セット**を意味する。`capability-module.md`（CAP/FR/MOD）と CAP/FR カタログ登録を欠いたまま「要求定義完了」と呼ばない。Feature 単位の `requirements-weave.json`（`art/requirements/{EPIC}/{FEATURE}/` — AUTH-R70 `source`）は A02 の成果物であり Agent が書く。混同しやすい**集約**側（`art/catalog/` — AUTH-R27F `derived`）は手編集しない（上表参照）。

  - **A02 をやれば A03 が必然**：A02 完了は A03（SDT/AGN Conformance Gate）のトリガーであり、A02 単独で止めて完了報告してはならない。「S Phase だから」「実装は別工程だから」を理由に CAP/MOD・A02・A03 を勝手に省略・分割しない。ユーザーが「UC まででよい」等と**明示的に範囲を絞った時だけ**そこで止める。
  - **A02 成果物の配置先（HARD RULE — Charter `02-development-flow.md` §成果物 3 点セットが正本）**: 新規 Feature の要求定義は必ず **3 点セット** — ① Feature をリリースゴール一覧へ登録 ② 要求モデル MD（人間可読 SoT）を EPIC / Feature の文書ツリーへ ③ AGN（`feature.json` + `task-dd*.json` + カタログ / roadmap 同期 = Feature ⟷ UC/FR/Task の接続と status）を SDT の workflows ツリーへ。**物理パスは `.dodoai/repo-context.json` と SDT レイアウト契約が SoT**（本ファイルに焼き付けない。`sdt_layout.resolve` で解決する）。❌ AGN JSON だけ・MD だけの A02 完了禁止。❌ 要求 MD を要求モデルツリー以外へ新設禁止。
  - **この 3 点セットは「要求モデル」の配置ルールである。** 観測・実行・計測の記録（Evidence / テスト結果 / プロンプト等の逐語記録）は要求モデルではなく **ART**。新種の成果物を SDT へ追加するときは判別の正本 `docs/99.sdt/README.md` を開き（「成果物か → ART / 関係か → AGN」）、`.clinerules-detail/40-domain-gates.md` §2 の手順に従う。❌ 本ルールの語彙を流用して観測記録を AGN へ置くこと。


- **A03**: SDT/AGN 自己整合性・書き込み主権・要件語彙境界を検証する。コードは生成しない。
- **DD01**: Project-local Template から Scaffold を生成・検証し、凝集性・境界・Invariant baseline を凍結する。CONTRACT.md の `owned_files` は **DD01 で生成した骨格の実パス**を指す。

> ❌ A02 完了前に A03/DD01 着手禁止（P15/P16）。❌ A03 Conformance 完了前に DD01 着手禁止（P13）。❌ DD01 Scaffold + 凝集性 + Invariant baseline 凍結前に DD02 着手禁止（P28）。
> 正本: Charter `docs/0.charter/02-development-flow.md`（§A02 / §A03 / Gate 一覧 AG-*）。施行詳細: `.clinerules-detail/40-domain-gates.md` §1。


---

## 🔒 7つの HARD GATE（破ると壊れる）


1. **MCP Inventory Gate** — bootstrap 後、実装方針を決める前に MCP tool/action 一覧と schema を取得する。MCP 未露出時は §MCP Recovery Gate（再試行・health/listener/tmux確認・非破壊再起動1回）を実施し、それでも不可の時だけ fallback を Evidence に明記。
2. **Task Graph 存在ゲート（P9）** — `approved/99.sdt/agn/1.workflows/.../task-dd*.json` が無ければ作ってから DD01。
3. **A02 → A03 → DD01 順序ゲート（P13/P15/P16/P17/P28）** — DD01 着手前に A02（**要件モデル6層 EPIC→FEATURE→UC / CAP→FR→MOD の1セット定義** + 全体設計・AG-02）を通し、続いて A03（SDT/AGN Conformance）を PASS させる。DD01 内で project-local Template による Scaffold + ドメイン凝集性 + Architecture Invariant baseline 凍結を行い、DD02 入口で再検証する。**A02 完了は A03 のトリガー**であり、A02（特に CAP/FR/MOD まで）で止めて完了報告しない。A03 を飛ばして DD01/CONTRACT.md を作り始めず、DD01 Scaffold を飛ばして DD02 へ進まない。Action 不在時は手動検証して Evidence に明記。詳細 → Charter `docs/0.charter/02-development-flow.md`。

4. **Dev Preload + CallGraph（P18）** — 変更前に `callgraph.focus`（編集前ブリーフィング1コール: callers+callees+影響UC+境界リスク+チェックリスト）または `uc_reverse_lookup` で影響 UC/Feature/EPIC を把握し、Preload Evidence Block 行 #8 を出すまで変更禁止。Native Coding turn は composition root で `GateHarness` を必ず配線し、`target_file` 指定時は turn preflight、未指定時は `apply_patch` / `write_file` の各ファイル初回実行時に lazy `callgraph.focus` を行い、結果を次 iteration へ注入してから write を再試行する。ファイル単位キャッシュで同一 turn の重複 dispatch を防ぐ。Harness 経由の Codex / Claude Code / Cline dispatch は、workspace instructions の読込可否に依存せず P18 prompt をタスク先頭へ冪等注入する。プロンプト指示だけ・JSON 直読みだけ・未配線 Harness の単体テストだけで P18 PASS としない。初見モジュール把握は `callgraph.digest`。詳細 → `.clinerules-detail/10-preload-gate.md`。
5. **UI Semantic JSON Gate（画面/UI開発時）** — 画面・Template・Page・Atomic Design component・UI JSON を作る/直す前に、MCP 経由で `F-COCKPIT-UI-CATALOG/ui-components.json` の `semantic_review` を読む。重複候補は HIL 判断なしに新設しない。
6. **Zero Tolerance（P3）** — テスト失敗・カバレッジ <80% で「完了」と言わない。完了報告には `UT ✓ X passed / Coverage XX% ✅` を必須記載。
7. **Test Evidence + Roadmap Sync Completion Gate（P3/P9/P20）** — `attempt_completion`・DD Phase 完了・Feature/UC close の前に、MCP で①ガバナンス登録（`sdt.governance_metrics`）②`test_evidence.audit`（`gaps=0`/`broken_links=0`）③テスト PASS + Coverage ≥80% ④**`roadmap.sync_gate`（`stale_task_status=0`/`missing_milestone=0`/`roadmap_drift=0` — ロードマップ/タスクグラフ status 同期 + A02 milestone 反映）**を検証し、Completion Gate Evidence ブロックを出すまで「完了」と言わない。詳細 → `.clinerules-detail/11-completion-gate.md`。**SDT ガバナンス登録は A02 で行う（A03 は SDT/AGN Conformance、Scaffold は DD01）。**
   - **Completion Operation Hook sub-gate**: AGENTS/prompt/Skill/Operation Listは発見層であり強制機構ではない。Codex / Claude Codeの`Stop`とdodo Coderの`attempt_completion`を共通`sovereign.hook_gate`へ接続し、worksetに該当する宣言済みOperationを同一turnで遂行する。CRONは代用しない。High/criticalはcurrent explicit intentまたは`standing-scoped`範囲内のみ。同一plan fingerprintは1回だけ差し戻し、同じMCP callを反復せず、不能なら具体的blockerを1つ報告する。
   - **Specification-Conformance sub-gate**: MCP/status/Evidence を検証の代用にしない。全 SR/FR/UC→実装→acceptance test、A03 計画→実レイヤ/import、mutation safety、数値 NFR を current checkout で照合し、`PARTIAL` / `FAIL` / `NOT IMPLEMENTED` が1件でもあれば完了禁止。「1 Action」「自動合成」要件は live 最小入力で composition-root 配線まで確認し、caller 手動前処理が残れば `PARTIAL`。「実装して」に既存 done の再確認だけで返すことも禁止。延期する非 PASS は判定を維持して `_ready` Issue/STREAM + Task Graph に接続し Feature Complete を pending とする。既存管轄がある負債の重複 Issue 起票は禁止。
   - **DD05 Release sub-gate**: 全 Feature は Track A。`release_status=released` のみ Track B のリリース面 deploy/readiness/smoke/実 URL browser E2E/log Evidence を必須とする。`unreleased` は対象外、未計測と FAIL は別判定。FAIL を milestone done や稼働保証済みにしない。



---

## 🧭 次に何をやるべきか — Roadmap → Priority Intelligence

「次何やる？」「次のタスクは？」「今日やること」「着手可能な Feature は？」と問われた/迷った時は、**勘や口頭指示ではなく、実装済みの Roadmap + Priority Intelligence Engine（`F-SDT-PRIORITY`, done）で決める**。新規開発は不要。

```
① roadmap.derive        Feature 依存 → roadmap-phase グラフ（変化時のみ再導出）
② roadmap unlock eval    roadmap-graph.json から着手可能 Feature を判定
③ priority_cycle         候補→スコア→ポリシー→タスク化 = 優先度キュー
④ GET /priority/queue    先頭が「次にやるべき最有力タスク」→ 根拠付きで提示
```

- 最小手順: `dodo_action_dispatch action_key="priority_cycle"` → `GET /priority/queue` の先頭候補（`target_node_id` / `reason` / `priority_score`）を提示 → 承認後に HANDOFF/Issue 化。
- Feature 依存・新 Epic に変化があれば先に `roadmap.derive` で `roadmap-graph.json` を更新する。
- 詳細手順・REST/fallback → `.clinerules-detail/20-navigation.md`。着手後の status 同期 → `.clinerules-detail/11-completion-gate.md`（P20）。

---

## 📋 作業管理（最小）


- **Per-Work TaskGraph Lifecycle Gate（HARD）**: workspaceを変更する各作業は、①変更前にowning Featureを解決 ②今回専用task nodeを先に作成 ③対応Issue viewを作成 ④claim/lease取得 ⑤`ready → running` 後に初めて編集、の順を守る。**既存Featureの `feature.json`、既存DD task、過去Issueの確認だけでは代替不可。** 作業後は同じnodeへ変更・test/Action・Evidence・残課題を記録し、実態どおり `done` / `blocked` / `failed` / `running` へ遷移、同一作業でIssue suffix/bodyを同期してleaseを解放する。Gateを飛ばした後追いTaskを「作業前証跡」と称さない。
- **Agent 生成ファイル追跡 Gate（HARD）**: Task / Issue / Evidence は現在 checkout 中の同一 worktree に作り、作成直後に明示 path だけを stage する。MCP / Action へ別 checkout の `workspace_root` を渡して正本 worktree に `??` だけを残すこと、完了・handoff・push 後に Agent 生成の未追跡ファイルを残すことを禁止する。CI 修復 / ローカル変更一括 push は既存 local commit の直上で行い、明示要求なしに別 clone / worktree / 一時 branch / snapshot ref / patch 転送を作らない。
- **Issue は人間可読 view + HIL 承認 + dispatch envelope であり、機械ループの SoT ではない（P29）。** タスク状態の正はタスクグラフノード（`task-dd*.json` / `feature.json`）。Issue の status 変更（rename）を行う時は、同一作業内で対応する task node の status / Evidence ref を同期する（値の正は task node 側）。
- **「次やること」「計画」「精査結果」を書くときも同じ対規律（WM-5 / P29）**: 正本は TaskGraph ノード（`task-dd*.json` / `feature.json` / `roadmap-graph.json`）であり、MD（Issue / HANDOFF / 計画メモ / レポート）はその人間可読 view。①TaskGraph に存在しない計画を MD だけに書かない（先に task node を作成/更新してから MD view を書く）②TaskGraph だけ更新して人間可読 view を残さない ③「次何やる？」への回答は必ず task node（status=ready の実ノード）と対応 Issue のペアで提示する。ユーザーが明示しなくてもこの対で出力するのが既定動作。
- 作業計画は TaskGraph node を正本として `.dodoai/issue/` に view を作る。テンプレ: `docs/99.sdt/agn/0.schema/issue-handoff-template.md`
- 命名: `{YYYYMMDD}_HANDOFF_{status}.md`（`_ready`→`_in-progress`→`_done`）
- 完了メッセージにフルパスを記載。

---

## 🗂️ 詳細が要るとき → L1 索引へ


具体手順・ポート表・テスト層・AGN 登録・Clean Arch・防衛等の詳細は **本ファイルに無い**。
→ **`.clinerules/00-INDEX.md`** のトリガー表で該当 L2 ファイルを特定し、その時だけ読む。

> L2 詳細施行規則は `.clinerules/` の外（**`.clinerules-detail/`**）に置いてある（参照層）。
> `.clinerules/` に置く fallback entrypoint は L0(本ファイル) + L1(索引) の **2ファイルだけ**。通常セッションは `AGENTS.md` のみを注入し、`AGENTS.md` が利用できない時だけこの2つを fallback authority として読む。
