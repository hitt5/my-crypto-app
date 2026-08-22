# ドキュメントアーキテクチャ

正本: `docs/FOLDER_ARCHITECTURE.md`

## SDT / Governance Graph / ART 概念定義

| 概念 | 略称 | 一言定義 |
|------|------|---------|
| **Semantic Digital Twin** | **SDT** | **SDT = ART + Governance Graph**。プロジェクトの「今の状態」をリアルタイムで追跡・制御するデジタル双子 |
| **Governance Graph** | — | ART をセマンティックに表現したグラフ（ノード・エッジ・状態空間）。Intent → Code → Test → Evidence の因果チェーンを保持 |
| **ARTifact** | **ART** | AI が生成しファイルシステム上に実在する成果物の総称。コード・docs・テスト結果・CONTRACT.md など |

```
SDT Loop: ART → Governance Graph に投影 → drift 検出
Harness Loop: Governance Graph を読む → Agent が実行 → ART 生成 → 書き戻し
```

## JSON First — SoT は JSON ファイル

| 層 | 永続化先 | 内容 |
|---|---|---|
| **Governance Graph 層（JSON）** | `docs/99.sdt/agn/` | タスクグラフ・Evidence・Agent定義 |
| **ART 層** | ファイルシステム | コード・仕様書・テスト・CONTRACT.md |

- ✅ Governance Graph の SoT は `docs/99.sdt/agn/` の JSON ファイルのみ
- ✅ ART はファイルシステム上に実体として存在する

## SoT判定
- **憲法**: `docs/0.charter/` — 開発憲章
- **人間可読 SoT**: `docs/1.concept/` `docs/2.manual/` `docs/4.evaluation/` `docs/98.dodoai-custom-spec/` — 意図・手順・評価・A02 仕様
- **機械可読/機械生成 SoT**: `docs/99.sdt/agn/`（Governance Graph JSON）+ `docs/99.sdt/art/`（成果物）
- **索引のみ**: `docs/3.output/` — 成果物の正本は `docs/99.sdt/art/`。ここへ直接置かない
- **参考（読み取り専用）**: `docs/5.reference/` — 受領資料・テンプレート。SoT として開発しない

## 主要パス
| 用途 | パス |
|------|------|
| 開発憲章 | `docs/0.charter/` |
| コンセプト | `docs/1.concept/` |
| マニュアル（準備・構造化） | `docs/2.manual/` |
| アウトプット索引 | `docs/3.output/` |
| 評価 | `docs/4.evaluation/` |
| 参考資料・テンプレート | `docs/5.reference/` |
| Custom UI / Action 仕様（A02） | `docs/98.dodoai-custom-spec/` |
| SDT | `docs/99.sdt/` |
| Governance Graph JSON | `docs/99.sdt/agn/` |
| ART 成果物 | `docs/99.sdt/art/` |
| BR/SR/EPIC テンプレート | `docs/5.reference/templates/` |
| 用語集テンプレート | `docs/5.reference/templates/EPIC-template-2.system/GLOSSARY.md` |
| Custom Action / UI 実装 | `.dodoai/custom_actions/` `.dodoai/custom_ui/` |

## Context 構造: 横糸（UC）× 縦糸（FR）

`docs/99.sdt/art/context/` の各デプロイメント単位は **横糸 × 縦糸** の 2 軸で構成される。

| 軸 | フォルダ | 成果物 | 内容 |
|---|---|---|---|
| **横糸** | `usecase/` | UC（Use Case） | CallGraph 接続型。entry_point → call_chain → Code files |
| **縦糸** | `external-design/` | FR（Functional Requirement） | API仕様・入出力・受入基準 |

```
{deploy-unit}/
├── usecase/                ← 横糸（UC: CallGraph接続型）
│   └── usecase-catalog.md
└── external-design/        ← 縦糸（FR: 外部設計・機能要件）
    └── fr-catalog.md
```

❌ PROHIBITED: FR を `usecase/` に配置する
❌ PROHIBITED: UC を `external-design/` に配置する
