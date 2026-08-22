# SDT（Semantic Digital Twin）

## SDT = ART + Governance Graph

| 構成要素 | パス | 内容 |
|---------|------|------|
| **Governance Graph** | `agn/` | タスクグラフ・Evidence・Agent/Skill 定義 — 統治構造 |
| **ART** | `art/` | CallGraph IR・生成された成果物 — 精製物 |

## フォルダ構成

```
99.sdt/
├── README.md          ← このファイル
├── agn/               ← Governance Graph（ハーネス）
│   ├── 0.schema/      ← JSON スキーマ定義
│   ├── 1.workflows/   ← EPIC → Feature → Task Graph
│   ├── 2.agents/      ← Agent 定義
│   └── 3.skills/      ← Skill 定義
└── art/               ← ART（精製物）
    ├── context/       ← CallGraph IR 等
    ├── catalog/       ← ART catalog
    └── operations/    ← Operation catalog / reports
```

## ルール

- JSON ファイルが SoT（P10）
- タスクグラフ JSON なしでの開発着手禁止（P9）
- Evidence は全ての開発行為に必須（A3, P4）
