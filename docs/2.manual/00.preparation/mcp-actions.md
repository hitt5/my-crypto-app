# MCP / Action 一覧（本テーマで使うもの）

> Preparation / Structuring で使用する MCP tool・dodoAI Core Action・Custom Action のカタログ。
> Action の詳細 schema は `dodo_action_list(query="<key>", include_schema=true)` で取得する。

---

## MCP tools（gateway: `dodo-core`）

| Tool | 用途 |
|------|------|
| `dodo_project_bootstrap` | セッション開始（rules / issues / usage guide 取得） |
| `dodo_action_list` | Action 一覧・schema 取得 |
| `dodo_action_dispatch` | Action 実行 |
| `dodo_agent_list` / `dodo_agent_get` | Agent 定義の選定・ロード |
| `dodo_agn_context` | AGN タスクグラフ概況・context 取得 |

## dodoAI Core 標準 Action

| Action key | 用途 | 備考 |
|-----------|------|------|
| {例: callgraph.uc_reverse_lookup} | {影響逆引き} | {備考} |
| {例: sdt.search} | {SDT 横断検索} | {備考} |
| {追加する} | | |

## Custom Action（`.dodoai/custom_actions/`）

| Action key | 実装 | 用途 |
|-----------|------|------|
| {例: verify.gate_check} | `.dodoai/custom_actions/{action_name}/` | {生成物の合格条件を機械判定する等} |

> Custom Action の仕様（A02）は [docs/98.dodoai-custom-spec/](../../98.dodoai-custom-spec/00-overview.md) に置く。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | {YYYY/MM/DD} | 初版作成 |
