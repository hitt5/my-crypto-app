# Workflows — タスクグラフ

EPIC → Feature → Task Graph の階層構造。

## 構成

```
1.workflows/
└── {epic-name}/
    └── features/
        └── {feature-id}/
            ├── feature.json      ← Feature 定義
            ├── task-dd01.json    ← DD01 タスク
            ├── task-dd02.json    ← DD02 タスク
            └── task-dd03.json    ← DD03 タスク
```

## EPIC ディレクトリの作成

新しい EPIC を追加する場合:

```bash
mkdir -p docs/99.sdt/agn/1.workflows/EPIC-SEMANTIC-DIGITAL-TWIN/features/
```
