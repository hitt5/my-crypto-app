---
type: common-requirement
title: NFR-SEC — セキュリティ非機能要件（Agent Security）
tags: [common, nfr, security, crypto-wealth-os]
---

| Key | Value |
| --- | --- |
| Version | 0.1.0 |
| Updated | 2026-08-22 |
| 上位要件 | BR-2（鍵・権限のソブリニティ）/ BR-6（敵対的環境での Agent セキュリティ） |
| 入力正本 | CR-6（[`../../0.common-requirements/00-common-requirements.md`](../../0.common-requirements/00-common-requirements.md)）/ [`00-overview.md`](../../../1.concept/00-overview.md) §AI 統治の試金石 |

# NFR-SEC — セキュリティ非機能要件（Agent Security）

## 1. 前提（脅威モデル）

クリプトはゼロトラストが前提の環境である: 取引は不可逆・相手は匿名・コントラクトは敵対的・情報源は汚染済み・失敗は即座に定量化される。**Agent 自身をゼロトラスト対象**とし、LLM が乗っ取られても実害に至らない多層防御を要求する。

| 脅威カテゴリ | 具体的な脅威 | 主たる防御層 |
|---|---|---|
| 入力汚染 | プロンプトインジェクション（クロールコンテンツ・偽ドキュメント・偽 Governance） | NFR-SEC-1（命令非解釈）＋ 決定論的 Gate（SR-POL-4） |
| フロント/インフラ改ざん | フロントエンド改ざん・DNS 乗っ取り・偽サイト | NFR-SEC-2（RiskSignal 監視） |
| 資産直撃 | 不審トークン送付・Approval 悪用・任意 calldata 誘導 | NFR-SEC-2 ＋ SR-KEY / SR-EXE |
| サプライチェーン | 悪意あるモデル・ツール・外部データ・実行コード | NFR-SEC-3（SBOM/MCP 統制） |
| 鍵・権限奪取 | 鍵流出・Session Key 悪用 | SR-KEY（二層構成・失効・Kill Switch） |

## 2. 要件

| ID | 区分 | 要件 | 受入基準（検証方法） |
|---|---|---|---|
| NFR-SEC-1 | HARD | **プロンプトインジェクション対策**: クロール取得コンテンツ（Web・SNS・ドキュメント・オンチェーンメッセージ）を命令として解釈しない。データとしてのみ扱い、システム指示と外部入力を構造的に分離する | 外部コンテンツ由来の命令実行 = 0。敵対的入力の注入テストで Gate 迂回 = 0 |
| NFR-SEC-2 | HARD | フロントエンド改ざん・DNS 乗っ取り・不審トークン送付・Approval 異常を RiskSignal として監視し、検知時は Guardian 停止フロー（SR-VIA-14）に接続する | 各監視項目に決定論的な発火条件が定義され、検知 → 停止フローの経路が検証済み |
| NFR-SEC-3 | HARD | 利用モデル・ツール・外部データ・実行コードを SBOM / MCP 統制で追跡する。SDT スキャン・更新は必ず MCP Action 経由とする（JSON 直読み・直編集禁止） | 依存関係・利用モデルの追跡記録が存在。SDT 直編集 = 0 |
| NFR-SEC-4 | HARD | **Sybil farming**（大量ウォレットによる機械的エアドロップ収穫）を行わない。Airdrop 対応は正規利用の最適化のみとする | Sybil 目的のウォレット大量生成機能 = 0 |
| NFR-SEC-5 | HARD | LLM の出力が直接実行に接続される経路を作らない。全実行は決定論的 Gate（SR-POL / SR-EXE / SR-VIA）を通過する（LLM 汚染 ≠ 実害、の構造保証） | LLM 出力 → 署名の直結経路 = 0 |
| NFR-SEC-6 | SOFT | 攻撃・異常の試行（インジェクション試行・偽情報・Gate リジェクト）は Finding として記録し、Red Agent の反証観点へフィードバックする | 異常試行の Finding 起票が運用記録に残る |

## 3. dodoAI 統治機構との対応（検証マップ）

| dodoAI 機構 | 本テーマでの検証内容 | 対応要件 |
|---|---|---|
| 鍵の分離統治（DID/VC・`env://`・Desktop 署名＋ハードウェア二層） | Agent が鍵に到達できない構造での自律実行 | SR-KEY |
| 決定論的 Policy Engine | LLM 乗っ取り時も実害に至らない多層防御 | SR-POL-4 / NFR-SEC-5 |
| Session Key 失効・Kill Switch | blast radius の限定 | SR-KEY-4 |
| Evidence 追記のみ | 侵害後のフォレンジック可能性 | SR-EVD-2 |
| Guardian 停止フロー | 自動インシデントレスポンス | SR-VIA-14 |
| 入力境界防御・SBOM/MCP 統制 | 敵対的入力に常時晒される Agent の境界 | NFR-SEC-1〜3 |

## トレーサビリティ

| 上位 | 本 NFR | 関連 |
|---|---|---|
| BR-6 / CR-6.1〜6.4 | NFR-SEC-1〜6 | SR-KEY / SR-POL / SR-EXE / SR-VIA / SR-EVD |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 初版。CR-6 を脅威モデル付きの NFR-SEC-1〜6 へ展開。dodoAI 統治機構との検証マップを追加 |
