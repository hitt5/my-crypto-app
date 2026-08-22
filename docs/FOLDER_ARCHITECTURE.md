# ドキュメントフォルダアーキテクチャ — my-crypto-app

| Key | Value |
| --- | --- |
| Version | 3.0.0 |
| Status | Template |

---

## フォルダ構成

```
docs/
├── README.md                  ← docs 全体索引・手順書
├── FOLDER_ARCHITECTURE.md     ← このファイル
│
├── 0.charter/                 ← 開発憲章（憲法・9ファイル）
│
├── 1.concept/                 ← コンセプト
│   ├── 00-overview.md         （課題認識・なぜ dodoAI か・アプローチ）
│   ├── 01-problem.md
│   ├── 02-why-dodoai.md
│   └── 03-approach.md
│
├── 2.manual/                  ← マニュアル（実施手順）
│   ├── 00-overview.md
│   ├── 00.preparation/        （MCP セットアップ・入力資産の準備）
│   └── 01.structuring/        （構造化＝SDT 投影の実施手順）
│
├── 3.output/                  ← アウトプット
│   └── 00-overview.md         （成果物の正本は docs/99.sdt/art/。ここは索引のみ）
│
├── 4.evaluation/              ← 評価
│   └── 00-overview.md         （到達度評価・ドリフト統治・HIL ゲート）
│
├── 5.reference/               ← 参考資料
│   ├── README.md              （受領資料・外部資料の置き場ルール）
│   └── templates/             （BR/SR/EPIC 等のドキュメントテンプレート）
│
├── 98.dodoai-custom-spec/     ← dodoAI カスタム仕様（Custom UI / Custom Action の A02 正本）
│   └── 00-overview.md
│
└── 99.sdt/                    ← SDT（Semantic Digital Twin）
    ├── agn/                   ← Governance Graph（機械可読 SoT）
    │   ├── 0.schema/          ← JSON スキーマ定義
    │   ├── 1.workflows/       ← EPIC → Feature → Task Graph / Workflow 定義
    │   ├── 2.agents/          ← Agent 定義
    │   └── 3.skills/          ← Skill 定義
    └── art/                   ← ART 成果物（機械生成 SoT）
        ├── catalog/           ← API / 画面 等のカタログ
        ├── context/           ← CallGraph（Implemented Truth）
        └── operations/        ← Operation reports / catalog
```

## 番号付けの原則（Delivery Asset 共通フレーム）

| # | フォルダ | フェーズ | 内容 |
|---|---------|---------|------|
| 0 | `0.charter/` | — | 開発憲章 = 憲法。全 Agent が従う最上位原則 |
| 1 | `1.concept/` | Concept | なぜ・何を・どうやるか（Phase 0） |
| 2 | `2.manual/` | Preparation / Structuring | 準備と実施手順（Phase 1〜2） |
| 3 | `3.output/` | SDT ART | 成果物索引（正本は `99.sdt/art/`） |
| 4 | `4.evaluation/` | Evaluation | 到達度評価・ドリフト統治（Phase 3+） |
| 5 | `5.reference/` | — | 参考資料・受領資料・テンプレート |
| 98 | `98.dodoai-custom-spec/` | — | dodoAI Custom UI / Custom Action の A02 仕様正本 |
| 99 | `99.sdt/` | — | SDT = AGN（統治グラフ）+ ART（成果物） |

## SoT（Source of Truth）の原則

| 分類 | パス | 性質 |
|------|------|------|
| **憲法** | `docs/0.charter/` | 変わりにくい最上位原則 |
| **人間可読 SoT** | `docs/1.concept/`〜`docs/4.evaluation/`・`docs/98.dodoai-custom-spec/` | Markdown。人間の意図・手順・評価 |
| **機械可読 SoT** | `docs/99.sdt/agn/` | タスクグラフ・Evidence・Agent/Skill/Workflow JSON |
| **機械生成 SoT** | `docs/99.sdt/art/` | CallGraph・カタログ・requirements.json 等の生成成果物 |
| **参考（読み取り専用）** | `docs/5.reference/` | 受領資料・外部資料・テンプレート |

- 成果物（JSON/生成 Markdown）は `3.output/` に直接置かず、`docs/99.sdt/art/` を正本とする。
- MD と AGN JSON が矛盾する場合は、機械関係・status は AGN、規範文・意図・手順は MD を優先し、両方を同期補修する。

## カスタム実装の配置（docs 外）

| 対象 | パス |
|------|------|
| Custom Action 実装 | `.dodoai/custom_actions/<action_name>/`（`action.json` + `action.py` + `CONTRACT.md` + tests） |
| Custom UI 実装 | `.dodoai/custom_ui/<ui_name>/` |
| Issue / HANDOFF | `.dodoai/issue/` |
| リポジトリ指示 SoT | `AGENTS.md`（`.clinerules/` は併用する補助投影、AGENTS.md 不在時は fallback） |

Custom Action / Custom UI の**仕様（A02）**は `docs/98.dodoai-custom-spec/` に、**実装**は `.dodoai/` 配下に置く。
