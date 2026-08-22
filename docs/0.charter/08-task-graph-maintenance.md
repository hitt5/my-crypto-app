# タスクグラフメンテナンス

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## メンテナンスルール

### JSON ファイルが SoT

タスクグラフの正本は `docs/99.sdt/agn/` の JSON ファイルのみ。

### ステータス遷移

```
draft → ready → running → done
                    ↓
                  failed → draft
```

### 整合性チェック

| チェック項目 | 内容 |
|------------|------|
| Schema Conformance | type/status が規定値に準拠しているか |
| spec_refs Resolution | 参照パスが実在するか |
| 三位一体 Integrity | DD01 に CONTRACT/skeleton が存在するか |
| depends_on 妥当性 | 依存先ノード ID が定義済みか |

### 配置ルール

```
docs/99.sdt/agn/
├── 1.workflows/{epic}/features/{feature}/
│   ├── feature.json
│   ├── task-dd01.json
│   ├── task-dd02.json
│   └── task-dd03.json
├── 2.agents/{agent-name}/agent.json
└── art/operations/operation-list.md
```
