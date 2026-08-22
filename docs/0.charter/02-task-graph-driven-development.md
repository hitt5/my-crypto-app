# タスクグラフ駆動開発

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## 概要

開発はタスクグラフが起点となる。タスクグラフは状態空間であり、Intent（意図）から Code、Test、Evidence、Finding までを同一グラフで追跡できる。

## タスクグラフの構造

```
docs/99.sdt/agn/
├── 0.schema/           ← JSON スキーマ定義
├── 1.workflows/        ← EPIC → Feature → Task Graph
│   └── {epic}/
│       └── features/
│           └── {feature}/
│               ├── feature.json
│               ├── task-dd01.json
│               ├── task-dd02.json
│               └── task-dd03.json
├── 2.agents/           ← Agent 定義
│   └── {agent-name}/
│       └── agent.json
└── 3.skills/           ← Skill definitions
    └── operation-list.md
```

## タスクグラフ JSON の読み方

### feature.json
Feature の定義。`spec_refs` で仕様ファイルへのリンクを持つ。

### task-dd*.json
DD Phase ごとのタスク定義。`depends_on` で依存関係、`gate` で完了条件を定義。

## グラフ走査のルール

- JSON を全件 read_file しない（必要分だけ取得）
- `depends_on` チェーンを辿って依存関係を把握
- `status` フィールドで進捗を確認（draft / ready / running / done / failed）
