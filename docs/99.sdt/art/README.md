# ART（ARTifact）— 精製物

Agent が生成しファイルシステム上に実在する成果物を配置する。

## 配置するもの

- `context/callgraph/` — CallGraph IR（コード構造の解析結果）
- `catalog/` — ART catalog
- `operations/` — Operation catalog / reports
- その他の生成された成果物

## ART vs Governance Graph

| 分類 | 例 |
|------|---|
| **ART（ここ）** | CallGraph IR、生成レポート |
| **Governance Graph（`agn/`）** | タスクグラフ JSON、Evidence JSON |
