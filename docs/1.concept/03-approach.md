# 03 — アプローチ（Approach）

> [01-problem.md](01-problem.md) の課題を、[02-why-dodoai.md](02-why-dodoai.md) の能力でどう解くか。
> ここで定義したアプローチを [../2.manual/](../2.manual/00-overview.md) が実作業手順に落とす。

---

## 全体フロー

```text
Phase 0  Concept       → 1.concept/                  ← 今ここ
Phase 1  Preparation   → 2.manual/00.preparation/    入力資産の準備・MCP 接続
Phase 2  Structuring   → 2.manual/01.structuring/    構造化＝SDT 投影
Phase 3  SDT ART       → docs/99.sdt/art/            成果物の構造化出力
Phase 4  Evaluation    → 4.evaluation/               到達度評価・統治
```

## 中核原則

> {このテーマの作業原則を記載する。例:
> ・コードに根拠が無いものは創作しない（確度マーカー 🟢確定 / 🟡推定 / 🔴未確認 で分離する）
> ・成果物の正本は `docs/99.sdt/art/` に置き、Markdown は人間可読ビューとする
> ・要件モデルは BR → SR → UC ＋ CAP ─owns→ FR ─realized_by→ MOD の縦糸×横糸で通す}

## ステップ分解

| Step | 内容 | 入力 | 出力 | 確度 |
|------|------|------|------|------|
| ① | {ステップ1} | {入力} | {出力} | 🟢 |
| ② | {ステップ2} | {入力} | {出力} | 🟢🟡 |
| ③ | {ステップ3} | {入力} | {出力} | 🟡 |

## 入力資産（Evidence Sources）

| ソース | 実体 | 使い方 | 確度 |
|--------|------|--------|------|
| コード | {リポジトリパス} | CallGraph 抽出の SoT | 🟢 |
| 受領資料 | `docs/5.reference/` | {使い方} | 🟡 |
| {その他} | {パス} | {使い方} | {🟢🟡🔴} |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | {YYYY/MM/DD} | 初版作成 |
