# dodo Crypto Wealth OS — ドキュメント構成・手順書

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22

## 構成

```text
docs/
  GLOSSARY.md  用語集（略語・ドメイン用語の定義集）
  0.charter/   憲章  1.concept/  コンセプト   2.manual/   手順
  2.sdt-design/ 設計 view（開発ロードマップ・本体/カスタム分担）
  3.common/    共通要件（BR / SR / NFR）      4.evaluation/ 評価
  5.reference/ 参考資料
  98.dodoai-custom-spec/  Custom UI/Action 仕様
  99.sdt/      SDT = ART + AGN
```

## 索引

> 最初にルート [`README.md`](../README.md) §1.1 で**プロジェクトタイプ**を選んでから、以下を上から順に埋める。

| # | ドキュメント | 状態 |
|---|---|---|
| — | [GLOSSARY.md（用語集）](GLOSSARY.md) | ✅ 参照 view（正本は各定義元） |
| — | [2.sdt-design/01-development-roadmap.md（開発ロードマップ・本体/カスタム分担）](2.sdt-design/01-development-roadmap.md) | ✅ 設計 view（実装順の正本は 1.concept/03） |
| — | [1.concept/README.md（コンセプト設計標準）](1.concept/README.md) | 標準（正本） |
| 1 | [1.concept/00-overview.md](1.concept/00-overview.md) | ✅ 記入済（v0.5 根本改訂・H1 再承認待ち） |
| 2 | [2.manual/00-overview.md](2.manual/00-overview.md) | ⬜ |
| 3 | [3.output/00-overview.md](3.output/00-overview.md) | ⬜ |
| 4 | [4.evaluation/00-overview.md](4.evaluation/00-overview.md) | ⬜ |

### 1.concept の必須構成（[設計標準](1.concept/README.md)に従う）

| # | ファイル | 状態 |
|---|---|---|
| 00 | [00-overview.md](1.concept/00-overview.md) | ✅ |
| 01 | [01-problem.md](1.concept/01-problem.md) | ✅ |
| 02 | [02-why-dodoai.md](1.concept/02-why-dodoai.md) | ✅ |
| 03 | [03-approach.md](1.concept/03-approach.md) | ✅ |
| 04 | [04-data-model.md](1.concept/04-data-model.md) ⭐最重要 | ✅ |
| 05 | [05-multi-agent.md](1.concept/05-multi-agent.md) | ✅ |
| 06 | [06-common-requirements.md](1.concept/06-common-requirements.md)（共通要件 Common・追加） | ✅ |
| 07 | [07-why-not-simple.md](1.concept/07-why-not-simple.md)（単純な自動運用アプリではダメな理由・競合分析・追加） | ✅ |

> インプット正本: [5.reference/crypto.md](5.reference/crypto.md)

### 3.common の構成（共通要件 — [索引](3.common/README.md)）

| # | ファイル | 状態 |
|---|---|---|
| — | [3.common/README.md（索引・CR 対応マトリクス）](3.common/README.md) | ✅ |
| BR | [1.business-requirements/01-business-background-goals.md](3.common/1.business-requirements/01-business-background-goals.md) / [02-business-requirement.md](3.common/1.business-requirements/02-business-requirement.md)（BR-1〜7） | ✅ |
| SR | [01-key-custody](3.common/2.system-requirements/01-key-custody-requirements.md) / [02-policy-governance](3.common/2.system-requirements/02-policy-governance-requirements.md) / [03-execution-pipeline](3.common/2.system-requirements/03-execution-pipeline-requirements.md) / [04-evidence](3.common/2.system-requirements/04-evidence-requirements.md) / [05-viability-risk](3.common/2.system-requirements/05-viability-risk-requirements.md) | ✅ |
| NFR | [01-nfr-security](3.common/2.system-requirements/nfr/01-nfr-security.md) / [02-nfr-regulatory](3.common/2.system-requirements/nfr/02-nfr-regulatory.md) / [03-nfr-personal-scope](3.common/2.system-requirements/nfr/03-nfr-personal-scope.md) | ✅ |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.8.0 | 2026-08-22 | 2.sdt-design/01-development-roadmap.md（Concept 実装順の Feature 写像 + DODO 本体/カスタム分担）を新設し索引へ追加 |
| v0.7.0 | 2026-08-22 | docs 直下に GLOSSARY.md（用語集: 要件略語・コンセプト固有概念・データモデルノード型・crypto ドメイン用語・統治固有語）を新設し索引へ追加 |
| v0.6.0 | 2026-08-22 | 3.common/（共通要件層）を新設: CR-1〜CR-9 を dodoAI `docs/2.common/` と同型の BR（1〜7）/ SR（KEY・POL・EXE・EVD・VIA）/ NFR（SEC・REG・SCOPE）へ展開 |
| v0.5.0 | 2026-08-22 | 1.concept 根本改訂を反映: 大原則（生存制約下での幾何平均成長 + Optionality 最大化）・三要素アーキテクチャ・4仮説・CR-9 生存原理を導入（00〜07 改訂、H1 再承認待ち） |
| v0.4.0 | 2026-08-22 | 1.concept/07-why-not-simple.md（競合環境と差別化根拠）を追加 |
| v0.3.0 | 2026-08-22 | Product Form を single-owner / local-first のパーソナル dodo Custom App として確定（H0 承認） |
| v0.2.0 | 2026-08-22 | 1.concept 00〜06 記入完了を反映（H1 承認待ち）。テーマ名を確定 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
