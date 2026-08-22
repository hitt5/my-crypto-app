# 用語集 — my-crypto-app Glossary

> **TODO: プロジェクトの用語を定義してください**

## 1. 開発プロセス用語

| 用語 | 定義 |
|------|------|
| **DD01** | 契約 + テスト設計 + タスクグラフ定義（三位一体） |
| **DD02** | 実装（全テストが通るまで） |
| **DD03** | 異常系テスト強化 |
| **Feature Complete** | 全 IUC の DD03 完了後の Feature 横断検証（L6 + L7 + L8） |
| **CONTRACT.md** | 型定義・インターフェース宣言のみを含む設計契約文書 |
| **HANDOFF** | タスク引き継ぎドキュメント（MASTER + STREAM パターン） |
| **Gate** | Phase 間の遷移条件。全テスト PASS + Coverage ≥ 80% 等 |
| **Evidence** | 開発行為の証跡。テスト結果・レビュー結果等 |
| **Finding** | 失敗・逸脱の記録。Draft への差し戻しフィードバック |

## 2. アーキテクチャ用語

| 用語 | 定義 |
|------|------|
| **SDT** | Semantic Digital Twin = ART + Governance Graph |
| **ART** | ARTifact — Agent が生成する精製物（コード・仕様書・テスト等） |
| **Governance Graph** | タスクグラフ・Evidence・Agent 定義で構成される統治構造 |
| **EPIC** | 能力（Capability）単位の最上位分類 |
| **Feature** | EPIC 配下の機能単位 |
| **IUC** | Implementation Use Case — 実装の WHAT |
| **UC** | Use Case — 実装の HOW（CallGraph 接続型） |
| **FR** | Functional Requirement — 機能要件 |
| **SR** | System Requirement — システム要件 |
| **BR** | Business Requirement — ビジネス要件 |

## 3. テスト用語

| 用語 | 定義 |
|------|------|
| **L1** | Pure Test (FE) — 純粋ロジック UT |
| **L2** | Integration Test a (FE) — UI ワークフロー |
| **L3** | Pure Test (BE) — ビジネスロジック UT |
| **L4** | Integration Test b — 契約・スキーマ検証 |
| **L5** | Integration Test a (BE) — 実サーバー + HTTP |
| **L6** | ODSV — 分散トレース / ログ検証 |
| **L7** | E2E — ヘッドレスブラウザ |
| **L8** | Visual / AI / Human — ビジュアルリグレッション |
