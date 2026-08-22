# ハーネストレーサビリティ

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Template |

---

## トレーサビリティチェーン

```
Intent → Feature → IUC → UC → Code → Test → Evidence → Finding
```

全てのステップがタスクグラフ上で表現され、因果チェーンとして辿ることができる。

## Evidence（証跡）

全ての開発行為は Evidence を生成する。

| フィールド | 説明 |
|-----------|------|
| evidence_type | `verification_verdict` / `test_result` / `review_outcome` |
| truth_type | `verified` / `observed` / `improvement` |
| status | `success` / `failure` / `partial` |

## Finding（発見事項）

失敗・逸脱は Finding として記録し、Draft への差し戻しフィードバックループを回す。

## ART と Governance Graph の分離

| 分類 | 例 |
|------|---|
| **ART（精製物）** | コード、テストコード、CONTRACT.md、仕様書 |
| **Governance Graph（ハーネス）** | タスクグラフ JSON、Evidence JSON、Agent/Skill 定義 |
