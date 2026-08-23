---
type: charter
title: 要件アーキテクチャ地図 — World Model から Evidence までの接続
description: World Model / Core Concept / Strategy / 共通BR・SR / 縦糸EPIC-Feature-UC / 横糸CAP-FR-MOD-DFR / Code / SQ・AC / Evidence の接続関係と、どの層に何を書いてよいかの所有者境界
tags: [charter, requirements-model, architecture, navigation, entropy]
timestamp: 2026-08-02T00:00:00Z
---

# 要件アーキテクチャ地図 — World Model から Evidence まで

| Key | Value |
| --- | --- |
| Version | 1.1.0 |
| Created | 2026/08/02 |
| Status | Approved |
| 種別 | **接続の正本**（各層の内容は定義しない） |
| 条項の正本 | `01-development-charter.md` |

## 0. この文書の規律 — A クラス宣言（HARD RULE）

本書が単独所有するのは **層と層の接続**だけである。

| 書く | 書かない |
| --- | --- |
| 層の名前と、その層が答える**問い** | 層の内容の要約・再掲 |
| **正本のパス** | 十要素・6 エンジン・5 種エントロピー・BR 本文・CAP/FR 一覧 |
| 接続の**向き**とその意味 | 件数（カタログと MCP が所有する） |
| 書いてよい層（**所有者境界**） | 実装状況 |

> ⚠️ **本書と各層の正本が矛盾した場合、正本が勝つ。** 本書を修正する。
>
> この規律は経験則ではない。前身ツリーでは World Model 十要素を各層が自前で再掲した結果
> **正本と 4/10 が食い違い**、それが SCO `canonical` 昇格の品質バーとして使われていた。
> 「分かりやすくするため要約を足す」は $H_{semantic}$ の典型的な増大経路である
> （`05-entropy-governance.md` §0）。**本書は要約ではなく索引である。**

---

## 1. 全体の鎖

```text
════════════════════════════════════════════════════════════════════════════
 WHY — なぜ作るか（変わりにくい / 1.concept/）
════════════════════════════════════════════════════════════════════════════

  0.world-model/          「世界をどう表現し、どう遷移し、何を報酬とするか」＝ 数理
    │                       三層 SDT → World Model → Agent
    │                       S_{t+1} = f(S_t, I_t, O_t)
    │                       ※ 定義は各正本が単独所有。本書は再掲しない
    │
    ▼  「その数理を実現するシステムはどうあるべきか」
  1.core-concept/         アーキテクチャ命題（不変条件・意味づけ・危険）
    │
    ▼  「どこへ向け、何が順序を決めるか」
  2.strategy/             到達点と形成則

════════════════════════════════════════════════════════════════════════════
 WHAT MUST HOLD — 共通制約（全社 1 セット / 2.common/）
════════════════════════════════════════════════════════════════════════════

  1.business-requirements/   BR — 事業として満たすべきこと
  2.system-requirements/     SR / NFR — 全社共通のシステム制約・アーキテクチャ

    │                                              │
    │ BR が EPIC を根拠づける                        │ NFR が UC の受入基準を制約する
    ▼                                              ▼

════════════════════════════════════════════════════════════════════════════
 WHAT TO BUILD — 直交する 2 本の糸（3.system/）
════════════════════════════════════════════════════════════════════════════

  縦糸 Stakeholder Value              横糸 System Capability
  1.epic/                             2.capability/
  ───────────────────────             ───────────────────────
  EPIC                                Capability
    └ Feature（UC の束・成果物）          └ owns → FR
        └ UC（WHAT・Designed Truth）          └ realized_by → Module（コード境界）
            └ 受入基準                             └ defines → DFR
                 │                                      │
                 └──── references(satisfies) ──────────▶│
                                                        ▼
════════════════════════════════════════════════════════════════════════════
 WHAT IS TRUE — 実装事実（99.sdt/art/）
════════════════════════════════════════════════════════════════════════════
                                                      Code
                                                        │
                                                        ▼  CallGraph 抽出
                                       SQ（単一 Module）/ AC（Module 横断）
                                              = Implemented Truth
                                                        │
                                                        ▼
                                                    Evidence

  ┌──────────────────────────────────────────────────────────────────────┐
  │ UC（Designed Truth）  ⟷  SQ / AC（Implemented Truth）                  │
  │        この照合がドリフト検出の基盤である。両者を同一視しない。            │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. 層ごとの「問い」と正本の所在

**内容ではなく所在の表である。** 定義を知りたいときは必ず正本を開く。

| # | 層 | 答える問い | 正本 |
| --- | --- | --- | --- |
| 1 | World Model / Viability Model | 世界をどう表現し、何を守り増やすか | `docs/1.concept/00-overview.md` + `docs/2.sdt-design/02-data-model.md` |
| 2 | Core Concept | そのシステムはどうあるべきか | `docs/1.concept/02-why-dodoai.md` + `docs/1.concept/03-approach.md` |
| 3 | Strategy | どこへ向け、何が順序を決めるか | `docs/3.strategy/README.md` |
| 4 | 共通 BR | 事業として何を満たすか | `docs/4.common/1.business-requirements/` |
| 5 | 共通 SR / NFR | 横断システム制約は何か | `docs/4.common/2.system-requirements/`（`nfr/`） |
| 6 | 要件モデル | 6 概念の所有関係はどうなっているか | dodoAI reference repository の `ADF/docs/ja/5.document/2.system-requirements/09-requirements-model.md` |
| 7 | 縦糸 EPIC/Feature/UC | 誰が何をできるか（Designed Truth） | `docs/98.dodoai-custom-spec/{FEATURE_ID}/` + `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/{FEATURE_ID}/` |
| 8 | 横糸 CAP/FR/MOD/DFR | システムは何ができるか | `docs/4.common/3.capability-requirements/` + 初期化後の catalog |
| 9 | 実装事実 SQ/AC | 実際に何が動いているか（Implemented Truth） | 初期化後の `docs/99.sdt/art/context/`（CallGraph 由来・生成物） |
| 10 | Evidence | それを何が裏づけるか | `docs/99.sdt/art/test-results/` + schema 宣言後の Evidence family |
| 11 | 運用 | どう回すか | project-local Operation catalog は未初期化。Core の live state を観測し、推測 runbook を作らない |
| 12 | LOOP（閉ループ統治） | どの閉ループが存在し、各フェーズを誰が所有するか | `docs/1.concept/03-approach.md` §LOOP Catalog（命題）+ 初期化後の `docs/99.sdt/agn/4.loops/loops.json`（catalog） |

### 2.1 機械可読カタログ（件数・ID の SoT）

**件数・ID 一覧を MD に書かない。** 常に以下から取得する。

| 対象 | カタログ |
| --- | --- |
| EPIC | `docs/99.sdt/art/catalog/source/epic-catalog/epic-catalog.json` |
| Capability（`attributes.fr_ids` に所有 FR） | `docs/99.sdt/art/catalog/source/capability-catalog/capability-catalog.json` |
| Strategy | `docs/99.sdt/art/catalog/source/strategy-catalog/strategy-catalog.json` |
| Charter 条項 | `charter-catalog.json`（`rules.charter_sync` が生成） |
| LOOP（AGN 第一級・閉ループ統治） | `docs/99.sdt/agn/4.loops/loops.json`（schema `docs/99.sdt/agn/0.schema/loop-schema-v1.json` + MD view `docs/99.sdt/agn/4.loops/index.md`） |

上記 catalog が未生成なら件数を推測せず、`F-WORKSPACE-BOOTSTRAP` の blocker とする。

---

## 3. なぜ縦糸と横糸は直交するのか

**Capability と Feature は N:N** である。

```text
        F-A        F-B        F-C          ← 縦糸: ステークホルダーに見える成果物
         │          │          │
    ┌────┼────┬─────┼────┬─────┼────┐
    │    │    │     │    │     │    │
  CAP-1     CAP-2        CAP-3            ← 横糸: 複数 Feature を支える安定した能力
```

- 1 つの **Capability** は複数 Feature を支える。だから Feature ごとに CAP を作るのは定義の逆である。
- 1 つの **Feature** は複数 CAP を使う。だから Feature が FR を所有することはできない。

この N:N を 1 つのフォルダに畳むと、どちらの軸で管理しているのか判別不能になる。
したがって `1.epic/` と `2.capability/` は**物理的に分離**されている。
**1 つのフォルダに UC と FR を混載しない。**

### 3.1 Designed Truth と Implemented Truth

| | Designed Truth | Implemented Truth |
| --- | --- | --- |
| 何 | **UC** | **SQ**（単一 Module）/ **AC**（Module 横断） |
| 出自 | 人が設計する（WHAT） | CallGraph から機械抽出する |
| canonical | `C:WorkUnit` | `C:Sequence` / `C:ImplementationActivity` |
| 置き場 | `3.system/1.epic/.../uc.md` | `99.sdt/art/context/` |

**両者を同一視した瞬間にドリフト検出が不可能になる。**
Implemented Truth を `UC-` prefix / `C:WorkUnit` へ投影してはならない（Charter P23 / RV-7）。

### 3.2 同一層内関係 — 縦糸・横糸それぞれの概念データモデル

§1 の鎖と §3 の直交が扱うのは **層をまたぐ関係**（親子・所有）である。これと直交して、**同一層内関係**（`EPIC↔EPIC` / `Feature↔Feature` / `CAP↔CAP` / `FR↔FR` / `MOD↔MOD`）が各層に必要になる。

**縦糸の同一層内関係が縦糸の概念データモデルであり、横糸の同一層内関係が横糸の概念データモデルである。** 層の連鎖だけを持ち同一層内関係を持たない層では、非循環・依存方向・孤立の不変条件が機械検査できず、新設時に「既存のどれと、どこが違うか」を問えないため要素が統治不能に増える。

**これは概念データモデルであって依存グラフではない。** エンティティは「定義 / 関心事軸 / 弁別性」を、関係は「関係名 / 多重度 / 必須・任意 / 理由」を持つ（ADF R8）。また上位層の関係を下位層の観測の畳み込みで生成してはならず、概念関係（設計・belief）と観測事実（fact）は別配列に置く（ADF R9）。この 2 規律は、EPIC 層が「概念データモデル」と宣言されながらエッジ 100% が `depends_on`・エンティティ定義欄が全件空という依存グラフに退化していた実測（ADF §0.1.1）を受けて新設された。

定義規律（R1-R9）・不変条件の型・Fact/Policy 分離は **ADF `5.document/2.system-requirements/09-requirements-model.md` §0.1 が正本**。概念データモデルとしての構成要素は同 `17-conceptual-data-diagram.md` §要件モデル自身への適用 が正本。本書は再掲しない（§0 A クラス宣言）。

| 層 | 同一層内関係の実装（機械可読 SoT） | スキーマ | 人間可読 view |
| --- | --- | --- | --- |
| EPIC | `99.sdt/agn/1.workflows/epic-catalog/epic-relation-graph.json` | `epic-relation-schema-v1.1.json` | `3.system/1.epic/relation-map.md` |
| Feature | `99.sdt/agn/1.workflows/requirements-catalog/feature-relation-graph.json` | `feature-relation-schema-v1.0.json` | 同上 |
| CAP | `99.sdt/agn/1.workflows/capability-catalog/capability-relation-graph.json` | `capability-relation-schema-v1.0.json` | `3.system/2.capability/relation-model.md` |
| FR | 未作成（ADF 5 層化に伴う新設対象） | 未作成 | — |
| MOD | `99.sdt/agn/1.workflows/module-catalog/module-relation-graph.json` | `module-relation-schema-v1.0.json` | `3.system/2.capability/relation-model.md` |

実装済みの 4 層はスキーマ（`99.sdt/agn/0.schema/*-relation-schema-*.json`）に対し検証済みで、`sdt-layout-contract.json` の `artifacts[]` に登録されている。**概念関係と観測事実の分離（R8 / R9）を満たしているのは現時点で EPIC 層（v1.1）と MOD 層（`observed_edges` / `declared_edges`）のみ**であり、Feature 層・CAP 層は未対応、FR 層は未作成である。件数と裁定待ち件数は本書に転記せず各グラフと裁定表から取得する（§0 A クラス）。


**不変条件はすべて `enforcement: advisory`**（各グラフの `invariants[]`）。検証 Action は未実装であり、違反は導出時計算と裁定表に記録されるのみで新設をブロックしない。R7（測れるようになってから強制する）に従い、検証 Action と Evidence が揃うまで `hard_gate` へ昇格させない。**「機械検証済み」と誤認して報告しないこと。**

---

## 4. 所有者境界 — 誰が何を書いてよいか


| 対象 | 新設できるのは | 新設したい場合 |
| --- | --- | --- |
| World Model / Viability Model の定義 | `docs/1.concept/00-overview.md` + `docs/2.sdt-design/02-data-model.md` | 正本を改訂する。**他文書で再掲・再定義しない** |
| アーキテクチャ命題 | `docs/1.concept/02-why-dodoai.md` + `docs/1.concept/03-approach.md` | 同上 |
| 到達点・形成則 | `docs/3.strategy/` | 同上 |
| **BR** | `docs/4.common/1.business-requirements/` のみ | **HIL 裁定**。既存 BR への `traces_to_br` で足りないことを先に示す |
| **SR / NFR** | `docs/4.common/2.system-requirements/` のみ | **HIL 裁定**。Feature 固有の具体は **UC の受入基準**へ降ろす |
| **EPIC** | `epic-catalog.json`（Schema First + HIL 昇格） | 同上 |
| **Capability** | `capability-catalog.json`（Schema First + HIL 昇格） | 同上 |
| **FR** | Capability が所有（`attributes.fr_ids`） | カタログ更新。Feature 側からは宣言できない |
| **LOOP** | `agn/4.loops/loops.json`（Schema First + HIL 昇格） | OODA 4 フェーズ + Improve の所有者を宣言できることが登録条件。FR/UC・変動値は所有させず、`tier` で所属を表さない（`docs/1.concept/03-approach.md` §LOOP Catalog） |
| **Feature** | EPIC catalog + `docs/98.dodoai-custom-spec/{FEATURE_ID}/` + TaskGraph | ✅ owning EPIC / CAP が登録済みの場合だけ追加してよい |
| **UC** | Feature が所有 | ✅ 追加してよい。**受入基準を必ず持たせる** |
| **DFR** | Module が所有 | Module 詳細設計で定義する |
| SQ / AC | **生成のみ**（CallGraph 由来） | 手書き禁止。コードを直して再生成する |

### 4.1 Personal Custom App 境界

本プロジェクトは single-owner / local-first であり、Feature / UC は本人の Custom UI / Action に必要な範囲だけ定義する。

| Agent が起案してよい | HIL なしに起案してはいけない |
| --- | --- |
| **UC**（受入基準つき） | BR / SR / NFR |
| **Feature 候補**（既存 EPIC/CAP への接続案つき） | FR / Capability / EPIC の確定 |
| **`fr_gap`**（既存 CAP に不足する FR の指摘。`proposed_id: null`, `hil_status: "pending"`） | multi-user / public SaaS / hosted custody を前提にする要件 |

起案が要件 SoT になるのは **Human approval 後**である。

---

## 5. 判断フロー — 書きたいことがどの層に落ちるか

```text
                    ┌──────────────────────┐
                    │ 書きたいことがある      │
                    └──────────┬───────────┘
                               ▼
                  ┌────────────────────────┐
                  │ 世界の表現・遷移・報酬の   │──Yes──▶ 0.world-model/ の該当正本を改訂
                  │ 「定義」を変えるのか?      │         （他文書に再掲しない）
                  └────────────┬───────────┘
                               │No
                               ▼
                  ┌────────────────────────┐
                  │ 事業として新しい要求か?    │──Yes──▶ 既存 BR を全件読む
                  └────────────┬───────────┘              │
                               │No                        ├─内包される→ traces_to_br で紐づけ
                               │                          └─本当に無い→ HIL 裁定
                               │                             （自分で BR を作らない）
                               ▼
                  ┌────────────────────────┐
                  │ 全社共通のシステム制約か?  │──Yes──▶ 既存 nfr/ を確認 → HIL 裁定
                  └────────────┬───────────┘         （テーマ固有なら UC 受入基準へ降ろす）
                               │No
                               ▼
                  ┌────────────────────────┐
                  │ 「誰が何をできるか」か?    │──Yes──▶ UC を書く（受入基準必須）
                  └────────────┬───────────┘         UC が増えたら Feature を切る
                               │No                    Feature は既存 EPIC 配下
                               ▼
                  ┌────────────────────────┐
                  │ システムの横断能力か?      │──Yes──▶ CAP の attributes.fr_ids を見る
                  └────────────┬───────────┘              │
                               │No                        ├─実在→ references(satisfies)
                               ▼                          └─無い→ fr_gap（proposed_id: null）
                  ┌────────────────────────┐                    → HIL 裁定
                  │ 実装事実の記録か?          │──Yes──▶ 手書きしない。
                  └────────────────────────┘         コードを直して CallGraph 再生成
```

### 5.1 Feature の切り方

- **要件の単位は Feature（UC の束）**である。
- **入力資料は要件の単位ではない。** PDF 1 本・画像 1 束・研究テーマ 1 つを、そのまま 1 要件セットにしない。
- **1 Feature の主 CAP は 1 つ**を原則とする。所有 CAP が 3 を超えたら Feature 分割の signal。
- Feature 名は**能力**を表す。実装形態（`-UI` `-API` `-BATCH`）を名前にしない。

---

## 6. アンチパターン — 実際に起きた 2 件

**両方とも「正本があるのに、自前で作った / 再掲した」という同一の失敗である。**

### 6.1 BR 新設による連鎖崩壊（dodoAI upstream の実例）

参考資料から抽出した要件候補に対し、テーマ別 BR を新設した。

```text
BR-{THEME}-01..04 を新設
   └─▶ その BR を受ける SR が要る    → SR-{THEME}-01..18 を新設
          └─▶ その SR を実現する FR が要る → FR-{THEME}-* を 13 件新設
                 └─▶ FR を所有する CAP が要る → CAP-{THEME}-* を捏造

結果: 本体の BR / SR / CAP / FR と一切接続できない並行要件体系が出来上がった
```

**起点は BR の新設**である。BR を作らなければ SR も FR も CAP も要らなかった。
正しくは、既存 BR への `traces_to_br` ＋ UC の受入基準 ＋ `fr_gap` の 3 つで表現できた。

### 6.2 正本の再掲による定義ドリフト（前身 concept ツリー）

World Model 十要素を各層が「分かりやすくするため」自前で再掲した。

```text
01-representation.md §3（正本）  ⟷  各層の再掲版
                    └─▶ 4/10 が食い違ったまま運用され、
                        SCO canonical 昇格の品質バー Q3 の判定基準として使われた
```

**再掲した瞬間に 2 つの正本ができる。** 片方は必ず腐る。C/R/A 分類の **A（Anchor）= 参照のみ**が答えである。

---

## 7. 混同しやすい用語の対

**全用語集ではない。** 実際に取り違えが起きた対だけを置く。project-local 用語集は `docs/GLOSSARY.md`、ADF 用語は dodoAI reference repository の `ADF/docs/ja/glossary.md` を正とする。

| 対 | 区別 |
| --- | --- |
| **Intervention** ⇄ **Core Action** | Intervention（$I_t$）は世界モデル層の「世界を変える操作」。Core Action / `action_key` は dodo Core の実装カタログ。**階層が異なる**（正本: `0.world-model/03-action-observation.md` §0） |
| **UC** ⇄ **SQ / AC** | UC = Designed Truth（`C:WorkUnit`）。SQ/AC = Implemented Truth（`C:Sequence` / `C:ImplementationActivity`）。同義語として使わない |
| **SQ** ⇄ **AC** | Module 境界を跨ぐか否かで機械判定。`module_scope: single` / `cross` |
| **Capability** ⇄ **Module** | CAP = 能力境界（標準化の単位）。Module = コード境界（凝集メトリクスの計測単位） |
| **Feature** ⇄ **コードフォルダ** | Feature = UC の束（成果物）。`feature/<name>` というコードフォルダは Module である |
| **FR** ⇄ **DFR** | FR は Capability 所有の横断機能要件。DFR は Module 所有の詳細機能要件（親 FR を参照） |
| **SDT** ⇄ **World Model** | SDT は時間を持たない状態表現。World Model は時間発展を学習する。競合概念ではない |

---

## 8. 配置早見表

| 対象 | project-local 配置 | 規律 |
| --- | --- | --- |
| World Model / Core Concept | `docs/1.concept/` + `docs/2.sdt-design/` | Concept と SDT design の責務を混ぜない |
| Strategy | `docs/3.strategy/` | 実装順・優先度を所有 |
| 共通 BR | `docs/4.common/1.business-requirements/` | HIL 裁定 |
| 共通 SR / NFR | `docs/4.common/2.system-requirements/` | HIL 裁定 |
| Feature / UC | `docs/98.dodoai-custom-spec/{FEATURE_ID}/` + catalog | owning EPIC/CAP を先に解決 |
| CAP / FR / MOD / DFR | `docs/4.common/3.capability-requirements/` + catalog | Feature 側は `fr_gap` まで |
| Task Graph | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/{FEATURE_ID}/` | `sdt_layout.resolve` が使えるようになった後は解決結果を正とする |
| Evidence | `docs/99.sdt/art/test-results/{FEATURE_ID}/` + schema 宣言済み family | 実行していない証跡を作らない |
| 生成物（CallGraph 等） | `docs/99.sdt/art/` | 手編集しない |
| Custom UI / Action の A02 仕様 | `docs/98.dodoai-custom-spec/{FEATURE_ID}/` | personal scope を既定とする |

> ❌ **`docs/99.sdt/art/` へ要件・手書き仕様を置かない。** `art/` は Action が生成する成果物専用であり、
> `art/context/` の `usecase/` `external-design/` は CallGraph 由来の投影であって要件定義ではない。

---

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 1.1.0 | 2026/08/22 | LOOP 層を追加 — 閉ループ統治を AGN 第一級 catalog（`agn/4.loops/loops.json`）として §2 / §2.1 / §4 に接続。命題の project-local 正本は `docs/1.concept/03-approach.md` §LOOP Catalog（dodoAI reference §4.3 の HIL 裁定を投影） |
| 1.0.0 | 2026/08/02 | 初版。World Model 〜 Evidence の接続、所有者境界、判断フロー、アンチパターン 2 件を確定 |
