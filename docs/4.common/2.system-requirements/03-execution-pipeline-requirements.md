---
type: common-requirement
title: SR-EXE — 実行パイプライン要件（Execution Safety）
tags: [common, system-requirement, execution, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-3（安全な実行パイプライン） |
| 入力正本 | CR-3（[`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)） |

# SR-EXE — 実行パイプライン要件（Execution Safety）

全ての執行は次の固定パイプラインを通過する。**省略・順序変更を禁止する。**

```text
許可済み Adapter → トランザクションデコード → 複数価格ソース照合
→ fork 環境シミュレーション → Policy 検査 → 署名 → 執行 → Observation 記録
```

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法) |
|---|---|---|---|
| SR-EXE-1 | HARD | 任意 calldata の生成・署名を禁止する。実行は許可済み Adapter 経由のみとする | Adapter 外経路からの署名要求受理 = 0（SR-KEY-6 と対） |
| SR-EXE-2 | HARD | 未検証コントラクトの呼び出しを禁止する。呼び出し先は Allowlist 登録済みコントラクトのみとする | Allowlist 外コントラクト呼び出し = 0 |
| SR-EXE-3 | HARD | 単一価格オラクルでの判断を禁止する。価格は複数ソースの照合を必須とする | 単一ソース判断による Execution = 0 |
| SR-EXE-4 | HARD | 署名前の fork 環境シミュレーションを必須とする。シミュレーション未通過のトランザクションは署名に進めない | シミュレーション証跡なしの署名 = 0 |
| SR-EXE-5 | HARD | 全 Execution は署名前にトランザクションデコード（何をするかの機械可読な解読）を通過し、デコード結果が Policy 検査の入力になる | デコード結果なしの Policy 検査 = 0 |
| SR-EXE-6 | HARD | 執行結果（Observation）は Execution（Intervention）と必ず対で記録する（WM-4） | Observation なしの Execution ノード = 0 |
| SR-EXE-7 | SOFT | シミュレーションと実行結果の乖離は Finding として記録し、乖離パターンを Adapter / シミュレーション環境の改善入力とする | 乖離検知時に Finding が起票される |
| SR-EXE-8 | HARD | Execution は不可逆性レベル（可逆 / 条件付き可逆 / 不可逆）の検査を通過する。不可逆な Action（資金ロック・権限付与・Bridge・理解不能 Contract）は自律度に関わらず HIL 必須とする | 不可逆 Action の HIL 承認付随率 = 100%（SR-VIA-2 と対） |

## 禁止事項（HARD）

- パイプラインの省略・順序変更（本 SR 冒頭）
- 任意 calldata の生成・署名（SR-EXE-1）
- Allowlist 外コントラクトの呼び出し（SR-EXE-2）
- 単一オラクル判断（SR-EXE-3）
- シミュレーション未通過の署名（SR-EXE-4）

## トレーサビリティ

| 上位 | 本 SR | 関連 |
|---|---|---|
| BR-3 / CR-3.1〜3.4 | SR-EXE-1〜8 | SR-KEY（署名境界）/ SR-POL（Policy 検査）/ SR-EVD（Observation 記録）/ SR-VIA（不可逆性検査） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-3 を検証可能な SR-EXE-1〜8 へ展開（不可逆性検査 SR-EXE-8 は CR-9.2 由来） |
