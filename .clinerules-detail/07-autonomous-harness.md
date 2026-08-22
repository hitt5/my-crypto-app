# 自律実行機構（Agent Harness Runtime）

正本: `docs/0.charter/01-development-charter.md`

## 原則
人間は設計し、Agentが自律実行する。タスクグラフ → Harness自動ディスパッチが正規パス。

## Harness Loop
Select → Plan → Dispatch → Observe → Verify → Close

## Runtime Adapters（交換可能）
Codex / Claude Code / Copilot / Cline — いずれも Agent の実行エンジンであり、Agent 自体ではない。

## Agent 体制

| Layer | 目的 | 説明 |
|-------|------|------|
| **Development** | モジュール単位の DD01/DD02/DD03 実装 | 並列 dispatch 可能 |
| **Operations** | ガバナンス・整合性検証 | CRON / on-demand |
| **Coordination** | タスクグラフ生成・依存解析 | dispatch 計画 |

## 制約
- Evidence をタスクグラフに書き戻す
- 全 Agent 実行は Harness 経由（O8 参照）
