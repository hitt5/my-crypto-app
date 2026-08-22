---
title: Skills — {{PROJECT_NAME}}
updated: {{DATE}}
---

# Skills

プロジェクトの**大まかな手順を再利用可能な手続き**として定義したもの。
1 Skill = 1 手順の塊。Agent はこれを読んで実行する。

| 形式 | `{category}/{skill-id}/SKILL.md`（YAML frontmatter + 本文） |
| --- | --- |
| category | `{{THEME_ID}}` |
| 雛形 | [`SKILL.template.md`](SKILL.template.md) をコピーして使う |
| 参照元 | `art/operations/operation-list.md`（Operation → Skill の紐付け） |

---

## Skill 一覧

> **TODO: 本テーマの手順を Skill として定義してください**

| Skill | 担当ステップ | 状態 |
| --- | --- | --- |
| `{skill-id}` | - | ⬜ 未定義 |

> ⚠️ **状態は実測を書く**。`✅ 実行可` は「必要な Action が実在して動く」ことを指し、
> `⬜` は手順は定義済みだが実行に必要な Action / 入力が未整備であることを指す。
> `status` フィールドや過去の記録を根拠に `✅` と書かない。

## 実行の前提

| # | 前提 |
| --- | --- |
| 1 | MCP `dodo_project_bootstrap` が成功していること |
| 2 | Skill は**手順の正本ではあるが承認権を持たない**。HIL ゲートは人間が判断する |
| 3 | SoT への書き込みは Action 経由のみ（Skill が直接ファイルを書き換える手順を書かない） |
| 4 | 顧客実値・クレデンシャルを Skill 本文に書かない（Charter P5） |

## 依存関係（実行順序）

> **TODO: Skill の実行順と HIL 承認点を記述してください**

```text
{skill-a}
    ↓
{skill-b} ──→ [HIL 承認]
```

> 土台となる Skill（入力データを作る工程）を飛ばして表示層・成果物層の Skill を実行すると、
> **中身が無いまま構造だけができる**。依存順序は明示すること。
