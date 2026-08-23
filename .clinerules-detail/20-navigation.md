---
type: procedure
title: Navigation — 次に何をやるかの決め方
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, navigation, roadmap, priority]
---

# Navigation — 次に何をやるか

**原則**: 「次何やる？」に対して**勘や記憶で答えてはならない**。Roadmap → Priority Intelligence で機械的に決める。
Priority Intelligence Engine（`F-SDT-PRIORITY`）は実装済みなので、新規開発せず活用する。

## Ops Status が必要な場合だけ

### Step 1 — Ops Status
通常の coding / review / 文書作業では `autoloop.status` を dispatch しない。bootstrap、Session Startup、初回ターンは実行理由にならない。

dispatch できるのは、ユーザーの明示要求、AutoLoop/改善/OODA/CRON/scheduler/soak 自体を扱い現在値が必要な場合、
完了条件が現在の運用状態を明示的に要求する場合、または観測後の状態変化を再確認する場合だけ。実行時は作業メッセージに
1 行明記する。同一 task 内では task state または会話履歴の観測結果を再利用する。

```
Ops Status: autoloop=<verdict>(<loops>) | <roadmap 進捗>
```

目的は AutoLoop 運用を扱う作業での**衝突と重複の回避**であり、通常作業へ一律に課す起動ゲートではない。

### Step 2 — Route 判定
作業対象（Issue / Feature ID / user intent）が見えたら `agn.route_next` を呼ぶ。

| mode | 意味 | 動き |
|---|---|---|
| `standard` | 標準WFに乗っている | `workflow.status` の次アクションに従う |
| `adaptive` | SoT が不足・不整合 | `sdt.search` / `agn_session_startup` / `doc_digest` で SoT を特定・補修してから標準WFへ昇格 |
| `exploratory` | Feature/UC/Module が未安定 | 探索を続ける。**A02/DD の進捗を主張しない** |

制御は advisory（柔軟性を残す）。ただし completion 主張 / HANDOFF `_done` / protected branch push では
route・status・completion gate をスキップしてはならない。

## 「次のタスクは？」と問われた / 迷った時

```
roadmap.derive      → roadmap-graph.json を最新化
priority_cycle      → 優先度キューを再生成
GET /priority/queue → 先頭候補を取得
```

先頭候補の `target_node_id` / `reason` / `priority_score` を**根拠付きで提示**し、承認後に HANDOFF/Issue 化する。
ロードマップとタスクグラフは S/A Phase で必ず生成し、全期間で最新に保つ（Charter §1.3.1 / P9・P20）。

## 改善系・OODA・CRON・scheduler・soak タスクの場合

上記に加えて実施する。

| # | 内容 | Action / 参照先 |
|---|---|---|
| 1 | 6軸成熟度スコア | `autonomy.rate_compute`（F-SELF-IMPROVE-LOOP DD02 後は `selfimprove.evaluate`） |
| 2 | 最新 soak レポート | SDT の operations/soak 配下の**最新 1 件のみ** read_file（全件読み禁止） |

キューの健全性が損なわれている場合は、キューを広げる前に不変条件
（`ready_delta<=0` / `queue_age_p95<=limit` / `duplicate_active_issue_count=0`）を回復させる。
重複 Issue の生成を止めることが先。

## OODA レポート規律（採点・成功確度・較正 — Charter 04 §8）

OODA の周回記録（自動レポート・手動 OODA ログの両方）は **3 必須フィールド**を含むレポートで回す。
どれかを欠く記録はその周回が「観測されなかった」ものとして扱う（WM-4）。
条項正本 = `docs/0.charter/04-autonomous-loop.md` §8、framework 手順 = dodoAI reference repository の `docs/4.operation/13-ooda-scorecard-iteration.md`。project-local Operation / LOOP / metrics catalog が未初期化なら運用開始しない。

| # | 必須フィールド | 要点 |
|---|---|---|
| R-1 | 採点（Scorecard） | 軸別 100 点満点。得点には実測値（コマンド / Action と結果）を必ず添える（Z-05 / P27） |
| R-2 | 成功確度 | Feature / STREAM / 施策ごとに `success_probability`（0.0–1.0）+ 根拠。改善主張は対指標とペア（WM-2） |
| R-3 | 較正 | 前周回の確度と実績を突合し Brier score が縮んでいるかを見る（Z-02）。外れる基準は Skill / 運用方針へ書き戻す |

### μ-cell（新規 STREAM Issue の反復単位）

新規 STREAM Issue は `done_criteria`（実行可能チェック + 期待値）/ `size`（S/M/L）/
`success_probability` + rationale / `max_ticks` を宣言する。
フィールド型の正本 = `docs/99.sdt/agn/0.schema/issue-stream-v1.schema.json`、
テンプレート = `docs/99.sdt/agn/0.schema/issue-handoff-template.md`。
`size: L` は分割してから ready へ。散文のみの完了条件を持つ Issue を新規生成しない。
**μ-cell / status の SoT はタスクグラフノード側**（Charter 01 P29 / 04 §1.1）。Issue front matter・
ファイル名 suffix は投影であり、Issue だけ更新して task node を更新しない書き込みは view drift。

## 禁止事項

- ❌ `autoloop.status` を呼ばずに Autoloop/CRON/scheduler/soak 関連作業を開始する
- ❌ 対象 Issue/Feature が見えているのに `agn.route_next` を呼ばず勘で次アクションを決める
- ❌ `adaptive` / `exploratory` のまま A02/DD 完了を主張する
- ❌ soak / operations MD の全件 read（最新 1 件のみ）
- ❌ CRON レポート MD の新規作成（Charter O9 — `cron_leases` が SoT）
- ❌ 最新 soak レポート未読で「次のOODA」「改善の続き」を開始する
- ❌ 採点・成功確度・較正参照のいずれかを欠く OODA レポート / ログを周回の記録と数える
- ❌ 根拠なき得点・確度を書く / 対指標なしで単独指標の改善を主張する（Z-05 / WM-2）
- ❌ 散文のみの完了条件を持つ STREAM Issue を新規生成する（μ-cell — Charter 04 §8）
- ❌ Issue のファイル名 rename を機械ループの一次 SoT とする経路を新設・拡張する / Issue status を変えて task node を同期しない（P29 — Charter 01 / 04 §1.1）

## Operation / Agent の選定

作業種別・変更対象から Operation を特定し、その Operation が宣言する Agent を機械的に採用する。
Operation 一覧は `process_catalog.list` / SDT の operations 配下を参照する（本文に一覧を複製しない）。
Agent の context pack を初期メモリに注入し、作業開始メッセージに明記する。

```
Operation: <OP-ID> | Agent: <agent-id>
```

❌ Operation を特定せず勘で Agent を選ぶ / Agent 一覧を全件読んで目視選定する / context pack 未取得で着手する
