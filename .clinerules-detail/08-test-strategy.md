# テスト戦略

正本: `docs/0.charter/06-test-strategy.md`
Iteration正本: `docs/0.charter/04-iteration-protocol.md`

## ART と Governance Graph の分離原則

| 分類 | 実体 | テストでの例 |
|-----|------|------------|
| **ART（精製物）** | Agent が書く成果物 | テストコード（`.py` / `.ts`）、Skeleton ファイル |
| **Governance Graph（ハーネス）** | テスト実行を制御する統治構造 | `test-cases.json`、`evidence-dd*.json`、Skill/Action 定義 |

## Zero Tolerance
- テスト失敗 → 完了報告禁止
- カバレッジ ≥ 80% 必須
- L5 Harness型テスト必須（pytest+httpx / vitest+fetch）

## DD × L マトリクス v3.0（テスト配置）

| Phase | FE テスト | BE テスト | 横断 |
|-------|----------|----------|------|
| **DD01** | L2(skeleton) | L5(skeleton) | JSON整合性 |
| **DD02** | L1 + L2 | L3 + L4 + L5 | — |
| **DD03** | L1(err) + L2(err) | L3(err) + L5(err) | — |
| **Feature Complete** | L7 + L8 | L7 | L6(ログ/trace) |

## 8層テスト

### Per-IUC テスト（DD01〜DD03）
- **L1(PT-FE)**: 純粋ロジックUT — vitest
- **L2(ITa-FE)**: UIワークフローBDD — vitest + RTL
- **L3(PT-BE)**: ビジネスロジックUT — pytest / vitest
- **L4(ITb)**: 契約・スキーマ検証（静的 + 動的）
- **L5(ITa-Harness)**: 実サーバー+HTTP（BE の主軸テスト）

### Feature Complete テスト（全IUC DD03完了後）
- **L6(IT-ODSV)**: 分散トレース/ログ検証
- **L7(E2E)**: ヘッドレスブラウザ Playwright E2E
- **L8(Visual/AI/Human)**: L8a Headed + L8b AI + L8c Human Review

## Merge Gate
L1 + L3 + L4 + L5 PASS = merge-eligible（DD02 完了と同義）

## ファイル命名
L1: `l1_*.test.ts` / L2: `l2_*.bdd.test.ts` / L3: `l3_*.test.ts` / L5: `l5_*.system.test.ts`
L6: `l6_*.odsv.test.ts` / L7: `l7_*.e2e.test.ts` / L8: `l8_*.visual.test.ts`
