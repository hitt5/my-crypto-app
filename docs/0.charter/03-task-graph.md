# タスクグラフ定義

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## タスクグラフのノード型

| ノード型 | 説明 | dispatch 可否 |
|---------|------|:---:|
| `epic` | EPIC レベルのグルーピング | ❌ |
| `feature-group` | Feature レベルのグルーピング | ❌ |
| `uc-task` | UC 単位のタスク（推奨 dispatch 単位） | ✅ |
| `fr-task` | FR 単位のタスク | ✅ |
| `integration-task` | 統合タスク | ✅ |

## 依存関係ルール

- `depends_on` フィールドで先行タスクを指定
- 依存先が全て `done` でないと実行開始不可
- Wave 構造: 同一 Wave 内は並列実行可能

## タスク JSON スキーマ

### feature.json

```json
{
  "id": "F-XXX-YYY",
  "name": "Feature 名称",
  "epic": "EPIC_XX",
  "priority": "P0|P1|P2",
  "status": "draft|ready|running|done|failed",
  "phase": "DD01|DD02|DD03",
  "spec_refs": {
    "sr": "docs/.../system-requirements.md",
    "iuc": "docs/.../iuc.md"
  }
}
```

### task-dd*.json

```json
{
  "id": "F-XXX-YYY-DD01",
  "feature": "F-XXX-YYY",
  "type": "uc-task|fr-task|integration-task",
  "status": "draft|ready|running|done|failed",
  "gate": "完了条件の記述",
  "depends_on": ["F-ZZZ-DD01"],
  "spec_refs": ["UC-XXX", "FR-XXX-01"],
  "deliverables": ["path/to/CONTRACT.md"]
}
```

## ステータスモデル

```
draft → ready → running → done
                    ↓
                  failed → draft（Finding → 修正 → 再実行）
```

## 禁止事項

- ❌ Feature / IUC 単位でタスクグラフを直接生成（P7）
- ❌ タスクグラフ JSON なしで DD01 に着手（P9）
- ❌ `depends_on` 未充足の状態でタスクを `running` に遷移
