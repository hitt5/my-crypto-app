# 5.reference — 参考資料

> 受領資料・外部資料・ドキュメントテンプレートの置き場。**読み取り専用**（ここを SoT として開発しない）。

---

## 構成

```text
5.reference/
  README.md          ← このファイル
  templates/         ← BR / SR / EPIC 等のドキュメントテンプレート
  {received-docs}/   ← 顧客・他チームからの受領資料（プロジェクト開始後に追加）
```

## 置き場ルール

| 種別 | 置き方 |
|------|--------|
| 受領資料（原本） | `5.reference/{受領元}-{内容}/` にそのまま保存。改変しない |
| 受領資料（Md 化） | 原本と同じフォルダに `converted/` を作り Markdown 化を置く |
| 外部フレームワーク資料 | リンク集として本 README に追記（コピーは最小限） |
| テンプレート | `templates/` 配下（BR/SR/EPIC の雛形） |

## 禁止事項

- ❌ 参考資料を SoT として実装根拠にすること（SoT は `docs/1.concept/`〜`4.evaluation/` と `docs/99.sdt/`）
- ❌ 顧客名・実ドメイン・実キー等の実値を参照資料からテスト/fixture へコピーすること（Charter P5）

## テンプレート一覧

| テンプレート | パス |
|------------|------|
| プロダクト BR | `templates/1.business-requirements/` |
| プロダクト SR | `templates/2.system-requirements/` |
| EPIC 仕様一式 | `templates/EPIC-template-2.system/` |
