---
type: charter
title: 開発フロー — ADF 二経路 / A02 / A03 / DD01-DD05
description: 上流の二経路とタスクグラフ、DD 反復の手順正本
tags: [charter, adf, iteration, task-graph]
timestamp: 2026-08-01T14:00:00Z
---

# 開発フロー — ADF 二経路 / A02 / A03 / DD01-DD05

| Key | Value |
| --- | --- |
| Version | 1.4.0 |
| Updated | 2026/08/16 |
| Status | Approved |
| 種別 | **手順の正本**（条項は定義しない → 01 が正本） |

## 0. なぜ工程を固定するか

Agent は「とりあえず動くコード」を非常に速く出せる。速いからこそ、**何を作るべきかが未確定な
まま実装すると、破棄コストも同じ速度で積み上がる**。工程の固定は官僚主義ではなく、
**やり直しの量を減らすための投資**である。

不可逆の順序は 1 本だけである。

```
Reverse: 既存コード → CallGraph → SDT 逆導出 → 文書投影 → drift 裁定
                                                            │
Forward: Intent ───────────────────────────────────────────┴→ A02 → A03（SDT/AGN 検査） → DD01（骨格 + 契約） → DD02 → DD03 → DD04 → DD05
```

> **v1.1.0 で A03 / DD01 の役割を再定義した**（Charter 01 §2.2 P13 / P28）。骨格コード生成は
> 「コードを書く行為」であり、DD01（実装工程の入口）に属する。A03 は SDT/AGN 自身の構造検査
> （スキーマ宣言・書き込み主権・要件語彙境界）に専念する。

---

## 1. 上流の二経路（Reverse / Forward）

上流仕様は**白紙から書かない**。既存資産があるなら、実装が唯一の Ground Truth である。

| 経路 | 使う場面 | 入口 | 完了条件 |
| --- | --- | --- | --- |
| **A: Reverse**（brownfield — 既定） | 既存コード・既存文書がある | CallGraph 抽出 → SDT 逆導出 → 既存文書フレームへ投影 | drift 裁定 100%（未裁定を「完了」と呼ばない） |
| **B: Forward** | 新規の差分 Intent のみ | A02 から | A02 → A03 の連鎖完了 |

### Reverse の規律

- 既存の要求・設計文書は**投影先ビュー**であり、維持される SoT ではない。手で書き換えて二重管理しない。
- 実装由来の生成物は `candidate` 固定とし、HIL 裁定を経ずに `verified` / `done` へ昇格させない。
- 「どちらが正か分からない」差分は**捨てずに裁定待ちとして残す**（黙って消すのは P26 の意味削除）。

### 二重表現（WM-5 の適用）

上流成果物は必ず **MD（人間可読 view）+ JSON（機械可読 SoT）の対**で作る。
JSON 側は SDT へ蓄積され、そこで機械検証・トレーサビリティ・drift 検出が動く。
**MD だけ / JSON だけの成果物を「完了」と呼ばない。**

---

## 2. A02 — 要件モデル 6 層 + 全体設計

「BR/SR/UC を定義して」「A02 をやって」は、いずれも**次の 6 層 1 セット**を意味する。

```
縦糸（Stakeholder Value）  EPIC → FEATURE → UC → Evidence
横糸（System Capability）  CAP（FR を OWNS）→ MOD → Layer
```

| 層 | 意味 | 所有関係 |
| --- | --- | --- |
| **BR** | 事業要求 | — |
| **SR** | システム要求 | — |
| **UC** | ユースケース（最小の検証単位） | Feature は UC の束 |
| **CAP** | 能力 | **FR を所有する** |
| **FR** | 機能要件 | CAP のみが所有（Feature/UC は `satisfies` 参照のみ） |
| **MOD** | コード境界 | CAP が実現手段として持つ |

### 語彙の境界（RV-1 〜 RV-7 — P23 の施行細則）

この境界が崩れると、**実装事実と設計意図の照合が成立せず、ドリフト検出そのものが機能しなくなる**。
実測では Module 横断フローを SQ として登録した結果 SQ が 5,900 件規模に膨張し、認知不可能になった。

| # | 規律 | 内容 |
| --- | --- | --- |
| RV-1 | **SQ / AC は Module 境界で機械判定** | 関与 Module が 1 つなら **SQ**、2 つ以上なら **AC**（言語横断を含む）。Module はコード境界であり、ファイルパスやレイヤ（api / application / domain）は Module ではない。同一 Module 内で層をまたぐフローは SQ である |
| RV-2 | **実装事実と設計意図を混同しない** | SQ / AC はコードから導出される観測事実、UC は受入基準を持つ設計意図。ID 接頭辞を混用しない |
| RV-3 | **UC を定義する前に FR を生成しない** | FR は複数 UC を横断して初めて切り出せる。Module 単位に FR を割り当てると粒度が崩壊する。昇格の向きは `CallGraph → SQ / AC → UC 候補 → FR` に固定する |
| RV-4 | **FR の所有者は CAP のみ** | Feature / UC は `satisfies` で参照するだけで所有しない |
| RV-5 | **機械検証で 0 を担保** | 語彙違反が 0 でない状態を「完了」と呼ばない |
| RV-6 | **リバース生成は candidate 固定** | 実装由来の候補は HIL 裁定を経ずに昇格させない |
| RV-7 | **分類を下流投影でも保存する** | Module 境界で得た分類は、下流の投影先でも保存する。実装事実を設計意図の型へ投影しない |

検証 = `sdt.ontology_validate`。

### Step 0 — 所有者存在ゲート

Feature 単位の A02 着手前に、**所属 EPIC と FR を所有する CAP がカタログに存在するか**を確認する。
新しい関心事が既存 EPIC / CAP に収まらない場合、**Feature を先に切らず EPIC / CAP の新設・改訂から始める**。
既存拡張と新設で迷うときは HIL に選択肢を提示する。

### 成果物 3 点セット

| # | 何を | どこへ |
| --- | --- | --- |
| ① | Feature をリリースゴール一覧へ登録 | 版管理側の一覧 |
| ② | 要求モデル MD（人間可読 SoT） | EPIC / Feature の文書ツリー |
| ③ | AGN（因果グラフ: Feature ⟷ UC/FR/Task の接続と status）+ カタログ / roadmap 同期 | SDT の workflows ツリー |

物理パスは `.dodoai/repo-context.json` と SDT レイアウト契約が SoT である（本書に焼き付けない）。
ART（成果物 = 正本）と AGN（因果グラフ）の判別は `docs/99.sdt/README.md` が単独所有する。

> **A02 完了は A03 のトリガー**である。A02 で止めて完了報告しない。
> ユーザーが「UC まででよい」と**明示的に範囲を絞った時だけ**そこで止める。

---

## 3. A03 — SDT/AGN Conformance Gate

**A03 はコードを書かない。** A02 で確定した要件モデル・タスクグラフ自身が、SDT/AGN の構造規律に
従っているかを検査する工程である。ここを飛ばすと、DD01 が架空のスキーマ・所有権・語彙分類の上に
CONTRACT を積み、DD04 のガバナンス検査で一斉に破綻が露見する。

| 内容 | 検証 |
| --- | --- |
| スキーマ層（`agn/0.schema/`）の宣言整合性（dialect / role / ID 規則） | `sdt.schema_self_conformance` |
| SDT 書き込み主権（`derivation` / `authoring` 分類）が deny-by-default に違反していない | `sdt.authoring_validate` |
| 要件モデル語彙（SQ / AC / UC / FR の境界、P23）の誤分類が 0 | `sdt.ontology_validate` |
| タスクグラフの存在と UC/FR からの生成（P9 / P7） | `agn.schema_check` |

> **旧 A03（骨格生成 + `arch.layer_check` / `arch.module_boundary` + AG-04 Invariant baseline
> 凍結）は DD01 へ移した**（§5 参照）。骨格を書く・レイヤ境界を検証する・公開サーフェスを
> 凍結するのはいずれも実装工程の行為であり、設計工程では行わない。

### 上流ゲート（SG / AG / CJ / IV / AR）

各ゲートは工程の**出口条件**である。名前ではなく「何を確認して次へ進むか」で運用する。

| # | ゲート | いつ | 確認すること | 検証 |
| --- | --- | --- | --- | --- |
| SG-01 | マルチロールレビュー | A02 完了時 | 3 ロール（ドメイン / アーキ / QA）が approved（P12） | `agn.multi_agent_review` |
| SG-02 | NFR 適用判断 | A02 完了時 | 基準観点と領域固有観点を「Feature 固有要件 / 共通 NFR 継承 / 対象外」へ分類し、未確定を 0 にする（P11） | HIL レビュー（Feature 単位の検証 Action は未実装） |
| AG-01 | 境界整合 | DD01（新 EPIC/CAP 時は A01） | レイヤ・モジュール境界・階層互換 | `arch.layer_check` / `arch.module_boundary` |
| AG-02 | 全体設計 | A02 完了時 | コンテキストフロー JSON の機械検証（P15）+ 循環依存 0（P16） | `arch.context_flow_verify` |
| AG-03 | SDT/AGN Conformance | DD01 着手前 | スキーマ自己整合性・書き込み主権・語彙境界（P13） | `sdt.schema_self_conformance` / `sdt.authoring_validate` / `sdt.ontology_validate` |
| AG-04 | Scaffold + Invariant baseline | DD02 着手前 | 骨格生成 + 凝集性 + アーキテクチャ不変条件の baseline 凍結（P28） | `a03.scaffold_gate` / `arch.layer_check` / `arch.invariant_check` |

> **ゲートは advancer の status で代替しない。** 上位の前進 Action が「進んだ」と言っても、
> 各ゲートの Evidence を個別に確認する（CS-5）。

#### SG-02 — NFR 適用判断

`system-requirements.md` には、対象 Feature に必要な NFR 観点の適用判断を置く。

| 判定 | 必須記載 |
| --- | --- |
| Feature 固有要件 | 測定対象・条件・合否基準・検証方法 |
| 共通 NFR 継承 | 正準参照・本 Feature への適用範囲・Feature 固有差分（ある場合） |
| 対象外 | 対象外にできる具体的理由・変更しない境界 |

Performance / Scalability / Security / Availability / Observability / Maintainability / Portability は
**最低限の検討観点**であり、7 件すべてに新しい要求を書く義務ではない。対象領域に必要な観点は追加する。
カテゴリ名だけの列挙、共通 NFR の全文転記、測定不能な「高速・安全・高品質」は未確定として扱う。
現行の `nfr.performance_review` は性能ガバナンス用、`nfr.governance_evaluate` は実装・テスト Evidence を
含む横断評価用であり、いずれも A02 の Feature 単位適用判断を検証する Action ではない。

#### 契約検証（CJ-01 〜 CJ-05）— DD02 着手前

| # | 確認 |
| --- | --- |
| CJ-01 | 契約が機械可読な形で存在する（P14） |
| CJ-02 | 入出力スキーマが定義され、実装と一致する |
| CJ-03 | `owned_files` が DD01 の骨格生成で実際に作成した実パスを指す（架空パスでない） |
| CJ-04 | 異常系・境界条件が契約に含まれる |
| CJ-05 | 契約とテスト骨格が対応している（DD01 の三位一体） |

検証 = `agn.contract_json_verify`。

#### 統合検証（IV-01 〜 IV-05）— DD04

| # | 確認 |
| --- | --- |
| IV-01 | 観測性（ログ / trace）が境界をまたいで追跡できる |
| IV-02 | ガバナンス項目が全件通る |
| IV-03 | コンセプトとの整合を確認し Evidence を残す（P17） |
| IV-04 | Feature 内の UC がすべて DD03 まで完了している |
| IV-05 | 逸脱は Finding として登録し、done で覆い隠さない |

検証 = `concept.alignment_review`。

#### アーキテクチャ是正（AR-01 〜 AR-03）— 逸脱検出時

| # | 確認 |
| --- | --- |
| AR-01 | 逸脱を Finding として登録する（黙って直さない・黙って放置しない） |
| AR-02 | 是正を具体的な作業単位とタスクグラフ依存へ接続する |
| AR-03 | baseline を更新するのは意図的な設計変更のときだけとし、理由を残す |

検証 = `arch.layer_check` / `arch.module_boundary`。

---

## 4. タスクグラフ — dispatch の単位

タスクグラフは「誰が何を並列で実行できるか」を決める実行計画であり、**自律実行の前提**である。

| 規律 | 内容 |
| --- | --- |
| 生成元 | **UC / FR から生成する**。Feature から直接生成しない（P7 — 粒度が粗すぎて dispatch できない） |
| 存在ゲート | タスクグラフが無ければ**作ってから** DD01 に入る（P9） |
| 構成 | Feature ごとに `task-dd01` 〜 `task-dd05` を持つ |
| status 同期 | task status・`feature.json` の `dd_progress`・roadmap milestone を**同一作業内で**同期する（P20） |
| 検証 | `agn.schema_check` / `roadmap.sync_gate` |

---

## 5. DD01 → DD05

**UC 単位が DD01-DD03、Feature 単位が DD04-DD05。**

> **v1.1.0 で DD01 に骨格生成を統合した**。旧 A03 が担っていた「domain / application /
> infrastructure / interfaces フォルダ生成 + Domain skeleton + Application Port + Infrastructure Adapter
> + 未実装 Router」は、
> Feature の**最初の UC の DD01**でのみ実施する（2 件目以降の UC は既存骨格を再利用する）。
> 骨格生成直後に `arch.layer_check` / `arch.module_boundary` を実行し、DD02 着手前に
> Architecture Invariant baseline を凍結する（AG-04 / P28）。

Scaffold の言語・ランタイム差分は project-local Template で所有する。各 Project は
`.dodoai/scaffolds/clean-architecture/<template_id>/scaffold.json` と参照 Template file を持ち、
`arch.scaffold_generate` / `arch.scaffold_verify` / DD01 Scaffold Gate は同じ `template_id` を使う。
Generator 内へ言語別フォルダ表を追加しない。Template または Module の fingerprint が DD01 Gate 後に
変化した場合、`task_graph.transition_status` は DD02 入口を拒否し、Gate 再実行を要求する。

| Phase | 単位 | 内容 | 出口 |
| --- | --- | --- | --- |
| **DD01** | UC | ①（Feature 最初の UC のみ）project-local Template による骨格生成（domain/application/infrastructure/interfaces + skeleton）+ `arch.layer_check` / `arch.module_boundary` 通過 ② CONTRACT + Contract JSON + テスト骨格 + AGN 定義の三位一体。`owned_files` は ① で生成した実パスを指す | Contract JSON 検証（P14）+ Scaffold 検証（P28） |
| **DD02** | UC | 実装。全テストが通るまで。Mock フォールバック禁止（P2）。着手前に Architecture Invariant baseline 凍結済みであること（P28） | テスト PASS + Coverage |
| **DD03** | UC | 異常系テスト強化。ここまでが UC 単位 | 異常系網羅 |
| **DD04** | Feature | Integration Verification — 観測性（ログ / trace）+ ガバナンス全件 + Concept Drift Check | `concept.alignment_review` |
| **DD05** | Feature | System Validation（下記 2 トラック） | Track 判定 |

### DD05 の 2 トラック — リリース連動

Track A は開発完了の一部、**Track B（Release Validation）はリリースイベント連動の別軸ゲート**である
（条文 = 06 §4 Check 5）。分岐は `feature.json` の `release_status`（リリース有無）で行う。

| 状態 | 必要な検証 |
| --- | --- |
| 共通（全 Feature） | **Track A**: E2E + AI Visual + Human 確認 |
| `release_status: unreleased` | Track B は**対象外**。デプロイ検証・稼働証跡の欠如を理由に Feature done をブロックしない |
| `release_status: released` | Track A + **Track B**: リリース面へ deploy / 配布 → readiness → smoke → **リリース先実 URL** への browser E2E → 実行ログ検証 |

> **ローカル起動 URL の E2E は Track B の代替にならない。** 「動いた」のがローカルだけなら、
> それはリリース先で動く証拠を 1 つも持っていない。資格情報は `env://` 論理参照のみ（P5）。
> リリース形態（サーバー deploy / ローカルアプリ配布）は検証手段の選択にのみ使い、**免除条件にしない**。
> 旧 `deployment_validation: local-only / required` の環境ベース分岐は deprecated。

### Feature Complete

DD04 + DD05 Track A が PASS した状態を Feature Complete と呼ぶ。
Track B（Release Validation）は Feature Complete の前提ではなく、**リリース済み Feature の稼働保証**として
別軸で判定する。**リリース済みで Track B FAIL の Feature を稼働保証済みと扱わない** —
具体的な Finding とタスクグラフ依存へ戻し、優先度計算へ差し戻す。

---

## 6. 各工程の入口条件（早見表）

| 着手する工程 | 満たすべき条件 | 対応禁止 |
| --- | --- | --- |
| A03 | A02 完了（6 層 + NFR 適用判断の未確定 0 + マルチエージェントレビュー approved） | P11 / P12 |
| DD01 | A03 PASS（スキーマ自己整合性 + 書き込み主権 + 語彙境界）+ タスクグラフ存在 | P13 / P9 |
| DD01（骨格生成） | DD01 着手済み（Feature 最初の UC のみ） | — |
| DD02 | CONTRACT.md + Contract JSON 検証 + Scaffold 検証（骨格生成 + 凝集性 + Invariant baseline 凍結） | P4 / P14 / P28 |
| DD Phase 全般 | コンテキストフロー検証済み + 循環依存 0 + CallGraph 影響調査済み | P15 / P16 / P18 |
| Feature Complete | DD04 + DD05 Track A PASS + status 同期（Track B はリリース連動の別軸 — §5） | P17 / P20 |

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 1.4.0 | 2026/08/16 | DD05 の分岐を `deployment_validation`（環境属性）から `release_status`（リリース有無）へ再定義。Track B を Release Validation（リリースイベント連動の別軸ゲート）とし、未リリース Feature の Feature Complete を稼働実績でブロックしない。06 §4 Check 5 / `.clinerules-detail/11-completion-gate.md` と同期 |
| 1.3.0 | 2026/08/08 | DD01 Scaffold を `.dodoai` project-local Template 駆動へ変更。言語差分を `template_id` で選択し、Generator / Verifier のmanifest共有とTemplate/Module fingerprintによるDD02入口fail-closedを手順化 |
| 1.2.0 | 2026/08/08 | SG-02 を固定 7 カテゴリ一律充足から NFR 適用判断へ変更。Feature 固有要件・共通 NFR 継承・対象外の必須情報を定義し、既存 NFR Action を A02 の Feature 単位検証器として誤用しないことを明記 |
| 1.1.0 | 2026/08/06 | A03 を「コード骨格生成」から「SDT/AGN 構造検査（スキーマ自己整合性・書き込み主権・要件語彙境界）」へ再定義。旧 A03 の骨格生成 + `arch.layer_check`/`arch.module_boundary` + AG-04 Invariant baseline 凍結を DD01（Feature 最初の UC のみ）へ移動。AG-01/AG-03/AG-04 の対応表・タイミングを更新。Charter 01 §2.2 P13/P28 と同期 |
| 1.0.0 | 2026/08/01 | 新設。旧 `03-agent-task-graph` / `04-iteration-protocol` / `10-sa-phase-quality-gate`（1,413 行）を、条項の再定義を排し手順のみへ統合 |
