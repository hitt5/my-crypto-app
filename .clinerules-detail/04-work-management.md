のd# 作業管理

タスクSoT: `.dodoai/issue/`

## HANDOFF命名
- `{YYYYMMDD}_HANDOFF_{status}.md` — status: `_ready` / `_in-progress` / `_done`
- CHILD: `CHILD_{IUC-ID}_{DD-Phase}_{status}.md`
- ステータス変更時はファイルをリネーム

## タスク Issue フォーマット

タスクグラフの dispatch 単位タスク（`uc-task` / `fr-task`）は、STREAM フォーマットで `.dodoai/issue/` に Issue ファイルとして生成すること。

### 必須フィールド

| フィールド | 説明 | 例 |
|-----------|------|-----|
| UC ID | ユースケース ID | UC-001 |
| FR IDs | 機能要件 ID 一覧 | FR-001-01, FR-001-02 |
| Feature | Feature ID | F-FEATURE-NAME |
| EPIC | EPIC ID | EPIC-SEMANTIC-DIGITAL-TWIN |
| Module | モジュールパス | `src/modules/xxx/` |
| DD Phase | DD01 / DD02 / DD03 | DD01 |
| Wave | 依存 Wave 番号 | Wave 0 |
| Status | 📋 Planned / 🔄 In Progress / ✅ Done | 📋 Planned |
| Parent HANDOFF | MASTER HANDOFF パス | `.dodoai/issue/{topic}/MASTER_HANDOFF.md` |
| Task Graph Ref | タスクグラフ JSON 内の task id | `task-graph.json#UC-001-DD01` |
| spec_refs | IUC / SR / FR Catalog パス | 仕様への直リンク |
| gate | 完了条件 | `CONTRACT.md exists + schema validated` |

### 必須セクション

```
## 🎯 目標（1行）
## 📥 入力（spec_refs — このStreamが読むファイル）
## 📤 出力（このStreamが書き込むファイル — Owned Files）
## 🔧 実装ステップ
## ✅ 完了チェックリスト（FR の受入基準から）
## 🚪 Gate 条件
## 🔗 次のStreamへの引き継ぎ情報
```

### ❌ 禁止

- ❌ UC/FR 参照のない自由形式 Issue（トレーサビリティ断絶）
- ❌ spec_refs のない Issue（仕様との紐付け断絶）
- ❌ Gate 条件のない Issue（完了判定不能）

## 未完了タスク確認
```bash
find .dodoai/issue -name "*_ready.md" -o -name "*_in-progress.md" 2>/dev/null | sort -r | head -20
```
優先: `_in-progress`（前回の続き）> `_ready`（未着手）> `_done`（スキップ）

## アーカイブ
完了済みissue → `_done Issue を .dodoai/issue/_history/ へ移動（手動 or Custom Action）`
判定: `_done.md` あり + `_ready/_in-progress` なし → `.dodoai/issue/_history/` へ移動
