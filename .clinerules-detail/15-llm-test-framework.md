# LLM テストフレームワーク（L4-LLM 品質評価ゲート）

> **LLM 機能を含まないプロジェクトではこのルールは無効化可能です。**

## 根本原則

**LLM テストは「正解一致テスト」ではなく「契約テスト」である。**
出力が揺れることを前提に、品質・根拠・安全性・コスト・トレースの契約を検証する。

## L4-LLM 6 サブレイヤー

| サブレイヤー | テスト対象 | 評価器 | Zero Tolerance |
|---|---|---|---|
| **L4-LLM-a** Prompt Contract | 出力形式・必須/禁止語句 | schema + rule + llm_judge | ❌ |
| **L4-LLM-b** Tool Integration | tool 選択・引数 schema | schema + rule | ❌ |
| **L4-LLM-c** RAG Integration | faithfulness / relevancy | ragas + llm_judge | ❌ |
| **L4-LLM-d** Agent Workflow | ループ破綻防止・完了条件 | rule + llm_judge | ❌ |
| **L4-LLM-e** Guardrail | injection / PII / 権限外 | rule + policy_engine | ✅ |
| **L4-LLM-f** Cost & Latency | token / latency / tool回数 | rule | ❌ |

## DD × LLM テスト マトリクス

| Phase | L4-LLM |
|---|---|
| **DD01** | テスト境界定義 JSON 作成 + smoke dataset 設計 |
| **DD02** | a-f 実装 |
| **DD03** | e(guardrail) 強化 |
| **Feature Complete** | 全件回帰 |

## 評価器の使い分け

### Deterministic 評価器を使うべき場合（LLM Judge 禁止）
- JSON Schema 適合性
- Tool call の引数型・名前
- PII 検出 / 権限チェック

### LLM-as-Judge を使うべき場合
- 要約品質 / 回答の関連性 / トーン

❌ PROHIBITED: LLM-as-Judge だけで合否判定

## 合格基準（数値化必須）

```yaml
quality:
  task_success_rate: ">= 0.90"
  schema_valid_rate: ">= 0.99"
security:
  prompt_injection_success_rate: "= 0"
  pii_leakage: "= 0"
ops:
  p95_latency_ms: "<= 15000"
```

## 禁止事項

- ❌ テスト境界定義 JSON なしで LLM テスト実装着手
- ❌ LLM-as-Judge のみで合否判定
- ❌ 品質閾値を定義せずに「テスト通った」と報告
- ❌ Guardrail テストの Zero Tolerance を無効化
