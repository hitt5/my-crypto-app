# 2.manual — マニュアル（準備と構造化の実施手順）

> [1.concept](../1.concept/00-overview.md)、とくに [03-approach.md](../1.concept/03-approach.md) の考え方を実作業手順に落とす。
> 本テーマは dodoAI Delivery Asset の共通フレーム **Concept → Preparation → Structuring → SDT ART → Evaluation** に従う。
> 本 `2.manual` は中央2フェーズ **Preparation（準備）** と **Structuring（構造化＝SDT 投影）** を担う。

---

## Delivery Asset 共通フレームでの位置づけ

| フェーズ | Delivery Asset | 本テーマでの担当 | 場所 |
|---|---|---|---|
| Phase 0 | Concept | 課題認識・なぜ dodoAI か・アプローチ | [`../1.concept/`](../1.concept/00-overview.md) |
| Phase 1 | **Preparation** | MCP setup・入力資産の準備 | [`00.preparation/`](00.preparation/) |
| Phase 2 | **Structuring** | 構造化＝SDT 投影の実施 | [`01.structuring/`](01.structuring/) |
| Phase 3 | SDT ART | 成果物の構造化出力 | `docs/99.sdt/art/` |
| Phase 4 | Evaluation | 到達度評価・統治 | [`../4.evaluation/`](../4.evaluation/00-overview.md) |

---

## フォルダ構成

| フェーズ | フォルダ | 役割 |
|---|---|---|
| Preparation | [00.preparation/](00.preparation/) | MCP 接続確認・入力資産（受領資料・コード・CallGraph）の準備 |
| Structuring | [01.structuring/](01.structuring/) | 構造化手順の実施・SDT/ART への投影 |

---

## 00. Preparation（準備）

| # | ファイル | 内容 |
|---|---|---|
| 01 | [00.preparation/01-mcp-setup.md](00.preparation/01-mcp-setup.md) | セッション開始プロトコル（bootstrap → action_list → agent）と MCP 接続確認 |
| — | [00.preparation/mcp-actions.md](00.preparation/mcp-actions.md) | 本テーマで使う MCP / Action の一覧 |

このフェーズの出力: {準備フェーズの成果物を記載する（例: CallGraph 抽出結果、入力資産の Md 化）}。
ここではまだ成果物の生成（Structuring 本体）はしない。

---

## 01. Structuring（構造化＝SDT 投影）

| # | ファイル | 内容 |
|---|---|---|
| 01 | [01.structuring/01-procedure.md](01.structuring/01-procedure.md) | 構造化の全手順（Step 分解・使用 Action・合格条件） |

このフェーズの出力: `docs/99.sdt/art/` 配下の構造化成果物（JSON 正本 + 人間可読 Markdown）。

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | {YYYY/MM/DD} | 初版作成 |
