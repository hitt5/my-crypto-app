# Iteration プロトコル

正本: `docs/0.charter/04-iteration-protocol.md`

## 📍 タスクグラフ & ロードマップ参照

| 文書 | パス | 用途 |
|------|------|------|
| **タスクグラフ定義チャーター** | `docs/0.charter/03-task-graph.md` | ノード型・依存ルール・JSON スキーマ |
| **タスクグラフ JSON 配置先** | `docs/99.sdt/agn/1.workflows/{epic}/` | UC/FR レベルの実行計画 DAG |
| **UC カタログ** | `docs/99.sdt/art/context/{deploy-unit}/usecase/usecase-catalog.md` | UC 定義（タスクグラフの入力元） |

### ❌ タスクグラフ禁止事項（Charter P7 + P9）
- Feature / IUC からタスクグラフを直接生成禁止 — **UC / FR 単位で分解すること**
- dispatch 単位は `uc-task` / `fr-task` のみ
- **タスクグラフ JSON なしでの開発着手禁止（P9）** — 下記「タスクグラフ存在ゲート」参照

## 🚨 タスクグラフ存在ゲート（P9 — HARD GATE）

> **作業指示を受けたら、コード変更・CONTRACT.md 作成の前にタスクグラフの存在を確認する。**
> 存在しなければ**まず作成してから**開発フローに進む。

### 確認手順

```
1. 対象 Feature / UC を特定

2. タスクグラフ JSON の存在確認:
   find docs/99.sdt/agn/1.workflows/ -path "*/{feature-id}/*" -name "task-dd*.json" 2>/dev/null

3a. 存在する場合 → Preload Gate（14-dev-task-preload.md）へ進む

3b. 存在しない場合 → 以下のタスクグラフ作成フローを実行:
    ① UC カタログ確認
    ② FR カタログ確認
    ③ UC/FR 単位で task-dd01.json / task-dd02.json / task-dd03.json を作成
    ④ feature.json を作成（spec_refs 設定）
    → 作成完了後、Preload Gate へ進む
```

## DD × L マトリクス v3.0

```
A02 → DD01 → DD02 → DD03 → Feature Complete
```

| Phase | 主責務 | FE テスト | BE テスト | 横断 | Gate |
|-------|--------|----------|----------|------|------|
| **DD01** | 契約+テスト設計+タスクグラフ | L2(skeleton) | L5(skeleton) | JSON整合性 | 三者整合性 |
| **DD02** | 実装 | L1 + L2 | L3 + L4 + L5 | — | Coverage ≥ 80% + 全PASS |
| **DD03** | 異常系 | L1(err) + L2(err) | L3(err) + L5(err) | — | 0 failures |
| **Feature Complete** | Feature横断 | L7 + L8 | L7 | L6(ログ/trace) | E2E + ODSV PASS |

## A02: 全体設計作成（DD01 の前提）
- コンテキストフロー図、処理フロー・シーケンス図
- 画面一覧 + 画面設計書
- API 定義、データモデル設計
- コンポーネント構造、状態管理設計
- 成果物配置先: `docs/99.sdt/art/context/{deploy-unit}/external-design/`
- ❌ A02 完了前に DD01 着手禁止

## DD01: 契約 + テスト設計 + タスクグラフ定義（三位一体）

DD01 は **Contract + Test Skeleton + Task Graph JSON の三者整合性** を検証するフェーズ。

### DD01 成果物
| # | 成果物 | FE | BE | 内容 |
|---|--------|:--:|:--:|------|
| 1 | CONTRACT.md | ✅ | ✅ | **型定義・インターフェース宣言のみ**。実装コード・仕様転記禁止 |
| 2 | L2 Test Skeleton | ✅ | — | UIワークフロー仕様（SKIP/FAIL） |
| 3 | L5 Test Skeleton | — | ✅ | Harness テスト仕様（SKIP/FAIL） |
| 4 | Task Graph JSON | ✅ | ✅ | `task-dd01.json`（spec_refs 付き） |

> ❌ CONTRACT.md に実装コードを書くことは禁止
> ❌ 仕様書の内容を CONTRACT.md に転記することは禁止

## DD02: 実装（全テストが通るまで）

- FE: L1 + L2 全 PASS
- BE: L3 + L4 + L5 全 PASS
- Coverage ≥ 80%

## DD03: 異常系テスト強化

- FE: L1(err) + L2(err)
- BE: L3(err) + L5(err)
- テスト失敗 0 件（Zero Tolerance）

## Feature Complete（全 IUC の DD03 完了後）

- **L6 ODSV**: 分散トレース/ログ検証
- **L7 E2E**: ヘッドレスブラウザ Playwright E2E
- **L8**: Visual/AI/Human Review

## 絶対ルール
- ❌ DD01 で Test Skeleton なしに DD02 着手禁止
- ❌ DD02 で Mock フォールバック禁止
- ❌ テスト失敗状態で完了報告禁止（Charter P3）
- ❌ L6 を IUC 単位で実行しない（Feature Complete で実行）
- 完了報告にテストファイル名+実行結果を必ず含める
- HANDOFF に `## DD Phase Progress` セクション必須
