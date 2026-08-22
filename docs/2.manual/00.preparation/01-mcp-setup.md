# 01 — MCP セットアップ（Session Startup Protocol）

> Preparation の最初の手順。Agent が dodoAI Core と接続し、ルール・Action を取得する。

---

## セッション開始プロトコル

1. **`dodo_project_bootstrap`** を最初に呼ぶ（bounded payload）
   - rules manifest / active_issue_summary / mcp_usage_guide を取得
   - registry mismatch の場合は `dodo_project_index` / `project.settings` で登録済み slug を解決してから再実行
2. **`dodo_action_list(include_schema=false)`** で利用可能 Action の一覧を取得
   - schema は dispatch 直前に `dodo_action_list(query="<action>", include_schema=true)` で取得
3. **`dodo_agent_list` → `dodo_agent_get`** で作業に合う Agent 定義を初期メモリにロード
4. `.clinerules/00-CORE.md` と `docs/0.charter/01-development-charter.md` を読む

## MCP 接続不能時（MCP Recovery Gate）

即座に直接ファイル読みへ降りず、以下を実施する:

1. 2〜3秒待って同じ MCP call を1回だけ再試行
2. `/health`・`:8510` listener・`tmux ls` を確認
3. listener 不在/stale 時のみ非破壊 sidecar 起動/再起動を1回
4. `dodo_project_bootstrap` と `dodo_action_list` を再実行
5. なお不可の場合だけ Evidence 付きで read-only fallback

## プロジェクト登録の確認

```jsonc
// dodo_project_index で本プロジェクトが登録済みか確認
{ "query": "{project-slug}", "include_settings": true }
```

未登録の場合は `dodo_project_create` で登録する。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | {YYYY/MM/DD} | 初版作成 |
