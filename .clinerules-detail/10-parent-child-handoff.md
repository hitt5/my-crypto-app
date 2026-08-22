？# 親子Handoff（Parent-Child Handoff）ルール

> **「親子Handoffつくって」と言われたら、このルールに従うこと。**

---

## 🎯 トリガーワード

- 「親子Handoffつくって」「親子Handoff作って」
- 「並列Handoff」「マスターHandoff」
- 「ストリーム分割」

---

## 📖 親子Handoffとは

**親子Handoff** = **1つの親HANDOFF（MASTER）** と **複数の子HANDOFF（STREAM）** を作成し、並列開発を可能にするパターン。

---

## 📁 ファイル構造

```
.dodoai/issue/{topic}/
├── MASTER_HANDOFF.md                  ← 親HANDOFF（全体俯瞰・依存関係・Done Criteria）
├── {YYYYMMDD}_STREAM_A_{name}_{status}.md  ← 子HANDOFF（Wave内の独立タスク）
├── {YYYYMMDD}_STREAM_B_{name}_{status}.md
└── ...
```

> ステータスサフィックス: `_ready` / `_in-progress` / `_done`

---

## 🔧 親HANDOFF（MASTER）の必須セクション

```markdown
# {EPIC Phase} MASTER HANDOFF

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Created | YYYY/MM/DD HH:MM JST |
| Status | 進行中 |
| EPIC | {EPIC-ID} |
| DD Phase | DD01 / DD02 / DD03 |
| Task Graph Path | `docs/99.sdt/agn/1.workflows/{epic}/...` |

## 🎯 ゴール（Done Criteria）

## 📋 子HANDOFF（STREAM）一覧

| Stream | UC ID | FR IDs | 子HANDOFF | Wave | 依存 | Status |
|--------|-------|--------|-----------|------|------|--------|

## 🔗 依存関係グラフ（Wave構造）

## 📊 OVERLAP CHECK

## 📚 参照ドキュメント

## 🏁 結論
```

---

## 🔧 子HANDOFF（STREAM）の必須セクション

```markdown
# STREAM-{ID}: {タイトル}

| Key | Value |
| --- | --- |
| Parent HANDOFF | {親HANDOFFのパス} |
| UC ID | {UC-ID} |
| FR IDs | {FR-ID-01}, {FR-ID-02} |
| Module | {module path} |
| DD Phase | DD01 / DD02 / DD03 |
| Wave | {Wave N} |
| spec_refs | IUC: `path`, SR: `path`, FR: `path` |
| gate | {Gate 条件} |

## DD Phase Progress

| Phase | Status | Evidence |
|-------|--------|----------|
| DD01 | 🔴 未着手 | — |
| DD02 | 🔴 未着手 | — |
| DD03 | 🔴 未着手 | — |

## 🎯 目標（1行）
## 📥 入力（spec_refs — このStreamが読むファイル）
## 📤 出力（このStreamが書き込むファイル — Owned Files）
## 🔧 実装ステップ
## ✅ 完了チェックリスト
## 🚪 Gate 条件
## 🔗 次のStreamへの引き継ぎ情報
```

---

## 📐 作成ルール

### 1. 分割粒度（Charter P7 準拠）

> **❌ Feature / IUC 単位での dispatch は禁止（Charter P7）**
> **dispatch 単位は UC / FR のみ**

### 2. OVERLAP CHECK 必須

**書き込み対象ファイルの重複がゼロ**であることを確認する。

### 3. 各子HANDOFFは単独実行可能

- 「親HANDOFFを読まないと分からない」状態にしない
- コピペ実行可能なコマンドを含める

### 4. Wave 依存はMASTER HANDOFFで管理

Wave 構造はタスクグラフ JSON の `depends_on` から導出する。

---

## ❌ やってはいけないこと

- ❌ OVERLAP CHECKなしで子HANDOFFを作成する
- ❌ 子HANDOFFの出力ファイルが別 Stream と重複する
- ❌ 親HANDOFFなしで子HANDOFFだけ作る
- ❌ Feature / IUC 単位で dispatch する（Charter P7 違反）
- ❌ spec_refs / gate のない STREAM
- ❌ Evidence なしの完了宣言（Charter P3 / P4 違反）
