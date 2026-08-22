# テスト戦略

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## 8 層テスト

### Per-IUC テスト（DD01〜DD03）

| Layer | 名称 | 対象 | ツール例 |
|-------|------|------|---------|
| L1 | Pure Test (FE) | 純粋ロジック UT | vitest |
| L2 | Integration Test a (FE) | UI ワークフロー | vitest + RTL |
| L3 | Pure Test (BE) | ビジネスロジック UT | pytest / vitest |
| L4 | Integration Test b | 契約・スキーマ検証 | — |
| L5 | Integration Test a (BE) | 実サーバー + HTTP | pytest + httpx / vitest + fetch |

### Feature Complete テスト

| Layer | 名称 | 対象 |
|-------|------|------|
| L6 | ODSV | 分散トレース / ログ検証 |
| L7 | E2E | ヘッドレスブラウザ（Playwright） |
| L8 | Visual / AI / Human | ビジュアルリグレッション |

## 品質基準

| 基準 | 閾値 |
| --- | --- |
| テストカバレッジ | ≥ 80% |
| L5 実機テスト | 必須 |
| テスト失敗 | 0 件 |

## ファイル命名規則

- L1: `l1_*.test.ts` / `test_l1_*.py`
- L2: `l2_*.bdd.test.ts`
- L3: `l3_*.test.ts` / `test_l3_*.py`
- L5: `l5_*.system.test.ts` / `test_l5_*.py`
- L7: `l7_*.e2e.test.ts`
- L8: `l8_*.visual.test.ts`

## 禁止事項

- ❌ テスト失敗状態での完了報告（P3）
- ❌ DD02 での Mock フォールバック（P2）
- ❌ L5 実機テストなしでの DD02 完了宣言
