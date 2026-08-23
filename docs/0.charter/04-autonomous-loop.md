---
type: charter
title: 自律開発ループの運用
description: Harness Loop・優先度決定・Evidence 書き戻し・二面分担の手順正本
tags: [charter, harness, autonomous, evidence, two-plane]
timestamp: 2026-08-01T14:00:00Z
---

# 自律開発ループの運用

| Key | Value |
| --- | --- |
| Version | 1.4.0 |
| Updated | 2026/08/22 |
| Status | Approved |
| 種別 | **手順の正本**（条項は定義しない → 01 が正本） |

## 0. ループが閉じるとは何か

自律開発は「Agent が勝手にコードを書くこと」ではない。**次の 1 周が前の周より賢くなること**である。

```
       ┌────────────────────────────────────────────┐
       │                                            │
   SDT ──→ 優先度 ──→ dispatch ──→ 実行 ──→ Evidence ─┘
  (状態)   (意思決定)              (介入)    (観測)
```

この輪が閉じる条件は 1 つだけである。

> **実行結果が SDT の状態へ戻ること。** 戻らない実行は、次の意思決定を 1mm も改善しない。
> それは「作業をした」だけであって「学習した」ではない（WM-4）。

### 0.1 閉ループは WF として定式化する

閉ループ（観測が次の判断へ戻るループ）の正準構造は **「閉ループ = WF、1 周 = DAG インスタンス、
SDT = 状態空間」の 3 層分離**である。ADF（A02 → A03 → DD01–05 → Evidence → 優先度再導出）
自体が閉ループ WF の第一の適用対象であり、新設・改修する閉ループはこの形で定式化する。
グラフ自体への巡回エッジ・Decide（HIL）/ Improve（基準改訂）の WF ノード化は禁止する。
命題の正本 = concept `08-agentic-ooda-operations.md` §4.2（本章は手順への接続のみ）。

---

## 1. Harness Loop

全 Agent 実行は Harness を通る（P1）。Harness は 6 段の固定ループである。

| # | 段 | 内容 | 失敗時 |
| --- | --- | --- | --- |
| 1 | **Select** | 何をやるか決める（§2） | 候補なし → キュー健全性を先に直す |
| 2 | **Plan** | 実行計画へ分解する（タスクグラフが入力） | グラフ不在なら作る（P9） |
| 3 | **Dispatch** | Runtime へ渡す（Runtime 選定 = 03） | 可用性なしなら別 Runtime か保留 |
| 4 | **Observe** | 実行結果を観測する | 観測できない実行は成果と数えない |
| 5 | **Verify** | ゲートで検証する（= 06） | FAIL は done にせず Finding へ |
| 6 | **Close** | status と Evidence を同期して閉じる | 同期前に「完了」と言わない（P20） |

**Dispatch と Observe は必ず対にする**（WM-4）。定期実行（CRON / Scheduler）もこのループの
入口であって別経路ではない（P6 原則）。

### 1.1 ループの SoT はタスクグラフノードである（P29）

Harness Loop の 6 段が読み書きする**一次状態はタスクグラフノード（`task-dd*.json` / `feature.json`）**である。
Issue（`.dodoai/issue/`）は**人間可読 view + HIL 承認 + dispatch envelope** であり、機械ループの SoT ではない。

| 段 | SoT（正） | Issue の役割 |
| --- | --- | --- |
| Select | task node の status = `ready` + 優先度キュー | 人間への候補提示 |
| Claim（実行権） | lease key = task node ID（共有ストアの一意制約） | 着手中の可視化 |
| status 遷移 | task node の `ready → in-progress → done`（+ Evidence ref） | ファイル名 suffix は**投影の副作用** |
| Close | クローズ Gate → task node status + Evidence 同期（P20 / P22） | `_done` 改名は投影 |

Issue のファイル名 rename（`_ready` → `_in-progress` → `_done`）を一次 SoT とする経路を
**新設・拡張してはならない**（条文 = 01 P29）。既存の Issue ファイル駆動経路（cron dispatch の
`_ready.md` glob 選定・ファイル名 stem 由来 lease 等）は、①task node への併走記録 →
②view drift 0 の Evidence 複数周 → ③Select/lease の task node 切替 → ④rename の view 化、の
段階移行で縮退させる。project-local の機械 enforcement が未初期化なら ADVISORY のまま blocker を記録し、dodoAI upstream の Feature 状態を local 完了証拠にしない。
移行完了後、`roadmap.sync_gate` は「二重 SoT の突合」から「投影の鮮度検査」へ役割が縮退する。

---

## 2. 次に何をやるか — 勘で決めない

「次は何をやる？」に対する答えは、**口頭の思いつきではなく実装済みの意思決定系**が出す。

| # | 段 | 内容 |
| --- | --- | --- |
| ① | `roadmap.derive` | Feature 依存からロードマップを導出する（変化時のみ再導出） |
| ② | unlock 判定 | 依存が解けて着手可能な Feature を判定する |
| ③ | `priority_cycle` | 候補 → スコア → ポリシー → キュー化 |
| ④ | キュー先頭 | 根拠（対象 / 理由 / スコア）付きで提示し、承認後に Issue 化 |
| ⑤ | **実行者選定（Capability Routing）** | `cp.estimate`（複雑度 CP の決定論算出）→ `cp.route`（CP × risk × routing-policy → native / 外部 runtime / 人間レーン）。判定不能は人間へ fail-closed |

### 実行者は勘で決めない（Capability Routing）

「誰（どのエンジン）に実行させるか」も意思決定系が出す。タスクの複雑度（Complexity Point — CP）は
CallGraph 影響範囲・横断 MOD 数・risk class から**決定論算出**し（自己申告・LLM 推定禁止 — Z-05）、
routing-policy が許可したレーンへ流す。守備範囲の**昇格は HIL 裁定のみ、降格は機械が即時適用**する。
CP8+ / High risk は routing-policy の内容に関わらず常に人間レーン（ハード下限）。
**routing 判定なしの native 自動 dispatch を作ってはならない**（Z-01 の選定層適用）。
命題の framework 正本 = dodoAI reference repository の concept `08-agentic-ooda-operations.md` §4.1。本章は project-local 手順のみを所有し、upstream Feature 状態を複製しない。

### 時間軸は導出する、日付は持たない

ロードマップの座標系は **行 = EPIC / CAP、列 = 論理時間（導出値）**である。
Feature ごとに手で日付を持たせれば必ず腐るため、列は依存グラフから自動導出し、
**手書きするのはリリースの意思と順序の理由だけ**にする。

### キューが詰まったら、キューを増やさない

滞留しているときに新しい Issue を作るのは、**症状を隠して悪化させる**行為である。
先に滞留の原因（古い ready / 重複 Issue / 依存の循環）を解消する。
**Gate を緩めて通すのは最悪の解**であり、P3 / P20 違反の自動化にあたる。

---

## 3. Evidence — 監査ログではなく訓練データ

Evidence を「後で怒られないための記録」と捉えると、**書く動機は最小化に向かう**。
dodoAI ADF に準拠する本プロジェクトでの Evidence の役割は違う。

| 観点 | 監査ログとしての Evidence | 世界モデルの訓練データとしての Evidence |
| --- | --- | --- |
| 目的 | 責任の所在を示す | 次の予測精度を上げる |
| 欠測の扱い | 空欄で構わない | **欠測と実測 0 を区別する**（P27） |
| 粒度 | 結果だけ | 入力・介入・観測・判定の対応 |
| 削除 | 古いものは消してよい | **消せない**（P24 captured） |

### 記録の規律

| # | 規律 | 理由 |
| --- | --- | --- |
| E-1 | 実行 ID を発行し、入力・ログ・成果物・Evidence へ同じ ID を引き回す | 後から実行を再構成できないと因果が追えない |
| E-2 | 再試行・子実行は新しい ID とし、親を明記する | 同じ ID を再利用すると別実行が混ざる |
| E-3 | 「観測しなかった」を 0 と書かない | 欠測を実測と混ぜると収束判定が無意味になる |
| E-4 | 定期処理のトレーサビリティはレポート MD で持たない | MD が増え続け、実体（lease 記録）と乖離する |
| E-5 | Evidence は改変・削除しない | 監査証跡は二度と戻らない（P24） |

---

## 4. 実行面の分担（Two-Plane）

実行ノードは 2 面ある。基本方針は **「両方が開発する。ただし同じ仕事はしない」**。

| 面 | 役割 | 持つ権限 |
| --- | --- | --- |
| **Local**（品質・HITL レーン） | 設計・難所の実装・高リスク作業・現時点の自律開発の主戦場 | **Merge 承認 / Human Override / SDT 書き込み主権** |
| **Server**（スループットレーン） | headless 連続稼働・可搬性実証・定型作業 | Merge Gate を持たない |

### 「同じ仕事をしない」を担保する 4 層

| 層 | 仕組み |
| --- | --- |
| ① 選定 | **単一の優先度キュー**から両面が取る（キューを二重に持たない） |
| ② 実行権 | 共有ストアの一意制約による lease。同一対象の二重着手を防ぐ |
| ③ 書き込み | **Single Writer** — 有効な lease を持つノードだけが status を更新する |
| ④ Git | branch namespace を分離し、**Merge Gate は 1 箇所（人間側）に集約する** |

### 暫定運用

**live な二面 claim の Evidence が揃うまで、開発 dispatch は一方のノードのみで有効化する。**
もう一方は read-only 監視と自身の Evidence 書き込みに限る。
Evidence にはどちらの面で実行したかを含める。資格情報は `env://` 論理参照のみ（P5）。

> 静的に対象を分割して両面を動かす例外は、**重複しない割付を Evidence 化した場合のみ**認める。

---

## 5. 自律実行の規律（A1 〜 A5 / Z-01 〜 Z-05）

「人間は設計し、Agent が自律実行する」を成立させる条件。

| # | 規律 | 内容 |
| --- | --- | --- |
| A1 | **人間は設計と承認に集中する** | 実装の反復を人間の手戻り作業にしない |
| A2 | **Agent は Harness 経由で実行する** | Harness を迂回した実行は Evidence を持たず、存在しなかったものとして扱う（P1 原則） |
| A3 | **判断の根拠を残す** | なぜその選択をしたかを Evidence に含める。結果だけでは次の判断が改善しない |
| A4 | **人間の介入点を奪わない** | 停止・承認・差し戻しの経路を常に開けておく |
| A5 | **失敗を隠さない** | FAIL を Finding として可視化する。隠した失敗は同じ形で再発する |
| Z-01 | **観測なき介入を作らない** | dispatch と observe を対にする（WM-4） |
| Z-02 | **収束を測る** | 誤差が周回ごとに縮んでいるかを見る。発散は設計の問題であり、試行回数の問題ではない |
| Z-03 | **停止条件を持つ** | 無限に再試行しない。同一操作の乱打を禁じる（P6） |
| Z-04 | **高リスクは人間へ渡す** | リスクの高い操作は自動で完遂せず承認を挟む |
| Z-05 | **自己申告を計測値にしない** | 「できたはず」を State に書かない（P27 / WM-3） |

---

## 6. 実行面の規律（V1 〜 V6 / RP-1 〜 RP-5 / DR-1 〜 DR-4）

§4 の 4 層を運用するときの細則。

| # | 規律 | 内容 |
| --- | --- | --- |
| V1 | **キューは 1 つ** | 選定元を二重に持たない。二重キューは必ず重複着手を生む |
| V2 | **着手には lease を要する** | 実行権のない対象へ書き込まない |
| V3 | **書き手は 1 つ** | status の書き込みは有効な lease 保持者のみ（Single Writer） |
| V4 | **branch namespace を分ける** | 面ごとに名前空間を分離する |
| V5 | **Merge Gate は 1 箇所** | 承認経路を複数持たない |
| V6 | **面を Evidence に記録する** | どちらの面で実行したかを残す |
| RP-1 | **保護ブランチへ直接コミットしない** | 作業ブランチを切ってから作業する（P1） |
| RP-2 | **専用経路以外で Git 操作しない** | 自動化は専用 Harness に限る（01 §2.5） |
| RP-3 | **push / merge は別ゲート** | 人間が停止・拒否・差し戻しできる |
| RP-4 | **生成物の扱いを明示する** | 何を stage するかを宣言し、無宣言の巻き込みを避ける |
| RP-5 | **資格情報は論理参照のみ** | 実値を書かない（P5） |
| DR-1 | **解禁は Evidence で判断する** | 「動くはず」で dispatch を両面有効化しない |
| DR-2 | **read-only 監視から始める** | 書き込み権限を最後に渡す |
| DR-3 | **静的割付を記録する** | 例外運用は重複しない割付を Evidence 化してから行う |
| DR-4 | **サーバー面に承認権を渡さない** | Merge 承認・Human Override は品質レーンが持つ |

---

## 7. 自律度の測り方

「自律開発できている」は感想ではなく計測値で語る。

| 観点 | 測ること |
| --- | --- |
| ループが回っているか | `autoloop.status` の verdict / 周回数 |
| 成熟度 | `autonomy.rate_compute` の多軸スコア |
| 連続稼働の耐性 | `autonomy.soak_evaluate` の soak 判定 |
| 収束しているか | 誤差が周回ごとに縮んでいるか（発散していれば設計の問題） |

**改善系・OODA・CRON・soak の作業では、着手前に上記を確認する。** 稼働中のループが既に
進めた変更と衝突させないためであり、重複作業は最も高価な無駄である。

---

## 8. OODA レポート規律（採点・成功確度・較正）

OODA の周回は**必ずレポートで回す**。レポートには次の 3 つを必須フィールドとして含み、
どれかを欠く記録はその周回が「観測されなかった」ものとして扱う（WM-4）。

| # | 必須フィールド | 内容 |
| --- | --- | --- |
| R-1 | **採点（Scorecard）** | 軸別 100 点満点。得点には必ず実測値（コマンド / Action と結果）を添える。根拠なき得点は自己申告であり計測値ではない（Z-05 / P27） |
| R-2 | **成功確度（Success Probability）** | active な Feature / STREAM / 施策ごとに 0.0–1.0 + 根拠を宣言する。改善主張は対指標（例: 完遂率 ⟷ 測定可能率）とペアで観測する（WM-2） |
| R-3 | **較正（Calibration）** | 前周回の確度と実績を突合し、予測誤差（Brier score）が縮んでいるかを見る（Z-02）。系統的に外れる判定基準は Skill / 運用方針へ書き戻す |

### 反復単位の規律（μ-cell）

反復を高速に回す律速は実行力ではなく**作業単位の設計**である。dispatch される反復単位は
機械可読な完了条件（`done_criteria`）・サイズ宣言・成功確度・周回上限を持つ最小反復単位
（μ-cell）とする。**散文だけの完了条件を持つ反復単位を新規生成しない。**
**μ-cell フィールドの SoT はタスクグラフノード側**（task node attributes）であり、Issue の
front matter はその投影である（§1.1 / P29。移行完了までは両方に書いてよいが、値の正は task node 側）。
μ-cell は DD01–DD05 / P9 / P20 を置き換えない — dispatch 粒度と完了判定だけを機械可読にする層である。

手順・フィールド契約の framework reference は dodoAI reference repository の `docs/4.operation/13-ooda-scorecard-iteration.md`。project-local Operation / LOOP / metrics catalog が未初期化なら運用開始せず blocker とする。
（本章は条項のみを所有し、手順を再掲しない）。

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 1.4.0 | 2026/08/22 | §0.1 新設 — 閉ループの正準構造（閉ループ = WF / 1 周 = DAG インスタンス / SDT = 状態空間）への手順接続を追加。ADF を閉ループ WF の第一適用対象と明記。命題正本 = concept 08 §4.2 |
| 1.3.0 | 2026/08/08 | §1.1 新設 — Harness Loop の一次 SoT をタスクグラフノードと明文化（P29 の手順面）。Select / Claim / 遷移 / Close の SoT と Issue（view + HIL + envelope）の役割を分離し、Issue ファイル名 rename 駆動経路の段階移行手順（併走 → drift 0 Evidence → 切替 → view 化）を規定。§8 μ-cell フィールドの SoT を task node 側へ移動 |
| 1.2.0 | 2026/08/08 | upstream で §2 に実行者選定（Capability Routing）を追加。project-local catalog 初期化までは fail-closed |
| 1.1.0 | 2026/08/08 | upstream で §8 OODA レポート規律を追加。framework 手順は dodoAI reference repository の Operation 文書を参照 |
| 1.0.0 | 2026/08/01 | 新設。旧 `02-agn-driven-development` / `07-harness-traceability`（475 行）+ ClineRules 側に散在した優先度決定・Two-Plane 運用を、条項の再定義を排し手順のみへ統合 |
