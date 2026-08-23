---
type: charter
title: 開発憲章 — my-crypto-app Development Charter
description: dodoAI ADF に準拠する本プロジェクトの最上位原則・禁止事項・品質基準の唯一の正本
tags: [charter, governance, prohibition, principle]
timestamp: 2026-08-01T14:00:00Z
---

# 開発憲章 — my-crypto-app Development Charter

| Key | Value |
| --- | --- |
| Version | 4.8.0 |
| Updated | 2026/08/11 |
| Status | Approved |
| 位置づけ | **憲法**。施行規則の正本は `AGENTS.md`、ClineRules はその補助投影、MCP/Action は執行機構 |
| 条項の正本 | **本ファイルのみ**（02〜07 は手順・接続の正本であり条項を再定義しない） |

## 0. この憲章の存在理由

my-crypto-app は dodoAI ADF と dodo Core の統治下で Agent が継続開発する personal Custom App である。したがって憲章は理念の表明ではなく、**機械が読み取り、ゲートとして執行する条項の集合**でなければならない。Crypto 固有の意図・生存原理・鍵境界は `docs/1.concept/00-overview.md` と `docs/4.common/0.common-requirements/00-common-requirements.md` が所有し、本 Charter はそれらを上書きしない。

本憲章の条項は `rules.charter_sync` によって `charter-catalog.json`（機械可読 SoT）へ写像され、
`rules.audit` が grounding と drift を検証する。**MD に書いただけの条項は執行されない。**

### 憲章が満たすべき 3 条件

| # | 条件 | 破ったときに起きること |
| --- | --- | --- |
| 1 | **条項は一箇所にある** | 同じ禁止が複数ファイルに書かれ、改訂時に片方だけ直り、どちらが正か判定不能になる |
| 2 | **各条項は検証手段を名指す** | 検証できない条項が「HARD GATE」を名乗り、Agent が「ゲートは飾り」と学習する |
| 3 | **手順・事実を条項に混ぜない** | ポート・パス・件数が腐り、条項ごと信用されなくなる |

> **v4.0.0 で全面再構築した理由**: 旧憲章は 11 ファイル 4,230 行に膨張し、同一の禁止事項が
> 複数ファイルへ重複し、実在しない Action を HARD GATE として名指していた。**条項数ではなく
> 「1 条項あたりの検証可能性」が劣化していた**ため、条項を本ファイルへ一元化し、手順を
> 02〜06 へ分離した。本リポジトリには旧 Charter archive を複製せず、移植元の履歴は dodoAI reference repository で追跡する。

---

## 1. 最上位原則 — 人間は設計し、Agent が自律実行する

人間の役割は**設計・承認・停止**であり、実装の反復は Agent が担う。
この分担が成立するには、Agent の出力が**検証可能**であり、人間が**いつでも介入できる**必要がある。

### 1.1 Eight Principles（アーキテクチャ原則）

| # | 原則 | 内容 |
| --- | --- | --- |
| P1 | **Harness first** | 全 Agent 実行は Harness を通る。Harness を迂回した実行は Evidence を持たないため存在しなかったものとして扱う |
| P2 | **Twin as state** | SDT は可視化ではなく状態空間である。仕様・コード・テスト・Evidence はすべて SDT ノードとして存在する |
| P3 | **Runtime replaceable** | 特定 Runtime に固定しない。Codex / Claude Code / dodo coder / internal は交換可能な実行系である（使い分け = 03） |
| P4 | **Evidence by default** | 実行・判断・検証は最初から Evidence として記録する。Evidence は監査ログではなく**世界モデルの訓練データ**である |
| P5 | **Human override** | 人間は停止・承認・修正・差し戻しができる。Agent が人間の介入点を奪う設計を作らない |
| P6 | **Temporal through Harness** | CRON / Scheduler は Harness の入口であり、別経路ではない。定期実行も Evidence を残す |
| P7 | **Sovereign depth** | 実行環境の主権を保つ。閉域・オフラインでも成立する経路を常に一つ持つ |
| P8 | **Runtime boundary enforcement** | `AGENTS.md`・Skill・Operation List・prompt は発見と判断の入力であり、強制機構ではない。必須の残作業は Codex / Claude Code / dodo Coder に共通の Core Hook Gate で完了境界を検査し、宣言済み Operation・Agent・Skillへ接続する。CRONを完了フックの代用にしない |

**Completion Operation Gate**: source-affecting workset が `operations.json` の
`attributes.completion_gate` に一致した場合、`sovereign.hook_gate` は完了を一度だけ差し戻し、
同一 Agent turn に宣言済み Operation を実行させる。High/critical risk は current explicit intent
または scope を限定した standing authorization が無ければ自動実行しない。同一 plan fingerprint を
反復 block / dispatch せず、実行不能時は一つの具体的 blocker を報告して停止する。

### 1.2 世界モデルとしての SDT — 5 不変条件

開発統治の全条文は次の一つの表現原理から導出される。プロダクトの最上位目的関数は `docs/1.concept/00-overview.md` の生存原理が所有する。

$$\min H(S) \quad \text{subject to} \quad Meaning(S) = Meaning(World)$$

**意味を保存したまま、状態表現のエントロピーを最小化する。** 5 不変条件が揃って初めて
「世界モデル」が成立する。コンセプト文書の存在は成立条件ではない。

| # | 不変条件 | 内容 | 対応禁止 |
| --- | --- | --- | --- |
| WM-1 | **定式化** | 新しい概念・ノード種別は World Model 十要素（Entity / State / Relation / Constraint / Goal / Intervention / Observation / Reward / Dynamics / Provenance）のどれかを言えること | P25 |
| WM-2 | **エントロピー最小化** | $H$ と $Meaning$ を**同時に**測る。意味を削れば $H$ は下がるため、$H$ 単独の改善主張は禁止。文書・ルールは意味を保つ最小十分記述とし、重複・脚色・推測を加えない | P26 |
| WM-3 | **統治** | Fact（決定論的計測）/ Belief（confidence 付き）/ Hypothesis を混ぜない | P27 |
| WM-4 | **トレーサビリティ** | 観測されない介入を作らない。dispatch と observe を対にし、結果を State へ反映する | P20 / P24 |
| WM-5 | **双対表現** | MD（人間可読 view）と JSON（機械可読 SoT）の**対**で維持する。片方だけを正本と呼ばない | P10 / P21 |

**用語規約**: 世界モデル層で「世界を変える操作」は **Intervention（介入）**。dodo Core の
`Action Registry` / `action_key` とは階層が異なる（Intervention = 抽象型、Core Action = 実装形態の一つ）。

**SDT 横断 Action の命名規約**: ART と AGN を横断して SDT 全体を投影する Graph Bundle の
正規 `action_key` は **`sdt.graph_bundle`** とする。**`agn.graph_bundle` は旧称の deprecated
compatibility alias** であり、新規コード・規範・手順は正規名を使う。過去 Evidence では実行時の
旧称を改変せず、MD で参照するときに「旧称」と補足する。

> プロダクト概念正本: `docs/1.concept/00-overview.md` + `docs/2.sdt-design/02-data-model.md`／施行 = 05

### 1.3 Charter as SDT — 憲章の自己記述条項

| # | 条項 | 内容 |
| --- | --- | --- |
| CS-1 | **憲章は SDT の第一級ノード** | 憲章の Principle / Prohibition / Gate / 数値閾値は `canonical_id = C:GovernanceRule` の rule ノードとして charter catalog に登録する |
| CS-2 | **規範文は MD、enforcement は SDT** | 散文の正本は本憲章の MD とする。カタログは `md_ref`・条項参照・`enforcement` binding・機械可読な閾値だけを保持し、規範文を複製しない |
| CS-3 | **憲章改訂は SDT 同期を伴う** | 条項を追加・改訂・削除した作業では、同一作業内で `rules.charter_sync` を実行し `rules.audit` の Charter drift を 0 にする。未同期の憲章改訂を完了と呼ばない |
| CS-4 | **憲章は DocGraph の根拠として参照可能** | 憲章ディレクトリは DocGraph ingest 対象とし、rule ノードは `R:grounded_in` で該当 document / section / chunk を参照する |
| CS-5 | **偽のゲートを書かない** | 条項が名指す検証手段は実在する Action でなければならない。検証手段が無い条項は「宣言的原則」と明示し、HARD GATE を名乗らせない |

---

## 2. 禁止事項

禁止事項の**唯一の正本は本節**である。ClineRules・AGENTS.md・02〜06 は本節を参照するのみで、
条文を再定義しない（重複は改訂漏れを生むため CS-2 違反）。

**強度の 3 分類**: `HARD GATE` = 機械検証があり違反時に停止 / `AUDIT` = 機械計測があり継続監視 /
`ADVISORY` = 検証器が未実装で HIL レビューが代替（**機械検証済みと報告してはならない**）。

### 2.1 プロセスの禁止

| # | 禁止 | 強度 | 検証 |
| --- | --- | --- | --- |
| P1 | Git 操作（commit / push / merge）。特に `develop` / `main` / `master` への直接コミット・直接 merge。専用の Git automation Harness のみ例外（§2.5） | ADVISORY | 人間レビュー |
| P2 | Mock data へのフォールバック。DD02 以降は実機結合 | ADVISORY | コードレビュー |
| P3 | **テスト失敗状態での完了報告**（Zero Tolerance） | HARD GATE | `test_evidence.audit` |
| P4 | CONTRACT.md なしでの実装着手（DD01 スキップ） | HARD GATE | `agn.contract_json_verify` |
| P5 | シークレット / 顧客実値のハードコード。テスト・fixture・Harness・golden dataset を含む。参照は `env://` 論理参照のみ | AUDIT | `code.hardcode_audit` |
| P6 | 同一ツール × 同一引数の 2 回以上呼び出し（ツールコールループ） | ADVISORY | セッション自己申告 |
| P7 | Feature から直接タスクグラフを生成すること。UC / FR 単位へ分解する | HARD GATE | `agn.schema_check` |
| P9 | **タスクグラフなしでの開発着手**。存在しなければ UC / FR から先に作る | HARD GATE | `agn.schema_check` |

> **欠番を詰めない**: P8（旧「憲章 9 ファイル未読での着手」）は憲章が 6 ファイルへ再編され
> 前提が消滅したため廃止した。ただし**番号は再利用しない**。既存の Issue・Evidence・ClineRules が
> 参照する番号を動かすと、監査証跡の指す条項が別物にすり替わる（WM-4 / P24 の趣旨）。

### 2.2 上流工程の禁止（A02 / A03 → DD01 → DD02 の順序）

> **v4.3.0 で A03 / DD01 の役割を再定義した**: 旧 A03 は骨格コード生成を担っていたが、
> 「コードを書く行為」は設計工程ではなく実装工程に属する。A03 は **SDT/AGN 自身の構造規律**
> （スキーマ宣言整合性・書き込み主権・要件語彙境界・タスクグラフ存在）を検査するゲートへ
> 専念させ、骨格生成・レイヤ/モジュール境界検証・Architecture Invariant baseline 凍結は
> **DD01 側**（骨格は Feature 単位で最初の UC のみ）へ移した。P13 は「A03 突破」の対象を
> 差し替え、新設 P28 が DD01→DD02 の新しい境界を担う（手順の正本 = 02 §3 / §5）。

| # | 禁止 | 強度 | 検証 |
| --- | --- | --- | --- |
| P11 | Feature 単位の非機能要件の適用判断に未確定が残る状態で A02 を完了扱いにする、または A03 に着手すること。各観点は「Feature 固有要件」「共通非機能要件の継承」「対象外」のいずれかへ分類し、固有要件は測定可能な合否基準と検証方法、継承は正準参照と適用範囲、対象外は理由を持たせる。カテゴリ名や見出しだけでは充足とみなさない | ADVISORY | HIL レビュー（Feature 単位の機械検証 Action は未実装） |
| P12 | A02 完了時のマルチエージェントレビュー未実施、または 3 ロール approved 未達で A03 着手 | HARD GATE | `agn.multi_agent_review` |
| P13 | **A03（SDT/AGN Conformance Gate）なしで DD01 着手**。A03 はコードを書かない。スキーマ自己整合性・書き込み主権・要件語彙境界のいずれかが未 PASS のまま DD01 に進むことを含む | HARD GATE | `sdt.schema_self_conformance` / `sdt.authoring_validate` / `sdt.ontology_validate` |
| P14 | Contract JSON なしで DD02 着手 | HARD GATE | `agn.contract_json_verify` |
| P15 | コンテキストフロー JSON の機械検証なしで DD Phase 着手 | HARD GATE | `arch.context_flow_verify` |
| P16 | モジュール間の循環依存が残った状態で DD Phase 着手 | HARD GATE | `arch.module_boundary` |
| P17 | Concept Alignment Evidence なしでの Feature Complete | HARD GATE | `concept.alignment_review` |
| P28 | **Project-local Template による骨格生成（DD01）+ レイヤ/モジュール境界検証 + Architecture Invariant baseline 凍結なしで DD02 着手**。Generator と Verifier が同じ Template manifest を参照しない、Template または Module が DD01 検証後に変わったまま DD02 に入る、Feature の最初の UC で未実施のまま 2 件目以降の UC が DD02 に進むことを含む | HARD GATE | `a03.scaffold_gate` / `arch.scaffold_verify` / `task_graph.transition_status` / `arch.layer_check` / `arch.module_boundary` / `arch.invariant_check` |

P11 の基準カテゴリは、Performance / Scalability / Security / Availability / Observability /
Maintainability / Portability を**最低限の検討観点**として使う。これは全カテゴリに Feature 固有要件を
新設させる規則でも、非機能要件全体を 7 種に閉じる分類でもない。アクセシビリティ、信頼性、プライバシー、
決定性、監査性など、対象領域に必要な観点は追加する。共通非機能要件の重複転記は禁止し、正準参照と
Feature への適用差分だけを書く。

### 2.3 SDT の禁止

| # | 禁止 | 強度 | 検証 |
| --- | --- | --- | --- |
| P10 | **SDT の二重 SoT**（同一データ種別を JSON と DB の両方で authoritative 管理）。禁止の本質は「DB 化」ではなく「正が 2 つになること」。要求モデル・憲章・HIL 承認・trace の SoT は SDT の JSON / MD のみとし、状態系（task status / Evidence 等）は append-only ログを SoT としてその投影のみを持つ | AUDIT | `sdt.governance_metrics` |
| P18 | **CallGraph 影響調査なしのコード変更**。変更前に影響 UC / Feature / EPIC を把握し、Preload Evidence を出力する | HARD GATE | `callgraph.focus` |
| P19 | CallGraph 巨大 JSON の直読み。走査は Action 経由とし、直読みは Action 不能時の fallback に限り Evidence へ明記する | AUDIT | `callgraph.focus` |
| P20 | **ロードマップ / タスクグラフ status 未同期での完了報告**。`task-dd*.json` の status・`feature.json` の `dd_progress`・roadmap milestone が不同期のまま「完了」と言わない | HARD GATE | `roadmap.sync_gate` |
| P21 | **憲章改訂時の charter-catalog 未同期**（CS-3 の執行）。条項の追加・改訂・削除は同一作業内で `charter-catalog` と DocGraph grounding を同期し、Charter drift を 0 にする | HARD GATE | `rules.charter_sync` |
| P22 | Gate 未検証での Issue `_done` 化・Archive。本文の文言は補助シグナルであり、単独でクローズ根拠にしない。Gate 入力が取得不能なら fail-closed とする | HARD GATE | `agn_issue_archive` |
| P23 | 要件モデル語彙の誤分類登録（SQ / AC / UC / FR の境界違反）。SQ = 単一 Module 内、AC = Module 横断。UC 定義前に FR を生成しない。FR の所有者は CAP のみ | HARD GATE | `sdt.ontology_validate` |
| P24 | SDT 書き込み主権に反する書き込み。`derivation: derived` の生成物を手編集しない／`captured` の監査証跡を改変・削除しない／実効 authoring が `unclassified` の SDT へ書き込まない（deny-by-default） | HARD GATE | `sdt.authoring_validate` |
| P29 | **機械ループの SoT を Issue MD に置くこと**。自律ループ（Select / Claim / status 遷移 / Close）の正はタスクグラフノード（`task-dd*.json` / `feature.json`）であり、Issue（`.dodoai/issue/`）は人間可読 view + HIL 承認 + dispatch envelope である。Issue のファイル名 suffix（`_ready` / `_in-progress` / `_done`）の rename を機械ループの一次 SoT とする経路を**新設・拡張しない**。既存の Issue ファイル駆動経路は段階移行（併走記録 → drift 0 の Evidence → 切替 → view 化）で縮退させる | ADVISORY | HIL レビュー（project-local TaskGraph dispatch SoT の機械検証実装をもって HARD GATE へ昇格。dodoAI upstream の実装を local enforcement 済みの証拠にしない） |

### 2.4 世界モデルの禁止（段階導入 — 現在 ADVISORY）

| # | 禁止 | 強度 | 昇格条件 |
| --- | --- | --- | --- |
| P25 | 十要素アンカー未宣言の概念を `canonical` として使用（WM-1） | ADVISORY | `sdt.ontology_validate` の十要素アンカー検出の実装 |
| P26 | **意味保存の観測を伴わないエントロピー改善主張**（WM-2）。「整理した」「削減した」「統合した」を $H$ 単独で主張しない。件数・行数の減少をそのまま $H$ の低下と読み替えない | ADVISORY | $H$・$Meaning$ 同時計測器の稼働 |
| P27 | Fact / Belief / Hypothesis を混在させた State 書き込み（WM-3）。欠測を実測 0 として記録することも禁止 | ADVISORY | Fact / Belief 分離スキーマの検証実装 |

> **段階導入の規律（CS-5 の帰結）**: 実在しない検査を HARD GATE と宣言すると、Agent は
> 「ゲートは飾り」と学習し、その学習が**実在するゲートへ波及する**。よって P25-P27 は
> 検証器が動くまで ADVISORY とし、**「機械検証済み」と誤認して報告しない**。

### 2.5 P1 例外 — Git 操作専用 Harness

通常の開発 Agent は Git 操作をしない。自律化する場合は次の全条件を満たす専用経路に限定する。

| 条件 | 必須内容 |
| --- | --- |
| AGN 登録 | WF / Agent / Skill / CRON / Operation が SDT と Operation カタログに登録されている |
| Scope 限定 | 対象リポジトリ・submodule・branch pattern・stage 対象が明示されている |
| Safety Gate | dirty diff・secret scan・test status・生成物の扱いを検証し、失敗時は commit しない |
| Evidence | 実行結果・差分サマリー・対象 SHA・検証結果を記録する |
| Human Override | push / merge は別 Gate とし、人間が停止・拒否・差し戻しできる |

### 2.6 運用の禁止

Docker リビルド（明示指示なし）／長いインラインスクリプト（ファイルに書く）／`rm -rf` の無確認実行
（`trash` を優先）／`_in-progress` を放置した新規タスク着手／未登録の外部 MCP 接続／
CRON レポート MD の新規作成（トレーサビリティは lease DB が SoT）。

---

## 3. 品質基準

| 基準 | 閾値 | 検証 |
| --- | --- | --- |
| テスト成功率 | 100%（失敗が 1 件でもあれば未完了） | `test_evidence.audit` |
| カバレッジ | coverage >= 80% | `test_evidence.audit` |
| Evidence 欠落 | gaps = 0 かつ broken_links = 0 | `test_evidence.audit` |
| モジュール凝集度 | LCOM4 <= 2 | `arch.layer_check` |
| モジュール間依存 | Cross-Module Import = 0 / Domain Purity = 0 / Cycle = 0 | `arch.module_boundary` |
| ロードマップ同期 | stale_task_status = 0 / roadmap_drift = 0 | `roadmap.sync_gate` |
| 憲章同期 | Charter drift_count = 0 / missing_grounding = 0 | `rules.audit` |

数値の意味と測り方は 06 が正本である。**本節の閾値と 06 が食い違う場合は本節を正とし、
同一作業内で 06 を同期する**（CS-2）。

---

## 4. 憲章の構成

| ファイル | 役割 | 条項を定義するか |
| --- | --- | --- |
| `01-development-charter.md` | **本書**。最上位原則・禁止事項・自己記述条項・品質基準 | **する（唯一）** |
| `02-development-flow.md` | ADF 二経路 → A02 → A03 → DD01-05 とタスクグラフ | しない |
| `03-mcp-and-runtime.md` | MCP 起点の開発手順と Runtime の使い分け | しない |
| `04-autonomous-loop.md` | 自律開発ループの運用と Evidence 書き戻し | しない |
| `05-entropy-governance.md` | エントロピーを増やさない仕組み | しない |
| `06-quality-gate.md` | Gate 一覧・テスト戦略・完了ゲート | しない |
| `07-requirements-architecture-map.md` | **層の接続の地図**。World Model → Core Concept → Strategy → 共通 BR/SR → 縦糸 EPIC/Feature/UC ⟷ 横糸 CAP/FR/MOD/DFR → Code → SQ/AC → Evidence の接続・所有者境界・判断フロー | しない（各層の定義も再掲しない = A クラス） |

参照リンクは論理 URI（`ln://`）または本表のファイル名で行い、**物理パスの羅列を本文に書かない**
（移動で切れる／SDT が既に参照関係を持つため二重管理になる）。

> **どこに何を書くか迷ったら `07-requirements-architecture-map.md` を最初に開く。**
> 07 は接続と所有者境界だけを単独所有し、各層の定義は正本を指す。07 と層正本が矛盾した場合は
> **層正本が勝ち、07 を修正する**（$H_{semantic}$ の再発防止 — 05 §0）。

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 4.8.0 | 2026/08/11 | P8 Runtime boundary enforcement と Completion Operation Gate を追加。自然言語指示を強制機構と誤認せず、Codex / Claude Code / dodo Coderの共通Core完了境界で残Operationを1回だけ継続し、scope付き認可・fingerprint反復抑止・具体的blocker停止を要求。CRONは使用しない |
| 4.7.0 | 2026/08/08 | ART + AGN を横断する Graph Bundle の正規 Action key を `sdt.graph_bundle` と定め、`agn.graph_bundle` を旧称の deprecated compatibility alias に限定。新規コード・規範・手順は正規名、過去 Evidence は不変とする命名規約を追加 |
| 4.6.0 | 2026/08/08 | P28 を project-local Scaffold Template 駆動へ強化。Generator / Verifier の同一 manifest 参照、Template fingerprint / Module fingerprint の DD02 入口再照合、`task_graph.transition_status` の fail-closed admission を必須化 |
| 4.5.0 | 2026/08/08 | upstream で P29 新設 — 機械ループの SoT はタスクグラフノード、Issue MD は人間可読 view + HIL 面に限定。project-local enforcement は別途実測する |
| 4.4.0 | 2026/08/08 | P11 を固定 7 カテゴリの一律充足から、Feature 固有要件・共通非機能要件の継承・対象外理由による適用判断へ改訂。Feature 単位の検証器が未実装のため偽の HARD GATE を廃し、ADVISORY + HIL として機械保証範囲を明確化 |
| 4.3.0 | 2026/08/06 | A03 の役割をコード骨格生成から SDT/AGN 構造検査（スキーマ自己整合性・書き込み主権・要件語彙境界）へ再定義し、骨格生成・レイヤ/モジュール境界検証・Invariant baseline 凍結を DD01 側（Feature 最初の UC のみ）へ移動。P13 の対象を差し替え、新設 P28 で DD01→DD02 の境界を明示。02 / 06 / ADF A-phase・DD-phase と同期 |
| 4.2.0 | 2026/08/04 | カバレッジ完了閾値を ADF v5.0 §12 と同じ 80% に統一 |
| 4.1.0 | 2026/08/02 | §4 構成表に `07-requirements-architecture-map.md`（層の接続の地図 / A クラス）を追加。BR→SR→FR→CAP の連鎖崩壊と正本再掲によるドリフトの再発防止を、条項ではなく**接続の索引**として分離 |
| 4.0.0 | 2026/08/01 | upstream で全面再構築。旧 11 ファイルの重複を凍結し、強度 3 分類と CS-5（偽のゲート禁止）を導入。旧 archive は本リポジトリへ複製しない |
