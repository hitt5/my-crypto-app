# 開発タスク事前コンテキスト必須ロード（Dev Task Preload Gate）

> **このルールは開発コード変更の前提条件であり、スキップ不可。**
> 「続けて」「実装して」「DD02やって」等の口語フレーズでも省略禁止。

---

## 🚨 HARD GATE: コード変更前に必ず以下を完了せよ

Agent がソースコードを **新規作成 or 編集** する前に、以下のステップを **必ず** 実行し、**Preload Evidence Block** をユーザーに出力すること。

### ❌ PROHIBITED
- Preload Evidence Block を出力せずにコード変更を開始すること
- HANDOFF だけ読んで spec_refs / UC Catalog / FR Catalog を読まずにコーディング開始
- 「前回の続き」を理由に Issue → TaskGraph → Spec 接続をスキップすること

---

## 📋 Preload プロトコル

### Step 0: タスクグラフ存在ゲート（P9 — HARD GATE）

対象 Feature / UC のタスクグラフ JSON が存在することを確認する。

```
find docs/99.sdt/agn/1.workflows/ -path "*/{feature-id}/*" -name "task-dd*.json" 2>/dev/null
```

- **存在する** → Step 1 へ
- **存在しない** → `03-iteration-protocol.md` §タスクグラフ存在ゲートの作成フロー実行後、Step 1 へ

### Step 1: Issue 特定

```
find .dodoai/issue -name "*_in-progress.md" -o -name "*_ready.md" | sort -r | head -5
```
→ 対象 HANDOFF ファイルを `read_file`

### Step 2: TaskGraph 接続

HANDOFF の「参照ドキュメント」セクションからタスクグラフ JSON パスを取得。

### Step 3: Spec Files 読み込み

Step 2 で取得した spec_files を **全て `read_file`**:

| ファイル種別 | 例 |
|------------|---|
| System Requirements | `docs/.../system-requirements.md` |
| IUC 定義 | `docs/.../iuc.md` |
| Context Flow | `docs/.../context-flow.md` |

### Step 4: UC Catalog / FR Catalog 参照

対象モジュールの UC Catalog / FR Catalog を読む:

```
docs/99.sdt/art/context/{deploy-unit}/usecase/usecase-catalog.md
docs/99.sdt/art/context/{deploy-unit}/external-design/fr-catalog.md
```

### Step 5: Preload Evidence Block 出力

```markdown
## 🔒 Dev Task Preload Evidence

| # | Item | Status | Path / Value |
|---|------|--------|-------------|
| 1 | Issue HANDOFF | ✅ | `.dodoai/issue/{dir}/{file}` |
| 2 | Task Graph | ✅ | `docs/99.sdt/agn/...` |
| 3 | Spec: SR | ✅ | `docs/.../{sr-path}` |
| 4 | Spec: IUC | ✅ | `docs/.../{iuc-path}` |
| 5 | Spec: Context Flow | ✅/⬜ | `docs/.../{cf-path}` or N/A |
| 6 | UC Catalog | ✅ | `docs/99.sdt/art/context/...` |
| 7 | FR Catalog | ✅/⬜ | `docs/99.sdt/art/context/...` or N/A |

**Target UC**: UC-001, UC-002
**DD Phase**: DD02
```

→ この Block が出力されて初めてコード変更を開始してよい。

---

## 🔄 「続けて」への対応

1. 前回の HANDOFF (_in-progress) を探す
2. TaskGraph から spec_files を取得
3. spec_files を read_file（前回読んでいても毎回読み直す）
4. Preload Evidence Block を出力
5. ← ここで初めてコーディング着手

> 「前回読んだから省略」は禁止。セッションをまたぐとコンテキスト窓がリセットされるため。

---

## 📦 適用スコープ

| 対象 | 適用 |
|------|------|
| DD01 (CONTRACT.md 作成) | ✅ 必須 |
| DD02 (実装) | ✅ 必須 |
| DD03 (異常系) | ✅ 必須 |
| バグ修正 | ✅ 必須 |
| ドキュメントのみ変更 | ⬜ 不要 |
| ClineRule / AGENTS.md 編集 | ⬜ 不要 |
| テストのみ追加 | ✅ 必須 |
