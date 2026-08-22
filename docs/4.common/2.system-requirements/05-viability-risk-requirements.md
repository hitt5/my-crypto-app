---
type: common-requirement
title: SR-VIA — 生存原理・リスク統制要件（Viability & Risk Discipline）
tags: [common, system-requirement, viability, risk, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-1（生存制約下の資産統治）/ BR-3（安全な実行パイプライン） |
| 入力正本 | CR-5・CR-9（[`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)）/ [`00-overview.md`](../../1.concept/00-overview.md)（大原則） |

# SR-VIA — 生存原理・リスク統制要件

全 EPIC / Feature / Agent / Gate は大原則 — **生存制約下での幾何平均成長と Optionality 最大化**（`max E[Δlog W + αΔΩ + βIG] s.t. P(ruin) < ε`）— に従属する。リスクは価格変動ではなく**不可逆性**（将来の意思決定能力の喪失）を第一軸として管理する。

## 1. 生存制約（Viability — CR-9 由来）

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| SR-VIA-1 | HARD | **Ruin 確率の上限管理**: 生存制約（ε・総損失限度・最低流動性準備率・不可逆性エクスポージャ上限）はユーザーが HIL で数値定義し、全実行候補はこの制約で決定論的に検査される。生存制約を毀損する介入は期待収益に関わらず不実行 | 生存制約の数値定義が存在し、Viability Gate の検査ログが全実行候補に付随。逸脱実行 = 0 |
| SR-VIA-2 | HARD | **不可逆性の最小化**: 全 Execution は不可逆性レベル（可逆 / 条件付き可逆 / 不可逆）を持つ。不可逆な Action（資金ロック・権限付与・Bridge・理解不能 Contract の呼び出し）は自律度に関わらず HIL 必須 | 不可逆性レベルなしの Execution = 0。不可逆 Action の HIL 承認付随率 = 100% |
| SR-VIA-3 | HARD | **分布思考**: World Model・Opportunity 評価は単一予測値を使わず、確率分布 × 損益分布 × 不可逆性（Convexity）で表現する | 単一点推定のみで登録された予測ノード = 0 |
| SR-VIA-4 | HARD | **不確実性ベースのサイジング**: 資金量は確信度ではなく不確実性で制限する（Fractional Kelly 的サイジング）。分布の不確実性が大きいほどサイズを縮小する | Sizing Gate の検査ログに不確実性入力が付随 |
| SR-VIA-5 | HARD | **因果分散**: 分散は Token の数ではなく因果の異なりで測る。同一の Stablecoin 発行体・Bridge・Oracle・担保に依存する Position は合算して上限管理する | 因果依存（発行体・担保・Bridge・Oracle）が Asset に明示され、合算上限検査が実施される |
| SR-VIA-6 | SOFT | **Constraint Alpha**: Constraint Graph（誰が・いつ・なぜ動かざるを得ないか）を観測対象の一級市民とし、他者の強制行動の予測を価格予測より優先する | ConstraintNode の観測・的中実績が記録される |
| SR-VIA-7 | SOFT | **Reflexivity 監視**: 同一予測・同一 Policy の混雑度（CrowdingSignal）を観測し、自戦略が混雑側にいる場合は再評価を強制する | 混雑判定時に該当 Opportunity / Position の再評価が発火する |
| SR-VIA-8 | SOFT | **Optionality の蓄積**: 介入の評価に ΔΩ（資本・流動性・知識・権限・Protocol access の増減）と IG（情報利得）を含め、観測可能なプロキシで実測追跡する | OptionalitySet の実測記録が定期的に残る（LLM 自己申告値の記載 = 0） |

## 2. リスク統制（Risk Discipline — CR-5 由来）

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| SR-VIA-9 | HARD | デフォルトは「何もしない」。No-action との Counterfactual 比較で優位を示せない介入は不実行とする（優位性がコストの 3 倍未満 / Source 信頼度不足 / 流動性不足 / 相関過大 / 収益源が説明不能 → 不実行） | 全実行候補に Counterfactual 比較の記録が付随。基準未達の実行 = 0 |
| SR-VIA-10 | HARD | 回転数上限（1日取引回数・月間売買代金・ガス予算・スリッページ予算・再実行間隔）を全戦略に適用する | 回転数 Gate の上限超過実行 = 0 |
| SR-VIA-11 | HARD | 新戦略は Canary 段階（バックテスト → Paper → 少額 → 制限付き本番 → 増額）以外の経路で本番資金に触れない | Canary 段階を経ない本番投入 = 0 |
| SR-VIA-12 | SOFT | 成果は「Agent 介入による増分利益」（対: BTC 保持・ステーブル保持・不作為ベンチマーク）で測定する。増分利益がベンチマーク未満の戦略は降格 / 停止する | StrategyVersion ごとの増分利益がベンチマーク付きで記録される |
| SR-VIA-13 | HARD | Wallet は役割別（Vault / Earn / Explore / Trade）に分離し、損失可能額（RiskBudget）を Wallet・戦略ごとに配分する。全 Wallet の最大想定損失合計は総損失限度以内とする | 役割なし Wallet = 0。RiskBudget 合計の総損失限度超過 = 0 |
| SR-VIA-14 | HARD | Guardian の RiskSignal 発火時は **新規取引停止 → 権限停止 → Approval 解除 → 退避案 → 人間緊急承認** のフローを最優先で実行する。発火中の新規取引は全停止する | 停止フローの順序・実行証跡が Evidence に残る。発火中の新規取引受理 = 0 |
| SR-VIA-15 | HARD | RiskSignal の発火条件は決定論的な閾値として定義する。閾値の緩和は HIL のみとする（Agent 単独の緩和禁止） | 閾値変更の承認者記録が 100% 人間 |

## 禁止事項（HARD）

- 生存制約を毀損する介入の実行（SR-VIA-1）
- 不可逆 Action の HIL なし実行（SR-VIA-2）
- 単一点推定による評価・登録（SR-VIA-3）
- Counterfactual 比較なしの実行（SR-VIA-9）
- Canary を経ない本番資金投入（SR-VIA-11)
- Agent 単独での RiskSignal 閾値緩和（SR-VIA-15）

## トレーサビリティ

| 上位 | 本 SR | 関連 |
|---|---|---|
| BR-1 / CR-9.1〜9.8 | SR-VIA-1〜8 | SR-POL（Gate 実行面）/ SR-EXE-8（不可逆性検査） |
| BR-1, BR-3 / CR-5.1〜5.7 | SR-VIA-9〜15 | SR-EVD（増分利益・校正の記録）/ NFR-SEC（RiskSignal 監視対象） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-9（生存原理）と CR-5（リスク統制）を検証可能な SR-VIA-1〜15 へ展開 |
