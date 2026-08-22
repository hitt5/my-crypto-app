# 01 — 構造化手順（Structuring Procedure）

> [../00-overview.md](../00-overview.md) の Phase 2（Structuring）本体。
> [1.concept/03-approach.md](../../1.concept/03-approach.md) のステップ分解を、実行可能な手順に落とす。

---

## 前提

- [00.preparation/01-mcp-setup.md](../00.preparation/01-mcp-setup.md) 完了（MCP 接続・Agent 選定済み）
- 入力資産が揃っている（{入力資産を列挙する}）

## 手順

### Step 1: {ステップ名}

- **入力**: {入力}
- **実行**: {使用する Action / コマンド}

```jsonc
// dodo_action_dispatch の例
{
  "action_key": "{action.key}",
  "payload": {
    "workspace_root": ".",
    "write": false   // まず dry-run、確認後に true
  }
}
```

- **出力**: {出力先パス（docs/99.sdt/art/ 配下）}
- **合格条件**: {機械判定できる条件（exists / json_valid / 件数 など）}

### Step 2: {ステップ名}

- **入力**: {入力}
- **実行**: {Action / 手作業}
- **出力**: {出力}
- **合格条件**: {条件}

### Step N: HIL 確認

- 生成物を人間がレビューし、[4.evaluation](../../4.evaluation/00-overview.md) の HIL ゲートで承認する。

## 出力先一覧（正本 = docs/99.sdt/art/）

| 成果物 | パス | 形式 |
|--------|------|------|
| {成果物1} | `docs/99.sdt/art/{path}` | JSON |
| {成果物2} | `docs/99.sdt/art/{path}` | Markdown（人間可読ビュー） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | {YYYY/MM/DD} | 初版作成 |
