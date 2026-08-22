---
type: procedure
title: Domain Gates — 領域別ゲート（Architecture / SDT / UI / 運用資産）
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, gates, architecture, sdt, ui]
---

# Domain Gates

`10-preload-gate.md` に加えて、触る領域ごとに満たすゲート。該当領域でなければ読む必要はない。

---

## 1. Architecture（Clean Architecture / DD01 Scaffold）

**適用**: 新規 Feature の layer 作成、モジュール境界を跨ぐ変更、依存方向の変更。

A02 後の A03 は SDT/AGN Conformance のみで、コードを書かない（Charter P13）。Feature 最初の UC の
**DD01 内**で project-local Template を選択して Scaffold Gate を通し、DD02 入口で P28 を再検証する。

| 検査 | Action |
|---|---|
| Scaffold の生成・検証 | `a03.scaffold_gate` |
| DD02 入口の P28 強制 | `task_graph.transition_status` |
| layer 責務の逸脱 | `arch.layer_check` |
| モジュール境界の侵犯 | `arch.module_boundary` |
| tier 互換 | `arch.tier_compat` |
| Context Flow 整合 | `arch.context_flow_verify` |

凝集度・依存メトリクス（LCOM4 / Fan-out / Cross-Module Import / Domain Purity）は
**Module 境界**で測る。`dodo_core/module/<name>` と `frontend/src/modules/<name>` は
要求モデルの Feature ではなく **Module（コード境界）**である。Feature は UC の束（stakeholder に見える成果物）。

Generator / Verifier は同じ project-local Template manifest と `template_id` を使用する。Template または
Module fingerprint が DD01 Gate 後に変化した場合は DD02 を拒否し、Gate を再実行する。

❌ Scaffold なしで DD02 着手 / A03 でコード生成 / Domain 層から infrastructure へ直接依存 / facade のはずの router に業務ロジック

---

## 2. SDT / AGN / ART データ

**適用**: SDT/AGN/ART の JSON を生成・補修・移行するとき。

ART と AGN を横断する Graph Bundle は **`sdt.graph_bundle`** を使う。`agn.graph_bundle` は旧称の
deprecated compatibility alias であり、互換性確認以外の新規呼出しへ使わない。過去 Evidence の
実行時キーは不変とし、MD で旧称を引用するときだけ「旧称」と補足する（条文正本: Charter §1.2）。

1. **先に schema を読む**。`docs/99.sdt/agn/0.schema/` 配下の該当スキーマを確認してから書く
2. **書く前に主権を問う**（Charter P24）。`sdt.authoring_resolve` に対象パスと `actor` を渡し、
   書き込みが許されるかを確認する。生成物・監査証跡・未分類 SDT は書けない
3. パス解決は `.dodoai/repo-context.json` 経由。旧ツリーのパスをハードコードしない
4. 完了主張の前に MCP で**再計測**する（自分の書き込み結果を推定で PASS にしない）

| 検査 | Action |
|---|---|
| **書き込み主権の解決（書く前）** | `sdt.authoring_resolve` |
| **主権宣言の整合（AUTH-V01..V06 / 完了ゲート）** | `sdt.authoring_validate` |
| 主権の分類カバレッジ・未分類一覧 | `sdt.authoring_classify` |
| 生成物の手編集検知（再生成 fingerprint 比較） | `sdt.authoring_drift` |
| オントロジー整合（unmapped_term / mapping_conflict / core_specific_leak / undeclared_node_type）+ 概念の品質バー Q1-Q4 | `sdt.ontology_validate` |
| governance 登録状況 | `sdt.governance_metrics` |
| LN 参照の健全性 | `sdt.ln_link_integrity` |
| グラフ横断照会 | `sdt.khop_traverse` / `sdt.search` / `sdt.semantic_search` |

**巨大な graph JSON を直読みしない。** 上記の Action で必要分だけ取得する。

### 新種の成果物をどこへ置くか（ART か AGN か）

**新しい種類のデータを SDT へ追加するとき、既存ルールのフレーズを流用して置き場を決めてはならない。**

判別の正本は `docs/99.sdt/README.md`（ART/AGN 判別の単独所有者）。判定は 1 問で足りる。

> **それは成果物か → ART。成果物どうしの関係か → AGN。**

| 対象 | 層 |
|---|---|
| 観測・実行・計測の記録（Evidence、テスト結果、プロンプト等の逐語記録、計測値） | **ART** |
| 要求・契約・カタログ・解析結果の中身 | **ART** |
| ノード間の接続・trace・status・workflow・findings | **AGN** |

手順:

1. `docs/99.sdt/README.md` の判別表で ART / AGN を決める（**A02 の「3 点セット」は要求モデルの配置ルールであり、
   観測記録の配置ルールではない**。適用範囲外へ流用しない）
2. 置き場を `sdt_layout.resolve` で解決する。物理パスを推測で作らない
3. **契約へ宣言を追加する**。未宣言の新種は `unclassified` = 書けない（deny-by-default）。
   `sdt-layout-contract.json` の `artifacts` と `authoring_policy.rules[]` の両方に宣言が必要
4. 契約は `agn/0.schema/` 配下 = `human` / `source` / `hil_gate: true`。
   **Agent は draft 提案までで、家系の新設確定は HIL 承認**（AUTH-R01）
5. `sdt.authoring_resolve` で意図した `write_owner` / `derivation` / `source_rule_id` が返るか確認してから書く
6. `sdt_layout.audit` と `sdt.authoring_validate` が `ok=true` / `violations=0` を返すことを完了条件とする

❌ 観測記録・計測結果を「登録するもの」と読み替えて AGN へ置く
❌ 判別の正本を読まずに、他ルールの語彙（「AGN 登録」等）から置き場を推論する
❌ 家系の新設を HIL 承認なしに確定させる

### 書き込み主権（Authoring）— どれを触ってよいか


SDT には人間が操作してよいものと、機械生成で触ってはいけないものが混在する。
この区別は README の散文ではなく**スキーマの必須項目**として持つ（Charter P24 / 正本:
`docs/99.sdt/agn/0.schema/authoring-schema-v1.0.json`）。

2 軸で宣言する。1 軸では「消してよいか」が判定できないため。

| `write_owner` × `derivation` | 例 | 触り方 |
|---|---|---|
| `human` / `source` | `roadmap-release-plan.json`、schema、Agent/Skill 定義 | **手で書くのが正しい** |
| `generator` / `derived` | CallGraph、`roadmap-matrix.json`、docgraph、ln-registry | 手編集禁止。**上流 SoT を直して再生成** |
| `agent` / `captured` | Evidence、coverage、soak、findings | **改変も削除も禁止**（再生成不可の監査証跡） |
| `mixed` / `source` | `feature.json`、`task-dd*.json` | フィールド単位。`dd_progress` / `status` は生成器所有 |
| `unclassified` | 未宣言の新種 SDT | **書けない**（deny-by-default）。まず契約へ宣言を追加 |

実効値は**二層解決**で決まる: ノード宣言（override）→ 契約 `authoring_policy.rules[]`（glob /
先に一致したものが勝つ）→ default（`unclassified`）。契約は
`docs/99.sdt/agn/0.schema/sdt-layout-contract.json` の `authoring_policy`。

`sdt.authoring_resolve` は `source_rule_id` を返すので、**なぜその判定なのかを必ず説明できる**。

❌ 生成物を手編集して「直した」と言う（次の再生成で消える）／Evidence を後から書き換える／
`unclassified` のまま書き込む／新種 SDT を契約へ宣言せず追加する


### 概念（SCO）の追加・変更

規律の対象は概念の**数ではなく 1 概念あたりの定義品質**。「SCO 凍結」「概念を増やすな」という統治は
2026/08/01 に廃止した（悪い定義を保存するだけで、宣言と実体が乖離したまま固定化していた）。

ライフサイクル: `draft`（Agent 起案可・**型として使用不可**）→ `proposed`（品質バー機械 PASS）
→ `canonical`（**Human 承認のみ**・SDT ノードの型として使用可）→ `deprecated`

`canonical` 昇格の品質バー（4条件すべて必須）:

| # | 条件 | 機械検査 |
|---|---|---|
| Q1 | `definition` が単独で「何であるか」を説明し、`invariants` を 1 つ以上持つ | ✅ `promotion_bar_unmet` |
| Q2 | `discriminator` に「既存のどの canonical とも、この点で違う」を明記（衝突は merge 候補） | ✅ `promotion_bar_unmet` / `edge_voice_duplicate` |
| Q3 | World Model 十要素のいずれか 1 つに分類される（**WM-1 / P25** — 条文正本: Charter `docs/0.charter/01-development-charter.md`、概念正本: `docs/1.concept/0.world-model/`） | ✅ `world_element_unanchored`（十要素 enum 検証込み） |
| Q4 | 実 SDT/AGN インスタンスまたは具体的な適用予定から参照される見込みがある | ✅ `promotion_bar_unmet`（`evidence` の実測インスタンス件数） |

**Q3 が客観基準である理由**: 「これは真に新しい概念か」は主観的で Agent ごとに答えが揺れる。
十要素（Entity / State / Relation / Constraint / Goal / Intervention / Observation / Reward /
Dynamics / Provenance）への分類可能性は、その問いを**「どの要素か言えるか」という客観判定へ
置き換える**装置である。言えない場合は ①定義が曖昧 ②World Model 側の見直しが必要 の
シグナルとして扱い、`draft` に留めて HIL 裁定へ回す（十要素を安易に増やさない）。


Vertical 差分の吸収は 4 経路のみ: ① 語彙差 = STM 写像（**第一選択**）② 固有値 = STM のフィールド
③ 新概念（普遍）= Core SCO へ `draft` 起案 → Q1-Q4 → HIL ④ 新概念（Vertical 固有）= Domain SCO Package

❌ 語彙差を概念差として SCO へ直書き（まず STM 写像を試す）／SCO に Vertical 固有値を列挙
❌ `draft` / `proposed` の概念を実 SDT ノードの型として使用
❌ `canonical_id` の変更・改名（廃止は `deprecated` 遷移）
❌ Human 承認なしに Agent が `canonical` へ昇格させる
❌ `extends` / `sco_anchor` / `approval` を持たない自作 SCO（シャドーオントロジー）

品質バー Q1-Q4 は `sdt.ontology_validate` が**全 SCO エントリ（concepts / edges / phase_meanings / truths）に対して計測する**。
`summary.sco_*` に lifecycle 内訳・未達バー内訳・十要素分布・`sco_promotion_ready` が出る。
FR anchor と同じ ratchet 形状で、**`proposed` 以上は blocking / `draft` は advisory**（`draft` は rule-026 が
不完全を許すため。全件 blocking にすると初日に約 280 件出てゲート自体が無効化される）。

> 計測されるのは「バーを満たしているか」まで。**`canonical` への昇格は Human のみ（SC-5）** であり、
> `agn/0.schema/**` は `write_owner: human` / `hil_gate: true`（AUTH-R01）。Agent は差分提案に留める。

---

## 3. UI / 画面開発

**適用**: 画面 / Template / Atomic Design component / UI JSON / UI Catalog の変更。

コーディング前に `ui.component_catalog` を dispatch し、UI 部品の SoT の現在状態を確認する。
`semantic_review` の duplicate / `hil_required` / 推奨 canonical target を Evidence に残す。

reusable component は**登録先すべて**に反映する（実パスは `repo-context.json` の `key_paths` と
UI Catalog Feature の JSON を参照。本文にパスを列挙しない）。

- dodo-ui の component 実体
- frontend 側の UI catalog エントリ
- UI Catalog Feature の `ui-components.json`

停止条件:

- Action が無い / schema が取れない場合は、直接編集で進める前に **Operation/Action/Skill の欠落**として扱う
- JSON にあるが frontend catalog に無い component は「登録済み」とみなさない
- catalog にあるが component 実体が無いものは完了扱いしない
- Page-local JSX を reusable UI として扱わない（Atoms/Molecules/Organisms/Templates の適切な階層へ置く）

---

## 4. 運用資産の自己保守

**適用**: Agent / Skill / Operation / CRON catalog が古い・重複している・ゴミが溜まっているとき。

`audit`（重複 / orphan / dangling / draft 放置 / 正本↔catalog 乖離を検出）
→ `gc`（参照ゼロを 2 段階検証 → trash 退避で可逆削除）
→ `reconcile`（登録用 Skill 経由で正規化）

正本: `docs/4.operation/autonomous-execution-loop/01-autonomous-execution-loop.md`
プロセス一覧: `process_catalog.list`

❌ `rm` を使う（**trash 退避**が必須）／catalog の同期更新を省く／CRON レポート MD を新規作成（Charter O9）

---

## 5. ルール自体を変更するとき

このディレクトリの規約は `00-README.md`。ファイルを追加・改名・削除したら、
**同一変更内で** `.clinerules/00-INDEX.md` と `AGENTS.md` を更新する。

| 検査 | 手段 |
|---|---|
| L2 の参照実在・Action 実在・索引整合・事実混入 | `pytest dodo_core/tests/test_clinerules_l2_integrity_l1.py` |
| Charter catalog の drift | `rules.audit` |
| ハードコード混入 | `code.hardcode_audit` |
