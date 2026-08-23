---
name: {skill-id}
description: この Skill が何をするかを 1 行で（Agent がこの行だけで選択できるように書く）
category: {{THEME_ID}}
version: 1.0.0
---

# Skill: {Skill 名}

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Category | {{THEME_ID}} |
| Steps | 担当する手順ステップ |
| Created | {{DATE}} |
| 実行状態の正本 | `skills.json`（Skill 定義時に同階層へ作成）の `SKILL-{SKILL-ID}`（`status` / `executions` / `blocked_by`） |

> 実行状態（status / executions / 実測結果）を本 MD に転記しない。二重管理になり乖離するため、機械可読な `skills.json` を単一の正本とする（整合性はテストで強制する）。

## Purpose

**なぜこの Skill が必要か**を書く。手順の羅列ではなく、これを飛ばすと何が壊れるかまで書く。

## When to Use

- ✅ 使うべき状況
- ❌ 使わない状況（→ 代わりに使う Skill を示す）

## Prerequisites

**Required**:
- 前提条件（欠けていると実行できないもの）
- 必要な Action が登録済みであること（`dodo_action_list` で確認）

**Optional**:
- あると良いもの

**Blocking**: 前提が欠けている場合に**先に実行すべき Skill** を明示する。

## Steps

### Step 1: {手順名}

具体的な操作を書く。Action を使う場合は payload 例を示す。

```jsonc
// まず dry-run。schema は実行直前に dodo_action_list で確認する
{ "action_key": "{action.key}",
  "payload": { "workspace_root": ".", "write": false } }
```

### Step 2: {手順名}

> ⚠️ 落とし穴・破ってはいけない制約をここに書く（過去に踏んだ失敗を残す）。

### Step 3: 検証

出力が想定どおりかを確認する観点を書く。

## Output

- 生成物・更新されるファイルのパス（正本の場所）

## Success Criteria

- ✅ 検証可能な合格条件（「〜が 0 件」「〜が全件接続されている」など数えられる形で書く）
- ⬜ 未達の項目は正直に `⬜` で残す

## Related Skills

- **{skill-id}**: 前段 / 後段の関係を書く

## Related Documentation

- **手順詳細**: `docs/2.manual/...`
- **Action 契約**: `.dodoai/custom_actions/{action_name}/CONTRACT.md`
