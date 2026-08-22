# my-crypto-app — ドキュメント構成・手順書

> **プロジェクト**: my-crypto-app
> **フレームワーク**: ADF (Agentic Development Framework)
> **更新日**: {YYYY/MM/DD}

---

## このdocs/の構成

```text
docs/
  README.md                 ← 本ドキュメント（手順書・索引）
  FOLDER_ARCHITECTURE.md    ← フォルダアーキテクチャ定義
  0.charter/                ← 開発憲章（憲法）
  1.concept/                ← コンセプト（課題・なぜdodoAI・アプローチ）
  2.manual/                 ← マニュアル（準備・構造化の実施手順）
  3.output/                 ← アウトプット索引（正本は 99.sdt/art/）
  4.evaluation/             ← 評価（到達度・ドリフト統治）
  5.reference/              ← 参考資料（受領資料・テンプレート）
  98.dodoai-custom-spec/    ← dodoAI Custom UI / Action の A02 仕様正本
  99.sdt/                   ← SDT（Semantic Digital Twin）= AGN + ART
```

---

## 全体フロー（Delivery Asset 共通フレーム）

```text
Phase 0  Concept       → 1.concept/       課題認識・アプローチ定義
Phase 1  Preparation   → 2.manual/00.preparation/   MCP 接続・入力資産の準備
Phase 2  Structuring   → 2.manual/01.structuring/   構造化＝SDT 投影の実施
Phase 3  SDT ART       → docs/99.sdt/art/           成果物の構造化出力（3.output/ は索引）
Phase 4  Evaluation    → 4.evaluation/              到達度評価・ドリフト統治
```

---

## 主要ドキュメント索引

| # | ドキュメント | 内容 | 状態 |
|---|------------|------|------|
| 0 | [0.charter/01-development-charter.md](0.charter/01-development-charter.md) | 開発憲章（憲法） | 📋 |
| 1 | [1.concept/00-overview.md](1.concept/00-overview.md) | コンセプト概要 | 📋 |
| 2 | [2.manual/00-overview.md](2.manual/00-overview.md) | 実施手順の概要 | 📋 |
| 3 | [3.output/00-overview.md](3.output/00-overview.md) | 成果物索引 | 📋 |
| 4 | [4.evaluation/00-overview.md](4.evaluation/00-overview.md) | 評価・ドリフト統治 | 📋 |
| 5 | [5.reference/README.md](5.reference/README.md) | 参考資料の置き場ルール | 📋 |
| 98 | [98.dodoai-custom-spec/00-overview.md](98.dodoai-custom-spec/00-overview.md) | Custom UI / Action 仕様正本 | 📋 |
| 99 | [99.sdt/README.md](99.sdt/README.md) | SDT（AGN + ART）構成 | 📋 |

> 状態: 📋 計画中 / 🔄 進行中 / ✅ 完了 — プロジェクト開始後に更新すること。

---

## 開発手順

### 0. セッション開始

Agent（Cline / Claude Code / Codex）は最初に MCP `dodo_project_bootstrap` を呼び、
`.clinerules/00-CORE.md` と `docs/0.charter/01-development-charter.md` を読む。

### 1. コンセプト定義 → 実施

→ [1.concept/00-overview.md](1.concept/00-overview.md) から始め、[2.manual/00-overview.md](2.manual/00-overview.md) の手順に従う。

### 2. 成果物の確認

→ 成果物の正本は `docs/99.sdt/art/`。索引は [3.output/00-overview.md](3.output/00-overview.md)。

### 4. 評価

→ [4.evaluation/00-overview.md](4.evaluation/00-overview.md) を参照。

---

## 関連ドキュメント（外部）

| ドキュメント | 場所 |
|------------|------|
| dodoAI Core（Control Plane） | MCP `dodo_project_index` で解決 |
| Issue / HANDOFF | `.dodoai/issue/` |
| Custom Action 実装 | `.dodoai/custom_actions/` |
| Custom UI 実装 | `.dodoai/custom_ui/` |
