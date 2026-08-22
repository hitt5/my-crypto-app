# セッション開始

## 🔴 最優先: 開発憲章（Charter）必読 — 強制ルール

開発タスクに着手する前に、`docs/0.charter/` 配下の **9 ファイルを番号順に全件読む**。スキップ・抜粋・要約読み禁止。Charter 未読での実装着手は禁止事項（P8）として扱う（`02-prohibitions.md` 参照）。

| # | ファイル | 内容 |
|---|---------|------|
| 01 | `01-development-charter.md` | 開発の憲法（自動化原則・根本原則・禁止事項・品質基準） |
| 02 | `02-task-graph-driven-development.md` | タスクグラフの所在・読み方・変換ルール |
| 03 | `03-task-graph.md` | タスクグラフのノード型・依存関係・完了条件 |
| 04 | `04-iteration-protocol.md` | A02 → DD01 → DD02 → DD03 → Feature Complete 反復プロトコル |
| 05 | `05-quality-gate.md` | Phase Gate 判定基準 |
| 06 | `06-test-strategy.md` | 8 層テスト戦略 |
| 07 | `07-harness-traceability.md` | ガバナンスハーネス／トレーサビリティ |
| 08 | `08-task-graph-maintenance.md` | タスクグラフ JSON 一元化ルール |
| 09 | `09-knowledge-graph.md` | Knowledge Graph（抽象度横断の知識コンテナ） |

- **番号順厳守**: 01 から順に読む。スキップ禁止
- **セッション継続時も同じ**: コンテキスト圧縮後・新規ターン再開時に Charter を読んでいない場合は最初に読み直す

## 🚀 起動シーケンス

1. **Charter 9 ファイル（01〜09）を番号順に全件読む**（上記参照）
2. **プロジェクトスコープ確認**:
   - MCP bootstrap へ明示 `project_id` を渡し、返却された `project_path` を確認
   - UI の最終選択は Core Runtime preference から復元する（認可根拠にしない）
3. タスクグラフで概況把握（**JSON を全件 read_file しない**）
4. 作業対象の Feature/Task を特定
5. 関連する仕様ファイル（SR / IUC / Context Flow）を read_file
6. `docs/` の確定仕様を参照
7. 未完了タスクを確認:
   ```bash
   find .dodoai/issue -name "*_ready.md" -o -name "*_in-progress.md" 2>/dev/null | sort -r | head -20
   ```

## 📖 用語集（Glossary）

用語の定義に迷ったら、まず用語集を参照すること。

| 用語集 | パス |
|--------|------|
| **プロダクト用語集** | `docs/5.reference/templates/EPIC-template-2.system/GLOSSARY.md` |

## ❌ 禁止

- Charter を読まずにコーディング開始しない
- タスクグラフ JSON を全件 `read_file` しない（必要分だけ取得）
- `_in-progress` タスクを放置して新タスクを開始しない
- 用語の定義を独自に解釈しない（用語集に定義があればそれに従う）
