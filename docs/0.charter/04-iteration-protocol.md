# Iteration プロトコル — A02 → DD01 → DD02 → DD03 → Feature Complete

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## 概要

開発の反復は 3 軸（S: 要件 / A: 設計 / DD: 開発）に準拠する。仕様確定後、A02（全体設計）で設計コンテキストを確立し、IUC 単位で DD01 → DD02 → DD03 の 3 Phase を回す。全 IUC 完了後に Feature Complete で横断検証を実行する。

## DD × L マトリクス

| Phase | 主責務 | FE テスト | BE テスト | Gate |
|-------|--------|----------|----------|------|
| **DD01** | 契約+テスト設計+タスクグラフ | L2(skeleton) | L5(skeleton) | 三者整合性 |
| **DD02** | 実装 | L1 + L2 | L3 + L4 + L5 | Coverage ≥ 80% + 全PASS |
| **DD03** | 異常系 | L1(err) + L2(err) | L3(err) + L5(err) | 0 failures |
| **Feature Complete** | Feature横断 | L7 + L8 | L7 | E2E PASS |

## DD01: 契約 + テスト設計 + タスクグラフ定義（三位一体）

### 成果物

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | CONTRACT.md | 型定義・インターフェース宣言のみ |
| 2 | Test Skeleton | 実行すると SKIP/FAIL になるテスト骨格 |
| 3 | Task Graph JSON | `task-dd01.json`（spec_refs 付き） |

### Gate 条件
- CONTRACT.md + Test Skeleton + Task Graph JSON 存在
- 三者の整合性検証

## DD02: 実装（全テストが通るまで）

- Coverage ≥ 80%
- 全テスト PASS

## DD03: 異常系テスト強化

- テスト失敗 0 件（Zero Tolerance）

## Feature Complete

- L6 ODSV + L7 E2E + L8 Visual PASS
