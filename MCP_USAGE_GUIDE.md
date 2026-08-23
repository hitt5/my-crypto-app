---
type: guide
title: dodo Core MCP 利用ガイド
description: MCP の段階的開示、Action 選択、SQ/AC/UC/CallGraph の読み分けを定める利用ガイド。
resource: MCP_USAGE_GUIDE.md
tags: [mcp, progressive-disclosure, token-efficiency, callgraph, sdt]
timestamp: 2026-08-01T00:00:00Z
---

# dodo Core MCP 利用ガイド

この文書は MCP 利用の詳細 SoT。セッション開始時は全文を読まず、bootstrap の L0 essence と
`mcp.usage_guide(section=...)` で必要な節だけ取得する。

## 0. 30 秒で分かる結論

1. 最初に `dodo_project_bootstrap` を bounded payload で呼ぶ。
2. `dodo_action_list(include_schema=false)` で Action inventory を確認する。
3. 実行直前に対象 Action だけ `include_schema=true` で schema を取得する。
4. 最新・変動する外部情報や出典付き調査には `websearch.query` を使う。
5. callers / callees は CallGraph、単一 Module の実装フローは SQ、Module 横断は AC、Feature / EPIC 影響は Designed UC から辿る。
6. 巨大 JSON、全 Issue、全 schema、ガイド全文を起動時に読み込まない。

## 1. 接続情報

接続先・ポート・起動方法は `.dodoai/repo-context.json` と `.clinerules-detail/30-environment.md` を参照する。
値をこのガイドへ複製しない。MCP が不通なら AGENTS.md の Recovery Gate を通し、即座に直接読みに降りない。

## 2. 公開ツール一覧

固定一覧は持たない。現在の Action Registry を `dodo_action_list(include_schema=false)` で取得する。
代表的な入口だけを示す。

| Tool / Action | 用途 |
| --- | --- |
| **`dodo_project_bootstrap`** | rules manifest、bounded Issue候補、MCP L0 essence |
| **`dodo_action_list`** | 動的 inventory と対象限定 schema |
| **`dodo_action_dispatch`** | Action 実行 |
| **`websearch.query`** | OpenAI / Anthropic / Gemini の Web Search を共通 request / response で実行 |
| **`mcp.usage_guide`** | 本ガイドの単一節を取得 |
| **`sdt.search`** | SDT上のSQ/AC/UC候補を対象限定検索 |
| **`callgraph.focus`** | 対象記号の callers / callees と編集ブリーフ |
| **`callgraph.uc_reverse_lookup`** | Designed UC → Feature → EPIC の影響逆引き |
| **`callgraph.ac_sq_trace`** | AC↔SQ全体トレース。必要時のみ、関数ノードは既定で除外 |

## 3. シナリオ別の使い分け

| 問い | 使う層 / Action | トークン節約と判定規律 |
| --- | --- | --- |
| 誰がこの関数を呼ぶ / 何を呼ぶか | CallGraph / `callgraph.focus` | 対象記号、`detail=compact`、必要な深さだけ |
| このコードはどの実装フローか | SQ / `sdt.search` | 対象 + `SQ`、小さい `limit`、`include_context=false`、`include_roadmap=false` |
| この変更は Module 境界を越えるか | AC / `sdt.search` | 対象 + `AC module_scope cross`。全体トレース生成は通常行わない |
| どの Feature / EPIC に影響するか | Designed UC / `callgraph.uc_reverse_lookup` | `C:WorkUnit` / `UC-` だけを UC と数える |
| この1週間の情報など最新の外部事実を調べたい | Web Search / `websearch.query` | `dodo_action_list(query="websearch", include_schema=true)` で schema を取得し、必要なら provider を変えて照合する |

SQは `C:Sequence` / `SQ-` / `module_scope: single`、ACは `C:ImplementationActivity` / `AC-` /
`module_scope: cross`、UCは `C:WorkUnit` / `UC-` / Designed Truth。private helper やSQをUCとして数えない。
Feature / EPIC が0件でUC欄にhelperやSQが並ぶ場合、P18は未成立としてFindingを残す。

`tools/list` は既定で native tool だけを返す。全 Registry Action の個別 MCP Tool が必要なら
`tools/list(include_actions=true)` を指定するが、通常は bounded な `dodo_action_list(query="websearch")` を使う。
`websearch.query` の `answer` は Search API の生レスポンスではなく provider model が検索結果から生成した統合文である。
根拠は `citations`、実行内容は `search_queries` / `search_count` で確認し、Action 成功を真実性の証明にしない。
高リスク判断と provider 間不一致は一次資料で再検証する。API key は共有 credential resolver が解決し、payload に含めない。

## 4. MCP First 原則

- workspace識別、Action inventory、schema、実行、EvidenceをMCP経由で取得する。
- `sdt.search` は対象語と `limit` で絞り、不要な context / roadmap 展開を切る。
- `callgraph.focus` は巨大CallGraph JSONの代わりに compact brief を返すために使う。
- Action出力の成功は仕様適合やFeature完了の証明ではない。各ゲートのEvidenceを分離する。

## 5. 禁止事項

- 起動時に全Issue、全Action schema、本ガイド全文、巨大SDT/CallGraph JSONを読む。
- SQ / AC（Implemented Truth）をUC（Designed Truth）として命名・集計する。
- private helperをUCとみなし、Feature / EPIC 0件の逆引きをP18 PASSとする。
- `callgraph.ac_sq_trace(include_cg_functions=true)` を理由なく実行し、関数ノード全件を返す。
- Actionのschemaが存在することを実行成功の証拠にする。

## 6. LN URI

`ln://` は `ln_registry.resolve` で物理パスへ解決する。解決失敗時は
`.clinerules-detail/10-preload-gate.md` の heal plan → dry-run → integrity 手順に従い、registry JSONを手編集しない。

## 7. トラブルシュート

- MCP不通: `.clinerules-detail/30-environment.md` の Recovery Gate。
- Action not found: inventoryを再確認し、registry stale時だけ既定の復旧手順を使う。
- SQ/ACが見つからない: 対象パス・qualified name・ID prefixを変えて bounded `sdt.search`。巨大JSON直読へ降りない。
- UC逆引きがhelperを返す: Designed UCとして採用せず、SQ/UC分離不足をFindingにする。
- 出力が大きい: `limit`、`detail=compact`、`include_context=false`、`include_roadmap=false` を優先する。

## 8. 配布と保守

bootstrap は本ガイドの全文ではなく L0 essence と節索引だけを返す。Actionの追加・改名時は固定一覧を増やさず、
動的 inventory を正本とする。本ガイドの見出し番号は `mcp.usage_guide` の section mapping と同期する。
