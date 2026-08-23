---
type: concept
title: 実装優先度の定義（判定基準・優先度マトリクス・実装キュー）
tags: [crypto-wealth-os, strategy, priority, implementation-order, adf, epic, cap]
---

# 01 — 実装優先度の定義（Implementation Priority）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: [`README.md`](README.md)（3.strategy 索引）配下の**実装優先度の正本**。概念的な実装順（不可逆性の低い順①〜⑪）は [`../1.concept/03-approach.md`](../1.concept/03-approach.md) が所有し、本書はそれを**決定論的に再適用可能な判定基準**と**Feature 単位の優先度キュー**へ具体化する。
> **ADF パス（HARD）**: 本書の優先度は **ADF 要件アーキテクチャの上に載る** — 縦糸 `BR → SR → UC` / 横糸 `CAP ─owns→ FR`。**EPIC / CAP / FR の正本カタログは [`../4.common/3.capability-requirements/00-capability-requirements.md`](../4.common/3.capability-requirements/00-capability-requirements.md)（JSON-first: AGN catalog ノード `task-epic-catalog-crypto-wealth-os` / `task-cap-catalog-crypto-wealth-os` — 2026-08-22 `agn.node_upsert` 登録済み）**。EPIC / CAP に接続されていない Feature を本書のキューへ入れてはならない（A02 Step 0）。
> **追随関係**: [`../2.sdt-design/01-development-roadmap.md`](../2.sdt-design/01-development-roadmap.md)（設計 view）は本書へ追随する。EPIC / CAP 単位の優先度・成熟ロードマップは [`02-epic-cap-priority-roadmap.md`](02-epic-cap-priority-roadmap.md) が所有する。矛盾したら 03-approach → 本書 → 02（EPIC/CAP 順）→ roadmap の順を正とし、解消できなければ HIL。

## 0. ADF パス（要件アーキテクチャとの接続）

```text
Concept（1.concept 00〜07）
  → CR（4.common/0.common-requirements — CR-1〜9 正本）
    → BR（4.common/1.business-requirements — BR-1〜7）
      → SR / NFR（4.common/2.system-requirements）
        → EPIC（縦糸・価値のまとまり）─ 所属 → Feature ─ A02 → UC
        → CAP（横糸・FR の所有者）───── owns ──→ FR ──→ Mod（実装）
```

- **EPIC 6 / CAP 8 / FR 35 の定義と根拠**: [`../4.common/3.capability-requirements/00-capability-requirements.md`](../4.common/3.capability-requirements/00-capability-requirements.md)（`impl_provenance` = dodoAI 本体実装参照 Index を含む）
- Feature は FR を新設できない（`satisfies` 参照のみ）。欠落 FR は `fr_gap` として記録し HIL へ
- `impl_provenance = dodoai-core` の CAP/FR（例: CAP-KEY-CUSTODY = dodo-wallet）は**本体側の実装を参照するのみ**であり、本書の優先度では「統合作業のみ」として扱う

## 1. 優先度判定基準（5軸スコアリング）

優先度は「期待収益」ではなく、大原則 `max E[Δlog W + αΔΩ + βIG] s.t. P(ruin) < ε`（[`../1.concept/00-overview.md`](../1.concept/00-overview.md)）から導出する。各 Feature を次の 5 軸で評価する:

| 軸 | 問い | スコア基準（高いほど優先） | 由来 |
|---|---|---|---|
| **A. 不可逆性の低さ** | 失敗しても資本・鍵・権利を失わないか | 3=読み取り専用（観測のみ）/ 2=提案生成（実行なし）/ 1=承認つき実行 / 0=自律実行 | 03-approach 実装順原理・CR-9.2 |
| **B. 基盤依存度（他 Feature を解放するか）** | これが無いと後続が始められないか | 3=全 Feature の前提 / 2=複数 Feature の前提 / 1=単一系列の前提 / 0=末端 | H-1 Survival Premium（行動可能性の保有） |
| **C. IG（情報利得・校正への寄与）** | World Model / Viability Model の校正を早く始められるか | 3=校正ループそのものを回す / 2=校正データを蓄積する / 1=間接的 / 0=寄与なし | 大原則 βIG・07 §3.1（Calibration が最重要差別化） |
| **D. リスク回避α / 生存への寄与** | ruin 距離・不可逆損失の回避に効くか | 3=Guardian/生存制約そのもの / 2=DRIFTED・リスク検知 / 1=間接的 / 0=収益のみ | CR-9.1・crypto.md（リスク回避α = 非常に高い） |
| **E. Agent 適性（オペレーショナルα）** | 人間が継続できない反復作業を肩代わりするか | 3=24h 巡回・期限管理等の反復 / 2=定期評価 / 1=単発分析 / 0=価格予測 | crypto.md 勝ち筋表（価格予測α = 低い） |

**合成規則（決定論的）**:

1. **A（不可逆性）はハード制約**: A の低い Feature を A の高い Feature より先に着手しない（スコア合計での逆転を禁止）。Stage 昇格（Observe→Approve→Autopilot）は CR-2.5 の HIL 承認が必須で、スコアで代替できない
2. A が同値の Feature 間は **B → D → C → E** の辞書式順で優先する（基盤 → 生存 → 校正 → 運用効率）
3. 価格予測αを主収益源とする Feature（E=0）は、他の全 Feature が Canary 実績を持つまでキューに入れない（07 §2）
4. **EPIC / CAP 未接続の Feature はスコアリング対象外**（A02 Step 0 を先に満たす）

## 2. Feature 優先度マトリクス（ADF トレーサビリティ付き）

roadmap の Feature 系列（[`../2.sdt-design/01-development-roadmap.md`](../2.sdt-design/01-development-roadmap.md) §2）へ 5 軸を適用し、EPIC / CAP / BR への接続を明示した結果:

| Feature | EPIC | 主要 CAP（利用 FR） | satisfies | A | B | C | D | E | 優先度 | 根拠（要旨） |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| `F-WORKSPACE-BOOTSTRAP` | FOUNDATION | —（開発基盤） | — | 3 | 3 | 1 | 1 | 1 | **P0** | catalog / roadmap SoT 未初期化は全 Feature の共通負債。開発そのものを解放する |
| `F-CRYPTO-PORTFOLIO-DASHBOARD` | VIABILITY | ONCHAIN-OBSERVE（FR-OBS-1/2）, VIABILITY-EVAL（FR-VIA-3）, EVIDENCE-LEDGER | BR-1, BR-7 | 3 | 3 | 2 | 2 | 2 | **P0** | W・Ω の Fact 化は全評価の土台（着手済 — 完了させる） |
| `F-VIABILITY-POLICY-CORE` | VIABILITY | VIABILITY-EVAL（FR-VIA-1/2/4）, POLICY-ENGINE（FR-POL-1/2/3）, EVIDENCE-LEDGER | BR-1, BR-7 | 3 | 3 | 2 | 3 | 1 | **P0** | ε・Policy・RiskBudget の正本なしに「守るもの」が定義できない。DRIFTED 検知の前提 |
| `F-WORLD-MODEL-OBSERVE` | WORLD-MODEL | ONCHAIN-OBSERVE（FR-OBS-3/4/5）, RISK-DETECT（FR-RSK-3）, EVIDENCE-LEDGER | BR-4 | 3 | 2 | 3 | 2 | 3 | **P1** | 境界変数・Constraint Graph の観測開始が W.M. 校正期間の起点。観測開始が遅れるほど IG 蓄積が遅れる |
| `F-OPPORTUNITY-ENGINE` | OPPORTUNITY | OPPORTUNITY-GEN（FR-OPP-1〜4）, VIABILITY-EVAL（FR-VIA-5）, EVIDENCE-LEDGER（FR-EVD-2） | BR-1, BR-4 | 2 | 2 | 3 | 1 | 2 | **P1** | W.M.×V.M. 差分からの機会生成 + Convexity 評価。校正ループ（予測→実績→forecast error）を初めて閉じる |
| `F-GUARDIAN-RISKSIGNAL` | GUARDIAN | RISK-DETECT（FR-RSK-1/2/4）, ONCHAIN-OBSERVE, POLICY-ENGINE（FR-POL-4） | BR-3, BR-6 | 2 | 1 | 1 | 3 | 3 | **P1** | リスク回避αは「非常に高い」。ただし検知対象（Position・正本）が P0 に依存 |
| `F-AIRDROP-CLAIM-TRACKER` | OPPORTUNITY | OPPORTUNITY-GEN（FR-OPP-5）, EVIDENCE-LEDGER | BR-4 | 2 | 0 | 2 | 1 | 3 | **P2** | オペレーショナルα高。Opportunity Engine の評価枠組みに乗せる（単独先行しない） |
| `F-YIELD-COMPARE` | OPPORTUNITY | OPPORTUNITY-GEN（FR-OPP-2/4）, EVIDENCE-LEDGER | BR-4 | 2 | 0 | 2 | 1 | 2 | **P2** | 期待純収益比較は Convexity 評価器（P1）が前提。表面 APY 比較の禁止を評価器側で担保 |
| `F-EXECUTION-APPROVE` | SETTLEMENT | EXEC-PIPELINE（FR-EXE-1〜4）, KEY-CUSTODY（FR-KEY-1〜3 = **dodoai-core 統合のみ**）, POLICY-ENGINE | BR-2, BR-3, BR-5 | 1 | 1 | 2 | 2 | 1 | **P3** | Stage 2 昇格。**H4 + Stage 昇格 HIL（CR-2.5）+ dodo-wallet 統合**が前提。スコアに関わらず P0〜P2 の校正実績なしに着手しない |
| ⑧〜⑪ 限定自律〜トレーディング | SETTLEMENT | （後日 A02 — EPIC/CAP 接続を先行） | — | 0 | 0 | 1 | 0 | 0〜1 | **P4（凍結）** | Canary Gate 経由でのみ。方向性トレーディングは E=0 のため最後尾固定 |

> CAP 列は主要な利用 FR のみ表記。全対応は [`../4.common/3.capability-requirements/00-capability-requirements.md`](../4.common/3.capability-requirements/00-capability-requirements.md) §4 のマトリクスが正本。

## 3. 優先度付き実装キュー（P0 → P3）

### P0 — 基盤（今すぐ・並行可）

| 順 | 作業 | 完了条件 | Gate |
|---|---|---|---|
| P0-1 | `F-CRYPTO-PORTFOLIO-DASHBOARD` 完了 | portfolio.json 実値設定（HIL）→ live dispatch → `custom_ui.manifest_lint` error 0 → Issue close | Completion Gate（P20） |
| P0-2 | `F-WORKSPACE-BOOTSTRAP` 解消 | catalog / roadmap SoT 初期化・標準 WF カタログ生成（**EPIC/CAP/FR catalog は 2026-08-22 初期化済** — 残: roadmap SoT・標準 WF） | roadmap.sync_gate ok |
| P0-3 | H1 再承認（Concept v0.5） | HIL 承認記録 | HIL |
| P0-4 | `F-VIABILITY-POLICY-CORE` A02 → DD03 | ε・Policy・Wallet 役割・RiskBudget・Ω 棚卸しの機械検査可能な正本 + DRIFTED 表示（FR-VIA-1〜4 / FR-POL-1〜3 に接続） | H2（正本値の HIL 確定） |

### P1 — 観測・評価ループの開通（P0 完了後）

| 順 | 作業 | 完了条件 | Gate |
|---|---|---|---|
| P1-1 | `F-WORLD-MODEL-OBSERVE` | 観測容易な境界変数から観測 Action 群 + 観測ページ。Source 信頼度階層の実装（FR-OBS-3/4/5） | H1 前提 |
| P1-2 | `F-OPPORTUNITY-ENGINE` | 差分生成・Convexity 評価・No-action Counterfactual・`derives_from` 必須（FR-OPP-1〜4）。評価成果物は SDT+MD 双対（FR-EVD-5） | P0-4・P1-1 |
| P1-3 | `F-GUARDIAN-RISKSIGNAL` | 決定論的閾値の RiskSignal 検知・不可逆性レベル付与・通知（FR-RSK-1/2、実行系接続なし） | P0-4・P1-1 |

> P1-2 と P1-3 は P1-1 の観測基盤が動き次第、並行着手可。

### P2 — ドメイン適用（P1 の評価枠組みが前提）

| 順 | 作業 | 完了条件 | Gate |
|---|---|---|---|
| P2-1 | `F-AIRDROP-CLAIM-TRACKER` | Eligibility 構造化・期限管理・Claim 検知（FR-OPP-5、実行なし・Sybil 禁止） | P1-2 |
| P2-2 | `F-YIELD-COMPARE` | 期待純収益（コスト込み）比較。表面 APY 単独比較の機械的拒否（FR-OPP-2/4） | P1-2 |

### P3 — 実行系（Stage 2 昇格 — HIL 必須）

| 順 | 作業 | 完了条件 | Gate |
|---|---|---|---|
| P3-1 | `F-EXECUTION-APPROVE` | CR-3 固定パイプライン + 15 Gate + HIL 全件承認（FR-EXE-1〜4 / FR-POL-4）+ dodo-wallet / Session Key 統合（FR-KEY-1〜3 = **本体側実装の統合のみ・再実装禁止**） | **H4 + Stage 昇格 HIL（CR-2.5）** |

### P4 — 凍結（再裁定なしに着手禁止）

⑧限定自律・⑨リバランス/DCA 自律・⑩LP/Borrow/デルタニュートラル・⑪方向性トレーディング。着手には本書の優先度再裁定（HIL）+ Canary Gate 実績 + Stage 3 昇格 HIL + **所属 EPIC-SETTLEMENT 配下での A02（EPIC/CAP 接続）** を要する。

## 4. 優先度の見直し条件（トリガ）

次のいずれかを観測したら、本書の優先度を再評価する（変更は HIL）:

| トリガ | 再評価対象 |
|---|---|
| H1 / H2 の HIL で Concept・正本値が変わった | 全 Feature |
| **EPIC / CAP / FR カタログが HIL で改訂された** | 該当 CAP を利用する全 Feature |
| Guardian 相当の重大 RiskSignal を手動運用中に検知した | `F-GUARDIAN-RISKSIGNAL` の P1→P0 昇格 |
| P1 の校正データ蓄積が計画より著しく遅い | P2 の着手前倒し可否（IG 軸の再評価） |
| 競合再評価（07 §6.4 四半期クロール）で前提が崩れた | ポジショニング依存の Feature |
| 規制動向（CR-7.4）が実行系の前提を変えた | P3 以降 |
| dodoAI 本体側の core_ref 対象（dodo-wallet 等）の状況が変わった | `impl_provenance = dodoai-core` の FR を使う Feature |

## 5. 本書が禁止する優先度判断

- スコア合計による A 軸（不可逆性）逆転 — 「期待収益が大きいから実行系を先に」は禁止
- **EPIC / CAP 未接続の Feature をキューに入れること**（A02 Step 0 違反）
- **CAP を経由しない FR の新設**（FR は CAP が所有。Feature は `satisfies` 参照のみ）
- `impl_provenance = dodoai-core` の機能をカスタム再実装する Feature の起票（還流課題として本体へ）
- 「Swap 実行」「Yield 最適化」単体を主価値とする Feature の新設（07 §6.1）
- Stage 昇格の HIL を優先度判断で代替すること（CR-2.5）
- 本書と roadmap の片側のみ更新（双方同一変更で追随）

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.0 | 2026-08-22 | **ADF パス接続（HIL 裁定）**: §0 に要件アーキテクチャ（BR→SR→UC / CAP─owns→FR）との接続を新設。優先度マトリクスへ EPIC / CAP(FR) / satisfies 列を追加。EPIC/CAP 未接続 Feature のキュー投入・CAP 非経由の FR 新設・dodoai-core 再実装を禁止事項へ追加。カタログ改訂・core_ref 変化を見直しトリガへ追加 |
| v0.1.0 | 2026-08-22 | 新設。5軸スコアリング基準（不可逆性ハード制約 + 辞書式順）・Feature 優先度マトリクス・P0〜P4 実装キュー・見直しトリガ・禁止事項を定義 |
