---
type: common-requirement
title: CR — 共通要件正本（Common Requirements CR-1〜CR-9）
tags: [common, requirements, cr, crypto-wealth-os]
---

# 共通要件（Common Requirements）— CR 正本

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 全 EPIC / Feature に横断適用される共通要件（Common）の**正本**。個別機能の要件はここに書かず、各 EPIC の要件定義（BR → SR → UC）で表現する。ここに定義した CR に反する個別要件は無効。
> **展開先**: 本書の CR-1〜CR-9 は同フォルダ配下 [`../1.business-requirements/`](../1.business-requirements/02-business-requirement.md)（BR）/ [`../2.system-requirements/`](../README.md)（SR・NFR）で要件 ID・受入基準・トレーサビリティ付きへ展開されている。CR の追加・変更は HIL 裁定を経て本書で行い、BR / SR / NFR は同一変更で追随する。
> **移動履歴**: 本書は旧 `docs/1.concept/06-common-requirements.md` を正本ごと `3.common/` へ移設したもの（v0.4.0）。Concept 側の各書からの参照は本書を指す。

## CR-1 鍵管理・署名（Key Custody）

**秘密鍵は AI / Agent / サーバーに絶対に渡さない。** 鍵は次の二層で保持・補完する。

| 層 | 役割 | 用途 |
|---|---|---|
| **dodo クレデンシャル機構**（基本） | DID/VC による Agent・承認者の識別、`env://` 参照による資格情報の間接参照、Desktop によるユーザー環境内の署名処理 | 日常的な承認フロー・Session Key の発行/失効・限定権限の署名 |
| **個人ハードウェアモジュール**（補完） | ハードウェアウォレット等、ユーザーが物理保持する署名デバイス | Vault（長期保全）資産の移動、Policy 変更、Safe owner 権限の行使、高額取引の最終署名 |

- CR-1.1 Agent が持てるのは **期限付き・用途限定の実行権限**（Session Key / Safe Module 経由）のみ。生の秘密鍵・シードフレーズをコード・設定・SDT・ログのいずれにも保存しない
- CR-1.2 資格情報の参照は `env://` 等の間接参照のみ（平文直書き禁止）
- CR-1.3 高権限操作（Vault 移動・Policy 変更・権限付与）は個人ハードウェアモジュールの物理署名を必須とする
- CR-1.4 Session Key は必ず失効期限を持ち、緊急停止（Kill Switch）で即時無効化できる

→ 展開先: [SR-KEY](../2.system-requirements/01-key-custody-requirements.md)

## CR-2 権限統治（Policy-Custodied Autonomy）

- CR-2.1 全実行はいずれかの Policy（投資憲法）に拘束される。Policy 非拘束の実行経路を作らない
- CR-2.2 Policy の項目（金額上限・Allowlist・スリッページ・レバレッジ禁止・損失限度・回転数上限・失効期限・承認閾値）は決定論的に検査可能な形式で定義する
- CR-2.3 **Agent 自身に権限上限・Policy を変更させない**（変更は HIL のみ）
- CR-2.4 最終可否は LLM でなく決定論的な Policy Engine が判断する（多数決・確信度ベース禁止）
- CR-2.5 自律度は Observe → Approve → Autopilot の段階のみ。段階昇格は HIL 承認必須

→ 展開先: [SR-POL](../2.system-requirements/02-policy-governance-requirements.md)

## CR-3 実行パイプライン（Execution Safety）

全ての執行は次の固定パイプラインを通過する。省略・順序変更禁止。

```text
許可済み Adapter → トランザクションデコード → 複数価格ソース照合
→ fork 環境シミュレーション → Policy 検査 → 署名 → 執行 → Observation 記録
```

- CR-3.1 任意 calldata の生成・署名を禁止（許可済み Adapter 経由のみ）
- CR-3.2 未検証コントラクトの呼び出しを禁止（Allowlist のみ）
- CR-3.3 単一価格オラクルでの判断を禁止（複数ソース照合必須）
- CR-3.4 署名前の fork シミュレーション必須。シミュレーションと実行結果の乖離は Finding として記録

→ 展開先: [SR-EXE](../2.system-requirements/03-execution-pipeline-requirements.md)

## CR-4 根拠と記録（Evidence by Default）

- CR-4.1 全ての判断・実行・リスク判定は Evidence（Intervention と Observation の対 ＋ Source 参照 ＋ 使用 Agent・モデル・戦略バージョン）を必須とする
- CR-4.2 Evidence Ledger は追記のみ（改変・削除禁止）
- CR-4.3 Fact / Belief / Hypothesis を分離して記録し、SNS 等の低信頼 Source を事実として扱わない
- CR-4.4 税務要件（取得価格・取引理由）を Evidence が兼ねられる形式で記録する

→ 展開先: [SR-EVD](../2.system-requirements/04-evidence-requirements.md)

## CR-5 リスク統制（Risk Discipline）

- CR-5.1 デフォルトは「何もしない」。取引しない理由を先に評価し、No-action との Counterfactual 比較で優位を示せない介入は不実行とする（優位性がコストの 3 倍未満 / Source 信頼度不足 / 流動性不足 / 相関過大 / 収益源が説明不能 → 不実行）
- CR-5.2 回転数上限（1日取引回数・月間売買代金・ガス予算・スリッページ予算・再実行間隔）を全戦略に適用
- CR-5.3 新戦略は Canary 段階（バックテスト → Paper → 少額 → 制限付き本番 → 増額）以外の経路で本番資金に触れない
- CR-5.4 成果は「Agent 介入による増分利益」（対: BTC 保持・ステーブル保持・不作為ベンチマーク）で測定する
- CR-5.5 Wallet は役割別（Vault / Earn / Explore / Trade）に分離し、損失可能額を Wallet・戦略ごとに配分する
- CR-5.6 Guardian の RiskSignal 発火時は 新規取引停止 → 権限停止 → Approval 解除 → 退避案 → 人間緊急承認 のフローを最優先する
- CR-5.7 リスクは価格変動（ボラティリティ）ではなく**不可逆性**（将来の意思決定能力の喪失）を第一軸として管理する（詳細は CR-9）

→ 展開先: [SR-VIA](../2.system-requirements/05-viability-risk-requirements.md)

## CR-6 セキュリティ（Agent Security)

- CR-6.1 プロンプトインジェクション対策: クロール取得コンテンツを命令として解釈しない（データとしてのみ扱う）
- CR-6.2 フロントエンド改ざん・DNS 乗っ取り・不審トークン送付を RiskSignal として監視
- CR-6.3 利用モデル・ツール・外部データ・実行コードを SBOM/MCP 統制で追跡
- CR-6.4 Sybil farming（大量ウォレットによる機械的エアドロップ収穫）を行わない

→ 展開先: [NFR-SEC](../2.system-requirements/nfr/01-nfr-security.md)

## CR-7 規制適合（Regulatory Posture）

- CR-7.1 初期は「ユーザー（自己勘定）が定義したルールの機械的実行を支援するソフトウェア」の範囲に留める
- CR-7.2 実行前承認（Approve 段階）を標準設定とする
- CR-7.3 個別銘柄推奨・有料継続助言・成果報酬・不透明なルーティング報酬に該当し得る機能は HIL 裁定なしに実装しない
- CR-7.4 金融庁の暗号資産制度動向（2026 制度移行期）を観測対象に含める

→ 展開先: [NFR-REG](../2.system-requirements/nfr/02-nfr-regulatory.md)

## CR-8 パーソナル Custom App スコープ（Personal Custom App Scope）

- CR-8.1 本プロダクトは **single-owner / local-first のパーソナル dodo Custom App** を既定形とし、`.dodoai/personal/custom_ui/` + `.dodoai/personal/custom_actions/` の personal scope で本人の資産形成運用を支援する
- CR-8.2 一次利用者・資産所有者・最終承認者はユーザー本人とする。Multi-Agent は本人を補助する内部ロールであり、複数顧客・組織・多数決を前提にしない
- CR-8.3 個人の Portfolio / Policy / Wallet / Evidence に合わせて最適化するが、秘密鍵・シード・個人実値を repository、fixture、SDT、ログへ保存しない
- CR-8.4 multi-user、public SaaS、hosted custody、顧客アカウント、組織承認、第三者向け商用化は既定スコープ外とする。着手前に HIL を行い、Concept と A02 要件セットを更新する
- CR-8.5 共通化は本人の Custom App の保守性・再利用性に必要な範囲に留め、将来の外販だけを理由に multi-tenant / enterprise 機能を先行実装しない

→ 展開先: [NFR-SCOPE](../2.system-requirements/nfr/03-nfr-personal-scope.md)

## CR-9 生存原理（Viability Principle）

全 EPIC / Feature / Agent / Gate は [`../../1.concept/00-overview.md`](../../1.concept/00-overview.md) の大原則 — **生存制約下での幾何平均成長と Optionality 最大化**（`max E[Δlog W + αΔΩ + βIG] s.t. P(ruin) < ε`）— に従属する。

- CR-9.1 **Ruin 確率の上限管理**: ユーザーは生存制約（ε・総損失限度・最低流動性準備率・不可逆性エクスポージャ上限）を HIL で定義し、全実行候補はこの制約を決定論的に検査される。生存制約を毀損する介入は期待収益に関わらず不実行
- CR-9.2 **不可逆性の最小化**: 全 Execution は不可逆性レベル（可逆 / 条件付き可逆 / 不可逆）を持つ。不可逆な Action（資金ロック・権限付与・Bridge・理解不能 Contract の呼び出し）は自律度に関わらず HIL 必須
- CR-9.3 **分布思考**: World Model・Opportunity 評価は単一予測値を使わず、確率分布 × 損益分布 × 不可逆性（Convexity）で表現する
- CR-9.4 **不確実性ベースのサイジング**: 資金量は確信度ではなく不確実性で制限する（Fractional Kelly 的サイジング）。分布の不確実性が大きいほどサイズを縮小する
- CR-9.5 **因果分散**: 分散は Token の数ではなく因果の異なりで測る。同一の Stablecoin 発行体・Bridge・Oracle・担保に依存する Position は合算して上限管理する
- CR-9.6 **Constraint Alpha**: 「誰が・いつ・なぜ動かざるを得ないか」（Constraint Graph）を観測対象の一級市民とし、他者の強制行動の予測を価格予測より優先する
- CR-9.7 **Reflexivity 監視**: 同一予測・同一 Policy の混雑度（CrowdingSignal）を観測し、自戦略が混雑側にいる場合は再評価を強制する
- CR-9.8 **Optionality の蓄積**: 介入の評価に ΔΩ（将来実行可能な Action 集合の増減 — 資本・流動性・知識・権限・Protocol access）と IG（情報利得・予測校正の改善）を含め、実測で追跡する

→ 展開先: [SR-VIA](../2.system-requirements/05-viability-risk-requirements.md)

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.4.0 | 2026-08-22 | **正本移設**: `docs/1.concept/06-common-requirements.md` から `docs/3.common/0.common-requirements/00-common-requirements.md` へ CR 正本を移動（ユーザー HIL）。各 CR に展開先（SR / NFR）リンクを付与 |
| v0.3.1 | 2026-08-22 | `docs/3.common/`（BR / SR / NFR への展開層）を新設し、正本関係（本書 = CR 正本、3.common = 展開）を明記 |
| v0.3.0 | 2026-08-22 | **根本改訂**: CR-9（生存原理 — Ruin 上限管理・不可逆性最小化・分布思考・Fractional Kelly・因果分散・Constraint Alpha・Reflexivity 監視・Optionality 蓄積）を追加。CR-5.1 に Counterfactual 比較、CR-5.7 に不可逆性第一軸を追記 |
| v0.2.0 | 2026-08-22 | ユーザー HIL により CR-8（パーソナル dodo Custom App スコープ）を追加 |
| v0.1.0 | 2026-08-22 | 初版。crypto.md とユーザー指示（秘密鍵 = dodo クレデンシャル機構＋個人ハードウェアモジュールの二層）を元に CR-1〜CR-7 を定義 |
