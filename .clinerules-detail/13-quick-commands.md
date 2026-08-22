# クイックコマンド インストラクション集

Agent が口語フレーズを受けたとき、以下のマッピングに従って自律実行する。

---

## 📋 Issue 管理系

### 「次やるIssueを対応して」「次のタスクやって」

```
1. _in-progress を優先チェック
   find .dodoai/issue -name "*_in-progress.md" 2>/dev/null | sort -r | head -5

2. _in-progress がある → 再開（O5: 放置禁止）

3. _in-progress がない → _ready を探す
   find .dodoai/issue -name "*_ready.md" 2>/dev/null | sort -r | head -10

4. 選択した HANDOFF を read_file

5. 🚨 タスクグラフ存在ゲート（P9）確認

6. ファイルを _in-progress にリネーム

7. Dev Task Preload Gate（14-dev-task-preload.md）実行

8. HANDOFF の実装ステップに従い実装開始
```

### 「Issueの状況を見せて」

```bash
find .dodoai/issue -name "*_in-progress.md" 2>/dev/null | sort -r
find .dodoai/issue -name "*_ready.md" 2>/dev/null | sort -r
```

### 「このIssueを完了にして」

```
1. _in-progress.md を _done.md にリネーム
2. HANDOFF に "## ✅ 完了サマリー" セクションを追記
3. 対応する task-dd*.json の status を "done" に更新
```

### 「Issueをアーカイブして」

```bash
_done Issue を .dodoai/issue/_history/ へ移動（手動 or Custom Action）
```

---

## 🧠 タスクグラフ系

### 「タスクグラフ登録して」

```
登録先: docs/99.sdt/agn/1.workflows/{epic}/features/{feature-id}/
命名規則:
  - Feature: feature.json
  - Task: task-dd01.json / task-dd02.json / task-dd03.json
```

**feature.json 最小スキーマ:**
```json
{
  "id": "F-XXX-YYY",
  "name": "Feature 名称",
  "epic": "EPIC_XX",
  "status": "draft|ready|running|done",
  "spec_refs": {
    "sr": "docs/.../system-requirements.md",
    "iuc": "docs/.../iuc.md"
  }
}
```

**task-dd*.json 最小スキーマ:**
```json
{
  "id": "F-XXX-YYY-DD01",
  "feature": "F-XXX-YYY",
  "type": "fr-task",
  "status": "draft|ready|running|done",
  "gate": "CONTRACT.md exists + schema validated",
  "depends_on": [],
  "spec_refs": ["UC-XXX", "FR-XXX-01"]
}
```

### 「Taskをreadyにして」

task-dd*.json の `.status` を `"ready"` に更新。前提: depends_on がすべて `"done"`。

### 「Taskをdoneにして」

task-dd*.json の `.status` を `"done"` に更新。前提: gate 条件が満たされている。

---

## 🔄 開発フロー系

### 「DD01を始めて」「CONTRACT.mdを作って」

```
0. 🚨 タスクグラフ存在ゲート（P9）
1. spec_refs から SR / IUC を取得
2. CONTRACT.md を作成（型定義・インターフェース宣言のみ）
3. Test Skeleton を作成
4. task-dd01.json の status を "done" に更新
```

### 「DD02を始めて」「実装を始めて」

```
前提: DD01 完了（CONTRACT.md + Test Skeleton 存在確認）
→ 全テストが通るまで実装
→ L5 PASS なしで完了宣言 ❌
```

### 「テストを走らせて」

```bash
# Backend
{your-test-command}

# Frontend
{your-test-command}
```

---

## 🚀 環境系

### 「サービスを起動して」

```bash
{プロジェクトの起動コマンド}
```

### 「ヘルスを確認して」

```bash
curl -s http://localhost:8000/health && echo " ✅ OK" || echo " ❌ DOWN"
```

---

## 🔖 クイックリファレンス（全コマンド早見表）

| 口語コマンド | 実行内容 |
|------------|---------|
| 「次やるIssueを対応して」 | `_in-progress` → `_ready` の順にピック → HANDOFF読む → 実装 |
| 「Issueの状況を見せて」 | `find .dodoai/issue` + タスクグラフ確認 |
| 「このIssueを完了にして」 | `_done.md` リネーム + task status done |
| 「Issueをアーカイブして」 | `_done Issue を .dodoai/issue/_history/ へ移動（手動 or Custom Action）` |
| 「タスクグラフ登録して」 | feature.json / task-dd*.json 追加 |
| 「Taskをreadyにして」 | task-dd*.json `.status = "ready"` |
| 「Taskをdoneにして」 | task-dd*.json `.status = "done"` |
| 「DD01を始めて」 | CONTRACT.md 作成フロー |
| 「DD02を始めて」 | 実装フロー |
| 「テストを走らせて」 | テスト実行 |
| 「サービスを起動して」 | `{プロジェクトの起動コマンド}` |
| 「ヘルスを確認して」 | curl 各サービス `/health` |
