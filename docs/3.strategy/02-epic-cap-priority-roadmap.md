---
type: concept
title: EPIC / CAP 優先度とロードマップ（EPIC 6 / CAP 8 の投資順序）
tags: [crypto-wealth-os, strategy, priority, epic, cap, roadmap, adf]
---

# 02 — EPIC / CAP 優先度とロードマップ

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: [`01-implementation-priority.md`](01-implementation-priority.md)（Feature 単位の優先度正本）の**上位ビュー**として、**EPIC 6 本（縦糸）と CAP 8 本（横糸）そのものの優先度・成熟ロードマップ**を定義する。Feature キューは 01 が正本のまま — 本書は「どの EPIC に価値を積み、どの CAP をどの成熟度まで先に立てるか」を所有する。
> **入力カタログ（JSON-first）**: EPIC / CAP / FR の定義正本 = [`../4.common/3.capability-requirements/00-capability-requirements.md`](../4.common/3.capability-requirements/00-capability-requirements.md)（AGN catalog ノード `task-epic-catalog-crypto-wealth-os` / `task-cap-catalog-crypto-wealth-os`）。EPIC / CAP の新設・変更は HIL 裁定必須 — 本書は優先度のみを所有し定義を変更しない。
> **矛盾時**: 03-approach（不可逆性順）→ 01（Feature 優先度）→ 本書（EPIC/CAP 順）→ roadmap view の順を正とし、解消できなければ HIL。

## 1. EPIC 優先度（縦糸 — 価値のまとまりの投資順序）

EPIC の優先度は、所属 Feature の最高優先度（01 §2）と「その EPIC が守るもの」から導出する:

| 優先 | EPIC | satisfies BR | 所属 Feature（01 の優先度） | 位置づけ | この EPIC が「完了」と言える条件 |
|---|---|---|---|---|---|
| **E-P0** | `EPIC-FOUNDATION` | — | F-WORKSPACE-BOOTSTRAP（P0） | 開発基盤。全 EPIC の共通前提 | catalog / roadmap SoT・標準 WF カタログ初期化。roadmap.sync_gate ok（**EPIC/CAP/FR catalog は 2026-08-22 登録済 — 残: roadmap SoT・標準 WF**） |
| **E-P0** | `EPIC-VIABILITY` | BR-1, BR-7 | DASHBOARD（P0）・VIABILITY-POLICY-CORE（P0） | 「守るもの」の正本。三要素②。**他 EPIC の評価がすべてここに依存** | W・Ω の Fact 化 + ε/Policy/RiskBudget の機械検査可能な正本 + DRIFTED 検知の稼働 |
| **E-P1** | `EPIC-WORLD-MODEL` | BR-4 | WORLD-MODEL-OBSERVE（P1） | 「何が起こるか」の観測。三要素①。IG 蓄積の起点 | 境界変数・ConstraintNode の定期観測 WF が定常運転し、分布更新が Evidence に残る |
| **E-P1** | `EPIC-GUARDIAN` | BR-3, BR-6 | GUARDIAN-RISKSIGNAL（P1） | リスク回避α（最高価値）。Viability と Settlement に交差 | 決定論的 RiskSignal 検知 + 不可逆性レベル付与 + 通知の定常運転（実行系接続は E-P3 と同時） |
| **E-P1〜P2** | `EPIC-OPPORTUNITY` | BR-1, BR-4 | OPPORTUNITY-ENGINE（P1）・AIRDROP（P2）・YIELD（P2） | 差分生成と Convexity 評価。校正ループの中核 | Opportunity 生成→評価→forecast error 追記の校正ループが 1 周以上閉じる |
| **E-P3** | `EPIC-SETTLEMENT` | BR-2, BR-3, BR-5 | EXECUTION-APPROVE（P3）・⑧〜⑪（P4 凍結） | 実行・承認。**Stage 2 昇格 HIL（CR-2.5）+ H4 が入口** | CR-3 固定パイプライン + 15 Gate + dodo-wallet 統合で承認つき実行が Evidence 付きで通る |

**EPIC 間の規律**:

- E-P0 の 2 EPIC は並行可。ただし `EPIC-VIABILITY` の正本値確定（H2）は他のすべての評価系 EPIC の前提
- `EPIC-SETTLEMENT` はスコアや進捗に関わらず、E-P0〜P1 の EPIC が完了条件を満たし校正実績を持つまで着手しない（01 §1 合成規則 1 と同一のハード制約）
- EPIC の完了宣言は Feature の `_done` ではなく、上表の完了条件 + roadmap.sync_gate ok で判定する

## 2. CAP 優先度（横糸 — 能力の成熟ロードマップ）

CAP は「作る/作らない」ではなく**成熟度（Maturity）を段階的に上げる**。M0=未着手 / M1=最小実装（主要 FR の一部） / M2=Observe 完成（実行なし系 FR 全部） / M3=実行系接続（Approve 以降）。

| 優先 | CAP | provenance | 直近で必要とする Feature | 現在→目標 | 優先度根拠 |
|---|---|---|---|---|---|
| **C-P0** | `CAP-ONCHAIN-OBSERVE` | custom | DASHBOARD（P0）→ WORLD-MODEL（P1） | M1（FR-OBS-1/2 実装済相当）→ **M2**（FR-OBS-3/4/5） | すべての Fact の供給源。これが止まると全 EPIC が盲目になる |
| **C-P0** | `CAP-VIABILITY-EVAL` | custom | VIABILITY-CORE（P0）・DASHBOARD（P0） | M0 → **M2**（FR-VIA-1〜4。FR-VIA-5 は Opportunity と同時） | 「守るもの」の機械検査。DRIFTED・ruin 距離は P0 の中核 |
| **C-P0** | `CAP-EVIDENCE-LEDGER` | core+rules | 全 Feature 横断 | M1（本体機構は既存）→ **M2**（FR-EVD-2/4/5 の記録スキーマ） | 校正（IG 測定）の記録面。後から遡って付けられない — 最初から通す |
| **C-P1** | `CAP-POLICY-ENGINE` | core+rules | VIABILITY-CORE（P0）で定義・GUARDIAN（P1）で検査 | M0 → M1（FR-POL-1/2/3）→ M2（FR-POL-4 = 15 Gate 接続） | Policy 定義（P0）と Gate 検査ルール（P1）の 2 段階で立てる |
| **C-P1** | `CAP-RISK-DETECT` | custom | GUARDIAN（P1）・WORLD-MODEL（P1） | M0 → **M2**（FR-RSK-1/2/3。FR-RSK-4 停止フローの実行系接続は M3） | リスク回避αは最高価値だが、検知対象の Fact/正本（C-P0 群）が前提 |
| **C-P1** | `CAP-OPPORTUNITY-GEN` | custom | OPPORTUNITY（P1）→ AIRDROP/YIELD（P2） | M0 → **M2**（FR-OPP-1〜4。FR-OPP-5 は P2 と同時） | 校正ループを閉じる評価器。P2 の 2 Feature はこの CAP の適用面 |
| **C-P3** | `CAP-EXEC-PIPELINE` | core+rules | EXECUTION-APPROVE（P3） | M0 → M3（FR-EXE-1〜4） | 実行系。Stage 2 昇格 HIL より先に作らない |
| **C-P3** | `CAP-KEY-CUSTODY` | **dodoai-core** | EXECUTION-APPROVE（P3） | —（本体側実装の**統合のみ**・再実装禁止） | dodo-wallet + クレデンシャル機構が正本。本プロジェクト側の作業は P3 の統合 FR（FR-KEY-1〜3）のみ |

**CAP 間の規律**:

- C-P0 の 3 CAP（OBSERVE / VIABILITY-EVAL / EVIDENCE-LEDGER）が**最初のクリティカルパス** — P0 Feature はこの 3 つの M2 化と同義
- `impl_provenance = dodoai-core` の CAP（KEY-CUSTODY）は成熟度管理の対象外（本体側 SoT）。本体側の状況変化は 01 §4 の見直しトリガ
- CAP の M3（実行系接続）はすべて Stage 2 昇格 HIL の後。M2 までは Observe 段階で完成させる

## 3. 統合ロードマップ（EPIC × CAP × Feature の時間軸）

```text
        t1 (now)                t2 (next)                 t3 (later)            HIL Gate
        ─────────────────────── ───────────────────────── ───────────────────── ────────
EPIC    FOUNDATION ██████       WORLD-MODEL ██████        SETTLEMENT ██
        VIABILITY  ██████       GUARDIAN    ██████        （⑧〜⑪ 凍結）
                                OPPORTUNITY ████░░ → P2適用
CAP     ONCHAIN-OBSERVE M1→M2   RISK-DETECT M0→M2         EXEC-PIPELINE M0→M3
        VIABILITY-EVAL  M0→M2   OPPORTUNITY-GEN M0→M2     KEY-CUSTODY（統合のみ）
        EVIDENCE-LEDGER M1→M2   POLICY-ENGINE  M1→M2
Feature P0-1 DASHBOARD 完了      P1-1 WORLD-MODEL-OBSERVE  P3-1 EXECUTION-APPROVE
        P0-2 BOOTSTRAP 解消      P1-2 OPPORTUNITY-ENGINE   （P2: AIRDROP / YIELD は
        P0-3 H1 再承認 [HIL]     P1-3 GUARDIAN-RISKSIGNAL    P1-2 完了後 t2 末〜t3）
        P0-4 VIABILITY-CORE [H2]
Gate    roadmap.sync_gate ok    校正ループ 1 周 Evidence    H4 + Stage 昇格 HIL
```

- **t1 → t2 の昇格条件**: P0 キュー（01 §3）全完了 + C-P0 3 CAP の M2 + H1/H2 承認
- **t2 → t3 の昇格条件**: 校正ループ（Opportunity 予測 → 実績 → forecast error）が 1 周以上 Evidence として閉じる + Guardian 定常運転
- **t3 入場条件**: H4 + Stage 昇格 HIL（CR-2.5）。スケジュールで代替不可
- 機械側 view: roadmap SoT（`docs/99.sdt/agn/1.workflows/roadmap/` — generated・手編集禁止）が本書へ追随する。現状 roadmap-matrix は EPIC 0 / CAP 0 で導出されており（catalog 接続前の生成物）、P0-2 の roadmap SoT 再生成で本書の EPIC/CAP 行が反映される（既知負債 — F-WORKSPACE-BOOTSTRAP）

## 4. 見直し条件

01 §4 のトリガをすべて継承する。加えて:

| トリガ | 再評価対象 |
|---|---|
| CAP の成熟度が目標に達しないまま依存 Feature が着手期日を迎えた | 該当 CAP の priority 昇格 or Feature の後ろ倒し（HIL） |
| roadmap SoT 再生成（P0-2）で本書と derived graph が乖離した | 本書 §3 の時間軸（機械導出を正としつつ、優先度原則との矛盾は HIL） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 新設。EPIC 6 の優先度（E-P0〜P3・完了条件付き）、CAP 8 の成熟ロードマップ（M0〜M3・C-P0〜P3）、EPIC×CAP×Feature 統合時間軸（t1/t2/t3 + 昇格条件）を定義。カタログ正本（4.common/3.capability-requirements — JSON-first）に基づく |
