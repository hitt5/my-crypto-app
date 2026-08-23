---
type: common-requirement
title: NFR-SCOPE — パーソナル Custom App スコープ非機能要件（Personal Custom App Scope）
tags: [common, nfr, personal-scope, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-7（パーソナル Custom App としての最適化） |
| 入力正本 | CR-8（[`../../0.common-requirements/00-common-requirements.md`](../../0.common-requirements/00-common-requirements.md)）/ AGENTS.md §Personal Custom App Policy（HARD） |

# NFR-SCOPE — パーソナル Custom App スコープ非機能要件

本システムは **single-owner / local-first のパーソナル dodo Custom App** を既定形とする。汎用の暗号資産 SaaS・不特定多数向けサービスを既定形にしない。

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| NFR-SCOPE-1 | HARD | プロダクト形態は dodoAI 上の Personal Custom UI + Personal Custom Action とし、personal scope（`.dodoai/personal/custom_ui/` / `.dodoai/personal/custom_actions/`）に実装する。A02 仕様は `docs/98.dodoai-custom-spec/` に置く | 実装物の配置が personal scope に限定されている |
| NFR-SCOPE-2 | HARD | 一次利用者・資産所有者・最終承認者はユーザー本人とする。Multi-Agent は本人の意思決定を補助する内部ロールであり、複数顧客・組織・多数決を前提にしない | 承認フローの承認者がユーザー本人に限定されている |
| NFR-SCOPE-3 | HARD | データ境界は local-first とする。個人の Portfolio / Policy / Wallet / Evidence に最適化するが、秘密鍵・シード・個人実値を repository、fixture、SDT、ログへ保存しない（SR-KEY-1 / SR-KEY-2 と対） | リポジトリ・SDT・fixture の走査で個人実値 = 0 |
| NFR-SCOPE-4 | HARD | multi-user、public SaaS、hosted custody、顧客アカウント、組織承認、第三者向け商用化への拡張は既定スコープ外とする。着手前に HIL を行い、Concept と A02 要件セットを先に更新する | スコープ外機能の実装 = 0。拡張時は HIL 記録＋Concept 更新が先行 |
| NFR-SCOPE-5 | HARD | 共通化は本人の Custom App の保守性・再利用性に必要な範囲に留める。「将来売るかもしれない」を理由に multi-tenant / enterprise 機能を先行実装しない | multi-tenant / enterprise 前提の実装 = 0 |

## スコープ境界（正本）

| 区分 | 内容 |
|---|---|
| **In scope** | 本人の Portfolio / Policy / Wallet / Evidence の統合管理、本人向け Custom UI / Custom Action、本人承認フロー、local-first データ、CR-1 の鍵二層統治 |
| **Out of scope（既定）** | multi-user、public SaaS、hosted custody、顧客アカウント、組織承認、Strategy Marketplace、第三者向け商用化 |
| **拡張条件** | Out of scope へ広げる前に HIL → Concept（00-overview.md §Product Form / CR-8）→ A02 要件セットの順に更新する |

## トレーサビリティ

| 上位 | 本 NFR | 関連 |
|---|---|---|
| BR-7 / CR-8.1〜8.5 | NFR-SCOPE-1〜5 | SR-KEY（個人実値の非保存）/ NFR-REG（自己勘定範囲）/ AGENTS.md §Personal Custom App Policy |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-8 を検証可能な NFR-SCOPE-1〜5 へ展開。スコープ境界表を正本化 |
