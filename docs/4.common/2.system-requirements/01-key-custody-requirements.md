---
type: common-requirement
title: SR-KEY — 鍵管理・署名要件（Key Custody）
tags: [common, system-requirement, key-custody, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-2（鍵・権限のソブリニティ） |
| 入力正本 | CR-1（[`../0.common-requirements/00-common-requirements.md`](../0.common-requirements/00-common-requirements.md)） |

# SR-KEY — 鍵管理・署名要件

**秘密鍵は AI / Agent / サーバーに絶対に渡さない。** 鍵は次の二層で保持・補完する。

| 層 | 役割 | 用途 |
|---|---|---|
| **dodo クレデンシャル機構**（基本） | DID/VC による Agent・承認者の識別、`env://` 参照による資格情報の間接参照、Desktop によるユーザー環境内の署名処理 | 日常的な承認フロー・Session Key の発行/失効・限定権限の署名 |
| **個人ハードウェアモジュール**（補完） | ハードウェアウォレット等、ユーザーが物理保持する署名デバイス | Vault（長期保全）資産の移動、Policy 変更、Safe owner 権限の行使、高額取引の最終署名 |

## 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| SR-KEY-1 | HARD | Agent が持てるのは**期限付き・用途限定の実行権限**（Session Key / Safe Module 経由）のみとする。生の秘密鍵・シードフレーズをコード・設定・fixture・SDT・ログ・Evidence のいずれにも保存しない | シークレットスキャン（コミット時）と Evidence 監査で秘密鍵素材の検出件数 = 0 |
| SR-KEY-2 | HARD | 資格情報（RPC キー・API キーを含む）の参照は `env://` 等の間接参照のみとする。平文直書きを禁止する | リポジトリ・設定・manifest の走査で平文資格情報 = 0 |
| SR-KEY-3 | HARD | 高権限操作（Vault 資産移動・Policy 変更・Safe owner 権限行使・権限付与）は個人ハードウェアモジュールの物理署名を必須とする | 高権限操作の Evidence に物理署名の証跡が 100% 付随 |
| SR-KEY-4 | HARD | Session Key は必ず失効期限（expiry）と用途スコープを持ち、緊急停止（Kill Switch）で即時無効化できる | 失効期限なしの Session Key 発行 = 0。Kill Switch 発動から無効化完了までの経路が実測で検証済み |
| SR-KEY-5 | HARD | 署名処理はユーザー環境内（Desktop / ハードウェアモジュール）でのみ行う。鍵素材・署名機能をサーバー・リモート Agent へ移送しない | 署名 API の呼び出し経路監査（local 境界外の署名経路 = 0） |
| SR-KEY-6 | HARD | 任意 calldata への署名を禁止する。署名対象は SR-EXE の固定パイプライン（デコード・シミュレーション・Policy 検査済み）を通過したトランザクションのみとする | パイプライン非通過の署名要求はリジェクトされ Finding として記録される |
| SR-KEY-7 | SOFT | Session Key・Approval の棚卸し（有効な権限の一覧・不要 Approval の検出）を定期実行し、Viability 空間の実態観測に含める | 棚卸し結果が観測記録として残る（放置 Approval は RiskSignal 化） |

## 禁止事項（HARD）

- 秘密鍵・シードフレーズの repository / fixture / SDT / ログ / Evidence への保存（SR-KEY-1）
- 資格情報の平文直書き（SR-KEY-2）
- 鍵素材のメモリ長期保持・サーバー移送（SR-KEY-5）
- 任意 calldata の生成・署名（SR-KEY-6、SR-EXE-1 と対）

## トレーサビリティ

| 上位 | 本 SR | 関連 |
|---|---|---|
| BR-2 / CR-1.1〜1.4 | SR-KEY-1〜7 | SR-EXE（署名前パイプライン）/ SR-POL（権限統治）/ NFR-SEC（Agent Security） |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-1 を検証可能な SR-KEY-1〜7 へ展開 |
