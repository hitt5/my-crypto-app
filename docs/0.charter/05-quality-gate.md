# Quality Gate

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## Gate 条件サマリー

| Phase | Gate 条件 |
| --- | --- |
| DD01 完了 | CONTRACT.md + Test Skeleton + Task Graph JSON 存在 + 三者整合性 |
| DD02 完了 | 全テスト PASS + カバレッジ ≥ 80% |
| DD03 完了 | 異常系テスト PASS + テスト失敗 0 件 |
| Feature Complete | L6 ODSV + L7 E2E + L8 PASS |

## Merge Gate

L1 + L3 + L4 + L5 PASS = merge-eligible（DD02 完了と同義）

## Zero Tolerance ルール

- テスト失敗 → 完了報告禁止（P3）
- CONTRACT.md なし → 実装着手禁止（P4）
- タスクグラフ JSON なし → 開発着手禁止（P9）
