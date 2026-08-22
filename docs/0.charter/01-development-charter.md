# 開発憲章 — my-crypto-app Development Charter

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Updated | YYYY/MM/DD |
| Status | Draft |
| SoT | 本ドキュメント |

> **本ドキュメントは my-crypto-app の全バージョンに共通する「開発の憲法」である。**
> Agent は開発セッション開始時に必ずこのファイルを最初に読むこと。

---

## 0. 最上位原則: 人間は設計し、Agent が自律実行する

my-crypto-app の開発は **完全自動化** を前提とする。人間が仕様（Draft）を策定・承認（Approved）し、Agent がタスクグラフを読み解き、DD01→DD02→DD03 の Iteration を自律的に回す。

```
人間: Draft → Approve（仕様確定）
                ↓
Agent: タスクグラフ読解 → 自律実行（DD01/DD02/DD03）
                ↓
Evidence: 結果を記録 → Gate 判定 → 次の Iteration
```

### 自律実行の 5 原則

| # | 原則 | 意味 |
| --- | --- | --- |
| A1 | **タスクグラフが入口** | Agent は構造化データから タスクを読み解く |
| A2 | **Harness が制御** | 全ての Agent 実行は Harness 経由 |
| A3 | **Evidence で閉じる** | 全ての開発行為は Evidence を記録して完結する |
| A4 | **Gate で進む** | Phase 間の遷移は Quality Gate 条件を満たした場合のみ |
| A5 | **Finding で戻る** | 失敗・逸脱は Finding として記録し、フィードバックループを回す |

---

## 1. 根本原則

### 1.1 開発プロセスの 7 原則

| # | Principle | 意味 |
| --- | --- | --- |
| P1 | **Harness first** | 全 Agent 実行は Harness を通る |
| P2 | **Twin as state** | タスクグラフは可視化ではなく状態空間 |
| P3 | **Runtime replaceable** | 特定 Runtime に固定しない（Codex / Claude Code / Copilot / Cline） |
| P4 | **Evidence by default** | 実行・判断・検証は最初から Evidence |
| P5 | **Human override** | 人間は停止・承認・修正・差し戻しが可能 |
| P6 | **Temporal through Harness** | CRON / Scheduler は Harness の入口 |
| P7 | **Sovereign depth** | セキュリティ境界の深度を制御 |

### 1.2 完全自律 Iteration — DD01 → DD02 → DD03 → Feature Complete

```
Feature 仕様確定（BR → FR → SR → IUC）
  │
  ├── A02: 全体設計
  │     ↓
  ├── IUC-A: DD01 → DD02 → DD03 ──┐
  ├── IUC-B: DD01 → DD02 → DD03 ──┤
  └── IUC-C: DD01 → DD02 → DD03 ──┤
                                    │
               全 IUC の DD03 完了 ←┘
                      │
               Feature Complete（L6 + L7 + L8）
```

### DD × L マトリクス

| Phase | 主責務 | FE テスト | BE テスト | Gate |
|-------|--------|----------|----------|------|
| **DD01** | 契約+テスト設計+タスクグラフ | L2(skeleton) | L5(skeleton) | 三者整合性 |
| **DD02** | 実装 | L1 + L2 | L3 + L4 + L5 | Coverage ≥ 80% + 全PASS |
| **DD03** | 異常系 | L1(err) + L2(err) | L3(err) + L5(err) | 0 failures |
| **Feature Complete** | Feature横断 | L7 + L8 | L7 | E2E + ODSV PASS |

---

## 2. プロダクト構成

> **TODO: プロジェクトの EPIC 構成・デプロイメント単位を定義してください**

### 2.1 EPIC 構成

| EPIC | Name | 責務 | 技術スタック |
| --- | --- | --- | --- |
| EPIC-SEMANTIC-DIGITAL-TWIN | {Name} | {責務} | {Stack} |

### 2.2 デプロイメント単位

| デプロイメント単位 | 開発対象 | 技術スタック |
| --- | --- | --- |
| **backend/** | バックエンド API | {Stack} |
| **frontend/** | フロントエンド | {Stack} |

---

## 3. UC 定義方式 — CallGraph 接続型

UC（Use Case）は IUC（WHAT）を **HOW** に変換する。各 UC は「どのモジュールの、どの関数/API を、どの順序で呼ぶか」を **CallGraph** として定義する。

```
Intent → EPIC → Feature → IUC (WHAT)
                             ↓
                          UC (HOW: CallGraph 接続型)
                             ↓
                          entry_point → call_chain → Code files
```

---

## 4. 禁止事項

| # | 禁止事項 | 理由 |
| --- | --- | --- |
| P1 | Git 操作（commit / push / merge） | 原則ユーザーが実行。例外は専用 Harness のみ |
| P2 | Mock data へのフォールバック | DD02 以降は実機結合必須 |
| P3 | テスト失敗状態での完了報告 | Zero Tolerance |
| P4 | CONTRACT.md なしでの実装着手 | DD01 スキップ禁止 |
| P5 | シークレットのハードコード | env 経由必須 |
| P6 | 同一ツール × 同一引数の 2 回以上呼び出し | ツールコールループ禁止 |
| P7 | Feature / IUC からタスクグラフを直接生成 | UC / FR 単位で分解すること |
| P8 | Charter 未読での開発着手 | 本ファイルを読まずに作業開始しない |
| P9 | タスクグラフ JSON なしでの開発着手 | 存在しなければ作成してから着手 |
| P10 | SDT データの不整合な永続化 | JSON ファイルが SoT |

---

## 5. 品質基準

| 基準 | 閾値 |
| --- | --- |
| テストカバレッジ | ≥ 80% |
| L5 実機テスト | 必須 |
| テスト失敗 | 0 件（Zero Tolerance） |

---

## 6. Agent の起動手順

```
1. docs/0.charter/01-development-charter.md を読む    ← 今ここ
2. docs/0.charter/ の残りのファイルを読む
3. タスクグラフで概況把握
4. 作業対象を特定
5. 仕様ファイルを read_file
6. DD01/DD02/DD03 を Iteration 実行
7. Evidence / テスト結果を記録
```

---

## Related Documents

| Document | Path |
| --- | --- |
| タスクグラフ駆動開発 | [./02-task-graph-driven-development.md](./02-task-graph-driven-development.md) |
| タスクグラフ定義 | [./03-task-graph.md](./03-task-graph.md) |
| Iteration プロトコル | [./04-iteration-protocol.md](./04-iteration-protocol.md) |
| Quality Gate | [./05-quality-gate.md](./05-quality-gate.md) |
| テスト戦略 | [./06-test-strategy.md](./06-test-strategy.md) |
| ハーネストレーサビリティ | [./07-harness-traceability.md](./07-harness-traceability.md) |
| タスクグラフメンテナンス | [./08-task-graph-maintenance.md](./08-task-graph-maintenance.md) |
| Knowledge Graph | [./09-knowledge-graph.md](./09-knowledge-graph.md) |
