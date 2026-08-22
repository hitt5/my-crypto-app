---
type: procedure
title: Completion Gate — 完了主張前の実査
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, hard-gate, completion, evidence]
---

# Completion Gate（HARD GATE）

**適用タイミング**: `attempt_completion` / DD Phase 完了 / Feature・UC close / HANDOFF を `_done` へ改名する前。
**根拠**: Charter P3（テスト失敗での完了報告禁止）/ P20（status 未同期での完了報告禁止）。条文の正本は Charter。

## Check 0 — Completion Operation Hook Gate

自然言語の指示・Skill・Operation Listの存在だけでは完了時の残作業を強制できない。Codex / Claude Codeの
`Stop` と dodo Coderの `attempt_completion` は共通 `sovereign.hook_gate` を通し、session worksetと
`operations.json.attributes.completion_gate`を照合する。該当時は返されたOperationのAgent/Skillを
同一turnで遂行する。CRONは使わない。

High/critical Operationはcurrent explicit intentまたは`standing-scoped` authorization内だけ実行する。
同一plan fingerprintは一度だけ差し戻し、同じMCP引数を反復しない。遂行不能なら一つの具体的blockerを
報告し、未実施を完了と呼ばない。

## Test Definition Gate

テスト層・旧 L 番号 alias・Mock 境界・DD01〜DD05 の配置は、SDT
`docs/99.sdt/art/contracts/F-SDT-TEST-EVIDENCE/adf-test-definition.json` と同 MD view から解決する。
意味の根拠は同 JSON の `authorities.taxonomy_and_phase` が指す ADF、数値閾値は Charter
`docs/0.charter/01-development-charter.md` §3。Feature の主 `deploy_unit` だけを根拠に必要層を N/A にせず、
実際に変更した全 deploy unit の profile を合成する。

## 前提 — status は完了の証拠ではない

以下はすべて**ナビゲーション・登録・回帰の証拠**であり、仕様適合の証明ではない。

`workflow.status` / `agn.route_next` / Issue・TaskGraph の `_done` / 既存 Evidence /
green gate / テスト PASS / coverage 達成

**「既に `_done` だから完了」と報告してはならない。** ユーザーが「実装して」「直して」と言った場合、
既存 status を根拠に検証のみで返答することは禁止。未実装なら実装するか、具体的な blocker を報告する。

## Check 1 — 仕様適合の実査（最重要）

現在の checkout に対して conformance matrix を作る。

1. 対象 Feature の `system-requirements.md` / `uc.md` / `capability-module.md` / `CONTRACT.md` を読む
2. 全 SR/FR/UC を列挙し、各行を**具体的な実装パス + acceptance test** に対応付ける
3. 各行を `PASS` / `PARTIAL` / `FAIL` / `NOT IMPLEMENTED` で判定する。**status metadata から PASS を推定しない**
4. 範囲内に PASS 以外が 1 件でもあれば **完了禁止**

判定時の注意:

- 「1 Action で結果が返る」「自動合成する」系の要求は、caller が前処理済みデータを注入する単体テストでは PASS にしない。
  live で要求どおりの最小入力で dispatch し、composition root から自動配線されることを確認する。手動持込みが必要なら `PARTIAL`
- 数値 NFR は現行 runtime で**実測**する。一般回帰テストの PASS で acceptance test の欠落を代替しない
- 変更系は declared データ非破壊 / dry-run と apply / 冪等性 / rollback・audit envelope / 全 SoT 書込先を個別に検証する

## Check 2 — アーキテクチャ適合

DD01 Scaffold の計画上の責務・選択 Template と実ツリー/import を比較する（`arch.scaffold_verify` /
`arch.layer_check` / `arch.module_boundary`）。
facade のはずの router/action に業務ロジックや SoT 書込が埋まっていれば不合格。

## Check 3 — Evidence と登録

| 検査 | Action |
|---|---|
| governance 登録（A02 時点で行う。A03 は SDT/AGN Conformance Gate） | `sdt.governance_metrics` |
| テスト Evidence の欠落・リンク切れ | `test_evidence.audit` → `gaps=0` / `broken_links=0` |
| **SDT 書き込み主権（Charter P24）** | `sdt.authoring_validate` → `error_count=0` |

SDT を書き換えた作業では `sdt.authoring_validate` を実行する。生成物の手編集（AUTH-V05）や
主権宣言の矛盾（AUTH-V04）が残ったまま「完了」と言わない。詳細は `40-domain-gates.md` §2。

## Check 4 — status 同期（P20）

`roadmap.sync_gate`（payload: `workspace_root` / `feature_id`）を実行し
`ok=true`・`stale_task_status=0`・`missing_milestone=0`・`roadmap_drift=0` を確認する。

A02 で AGN 登録した場合は同一作業内で `roadmap.derive` 等により roadmap milestone を反映し、
`task-dd*.json` の status・`feature.json` の dd_progress・roadmap milestone を揃える。
**この同期結果は DD05 のテスト証明を代替しない。**

**status の書き込み向き（P29）**: タスク状態の一次 SoT はタスクグラフノード。HANDOFF/Issue を
`_done` へ rename する時は、**先に（または同一作業内で）対応する task node の status / Evidence ref を
更新**し、Issue rename は投影として行う。Issue だけ rename して task node が stale なら P20 で FAIL する
（条文 = Charter 01 P29 / 手順 = Charter 04 §1.1）。

## Check 5 — 非 PASS の扱い

今回スコープ外へ延期する場合も、**判定を PASS に書き換えてはならない**。

- 各 gap を具体的な `_ready` Issue/STREAM と Task Graph 依存へ接続する
- Feature Complete は pending のままにする
- 既存 Feature/Issue が同じ責務を持つならそこへ集約し、**重複 Issue を起票しない**

## Check 6 — 意味保存の実査（World Model WM-2 / P26）

**適用**: 「整理した」「削減した」「統合した」「重複を排除した」「軽くした」と報告する時。

エントロピー $H$（複雑さ・不確実性）の低下だけを根拠に改善を主張してはならない。
**$H$ だけを目標にすると、最も安価な最小化は「意味を削ること」である。** 仕様を消せば
$H_{semantic}$ が下がり、Evidence を消せば $H_{governance}$ が下がる。指標上は改善に見えて
実際は破壊であり、この構造的欠陥を塞ぐのが本 Check の目的（Goodhart 対策）。

削減側と保存側を**対で**示す。

| 側 | 示すもの |
|---|---|
| 削減（$H$） | 何をどれだけ減らしたか（重複統合数 / 曖昧語の正規化 / 循環除去 / 未解決 Hypothesis の決着） |
| 保存（$Meaning$） | 意思決定に必要な情報が失われていないこと（SR/UC/FR の対応が維持 / trace 健全 / Evidence 不変 / テスト PASS） |

保存側の観測に使える既存 Action:

| 観測 | Action |
|---|---|
| trace・参照の健全性 | `sdt.ln_link_integrity` / `test_evidence.audit` |
| 語彙・概念の整合 | `sdt.ontology_validate` |
| governance 登録の維持 | `sdt.governance_metrics` |
| 監査証跡の不変性（削除していないこと） | `sdt.authoring_validate` |

❌ 件数・行数・ファイル数の減少をそのまま「改善」と報告する / 仕様・Evidence・trace を削って
数値を良くする / 欠測（測れなかった）を実測 0（測って 0 だった）として記録する

> 本 Check は **advisory**（$H$ と $Meaning$ の同時計測器が揃うまで）。
> 条文と段階導入の正本は Charter `docs/0.charter/01-development-charter.md`。

## Evidence Block


```md
## Completion Gate Evidence
| Check | 結果 | 実測値 |
|---|---|---|
| 0 Completion Operation | PASS/BLOCKED/N/A | plan fingerprint / Operation ID / Agent / Skill |
| 1 仕様適合 conformance matrix | PASS/BLOCKED | SR/FR/UC <n> 行 — PASS <n> / PARTIAL <n> / FAIL <n> |
| 2 アーキ適合 | | `arch.layer_check` / `arch.module_boundary` |
| 3 Evidence | | `test_evidence.audit` gaps=<n> broken_links=<n> |
| 4 status 同期 | | `roadmap.sync_gate` ok=<bool> stale=<n> drift=<n> |
| 5 テスト | | <n> passed / coverage <n>% |
```

## Custom UI Completion Gate

Custom UI manifest / block / catalog の変更は、通常の Completion Gate に加えて次を満たす。

- `custom_ui.design_guide`: `ok=true`、registry/catalog 件数一致、全 entry の `propsSchema.properties` が非空。
- `custom_ui.manifest_lint`: 変更対象 path を `mode="strict"` で実行し `error_count=0`。応答は最大 20 manifest / 200 findings。
- 既存全 manifest の `mode="compatibility"` 結果を別に記録し、warning があれば conformance を `PARTIAL` のままにする。
- CSS hard-coded color / inline style はこの lint の PASS に含めない。別の測定済み STREAM が未完なら完了へ格上げしない。

## DD04 / DD05（Feature 単位）

`feature.json` の `attributes.deployment_validation` を読んで分岐する。

| 値 | 必要な検証 |
|---|---|
| `local-only` | Track A のみ（ST-E2E-HL/HD + ST-AI-Visual + ST-Human） |
| `required` | Track A + **Track B**（サーバー面へ deploy → `/ready` → server smoke → **デプロイ先実 URL** へのブラウザ E2E → サーバー実行ログ/lease/soak 確認 → `evidence-dd05.json`） |

localhost への E2E は**サーバー検証ではない**。認証情報・エンドポイントは `env://` 論理参照のみ（P5）。
DD05 FAIL は done にせず、Task Graph の依存と Finding に戻して Roadmap/Priority を再評価する。
