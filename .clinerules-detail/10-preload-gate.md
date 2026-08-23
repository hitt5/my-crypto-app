---
type: procedure
title: Preload Gate — コード変更前の必須前提ロード
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, hard-gate, preload, callgraph]
---

# Preload Gate（HARD GATE）

**適用範囲**: すべてのコード変更。DD02/DD03、バグ修正、テスト追加、リファクタも例外なし。
**根拠**: Charter 禁止事項 P18（CallGraph 影響調査なしの開発着手禁止）。条文の正本は Charter。

## 停止条件

**下の Evidence Block を出力するまで、コード変更を開始してはならない。**
「前回の続き」「小さい修正だから」「口頭で指示された」はいずれも省略の理由にならない。

## 手順

### Step 1 — 対象の特定
`dodo_project_bootstrap` の `active_issues` から作業対象を選ぶ（`_in-progress` → `_ready` の順）。
選んでから、その Issue ファイルだけを読む。全件読みはしない。

### Step 2 — Task Graph 接続（P9）
`agn_session_startup`（`command=context`, `target_id=<ID>`）で Task Graph と spec_files を取得。
Task Graph が存在しなければ、**UC/FR から作成してから**着手する。無いまま DD01 へ進んではならない。

### Step 3 — 仕様の読み込み
Step 2 が返した `SPEC FILES` を read_file する。`ln://` が返った場合は直接 read_file せず
`ln_registry.resolve` で物理パスへ解決する。解決できなければ
`sdt.ln_link_heal_plan` → `sdt.ln_link_autoheal`（dry_run から）→ `sdt.ln_link_integrity`。
手で grep して探したり、`ln-registry.json` の `physical_path` を手編集したりしてはならない。

### Step 4 — CallGraph 影響調査（省略不可）
変更対象のファイル/関数に対して実行する。**静的な trace 参照では代替できない。**

同じコード記号に対しても、答える問いごとに参照する層を分ける。SQ / AC は Implemented Truth、
UC / Feature / EPIC は Designed Truth であり、同じ一覧として数えてはならない。

| 問い | 先に読む層 / Action | 判定・停止条件 |
|---|---|---|
| このコードはどの実装フローか | **SQ**。`sdt.search` を対象パス・記号と `SQ` で絞る | `C:Sequence` / `SQ-` / `module_scope: single` を満たす候補だけを SQ として扱う |
| この変更は Module 境界を越えるか | **AC**。`sdt.search` を対象パス・記号と `AC module_scope cross` で絞る。全体の AC↔SQ 関係が必要な場合だけ `callgraph.ac_sq_trace`（`include_cg_functions=false`） | `C:ImplementationActivity` / `AC-` / `module_scope: cross` を満たす候補だけを AC として扱う |
| 誰がこの関数を呼ぶ / 何を呼ぶか | **CallGraph**。`callgraph.focus`（対象既知）または `callgraph.digest`（不慣れな Module） | callers / callees の実コード関係として扱う。SQ / AC / UC の型判定へ流用しない |
| どの Designed UC / Feature / EPIC に影響するか | **UC**。`callgraph.uc_reverse_lookup`（`depth=2`, `include_callers=true`） | private helper や `SQ-` が UC として返る、または Feature / EPIC が 0 の場合は P18 を PASS にせず、`sq_matches` と `uc_matches` の分離不足を Finding とする |

`sdt.search` は `limit` を小さくし、原則 `include_context=false` / `include_roadmap=false` で対象を絞る。
SQ / AC の確認は CallGraph 影響調査の代替ではなく、`callgraph.focus` / `callgraph.uc_reverse_lookup` の
結果を正しい Truth Type で解釈するための事前分類である。巨大な SQ / AC / CallGraph JSON の直読みは禁止する。

`callgraph.focus` の markdown 出力はそのまま下の Evidence 行 #6 に貼れる。

### Step 5 — Evidence Block 出力

```md
## Preload Evidence Block
| # | 項目 | 値 |
|---|---|---|
| 1 | Issue / HANDOFF | <path> |
| 2 | Feature / UC | <ID> |
| 3 | Task Graph | <task-dd*.json path> |
| 4 | Spec Files 読込 | <list>（ln:// は解決済み） |
| 5 | Operation / Agent | <OP-ID> / <agent-id> |
| 6 | **CallGraph Impact** | 影響 UC=<n> / Feature=<...> / EPIC=<...> / boundary risk=<...> |
| 7 | 変更予定ファイル | <list> |
```

## Native Coding の場合

プロンプトに書くだけでは P18 遵守にならない。機械的に強制する。

- 本番の `AppendCodingTurnUseCase` は composition から `GateHarness` を受け取る
- `target_file` 指定時は turn preflight で調査する
- 無指定時はファイルごとの初回 write を遅延させ、`callgraph.focus` を lazy に注入してから再試行する
- Harness から Codex / Claude Code / Cline へ dispatch する際は P18 プロンプトを冪等に前置する
  （ワークスペース指示の読み込みだけを配送経路にしない）

Harness に結線されていないテストや、プロンプトのみの誘導は P18 適合とみなさない。

## 領域別の追加ゲート

画面/UI・SDT データ・アーキテクチャ境界を触る場合は `40-domain-gates.md` の該当節も満たすこと。

### Custom UI authoring

`.dodoai/custom_ui/*/manifest.json`、Custom UI block、block catalog を新規・変更する場合はコード編集前に次を実行する。

1. JSON manifest で画面を新規作成・編集する場合は `nocode-screen-compose` Skill をロードし、書き込み Action は `custom_ui.manifest_edit` に固定する。
2. `custom_ui.design_guide` を対象 `block_types` と bounded `limit<=50` で dispatch し、JSON catalog の prop / children / data-source contract を取得する。
3. 変更対象 manifest path だけを `custom_ui.manifest_lint` の `mode="strict"` で検査する。最大 20 manifest / 200 findings を超える作業は分割する。
4. 既存 manifest 全体は `mode="compatibility"` で別に観測する。warning を変更対象の PASS と相殺せず、未返済 debt は Finding / STREAM に残す。
5. 実書き込み前に `custom_ui.manifest_edit` を `dry_run=true` で実行し、`ok=true` / `error_count=0` を確認する。

TypeScript 内へ block type の第二リストを作らない。正本は `frontend/src/modules/custom-ui/domain/block-catalog.json`、TypeScript はその read-only view とする。

### Figma Atomic Design import

Figma の Atomic Design コンポーネントをソースへ反映する場合はコード編集前に次を実行する。

1. `figma-atomic-design-import` Skill をロードする。
2. Figma は正式化済みコンポーネントのセクション URL だけを読み、ファイル全体・ページ全体を一括 import しない。
3. セクション内で仕様テキスト、実コンポーネント本体、説明用 Frame、サンプルを見分ける。
4. `ui.component_catalog` と粒度分類標準を確認し、既存 dodo-ui 実体・旧配置・重複・import の照合結果を Evidence に残す。
5. 反映は 1 コンポーネント単位で行い、T2-B の整理（旧配置・重複・import 差し替え）は対象コンポーネントの Figma 反映と同じ単位で実施する。
