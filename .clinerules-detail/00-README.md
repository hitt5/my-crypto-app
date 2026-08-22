---
type: policy
title: L2 ClineRules — 収録基準と再腐敗防止契約
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, governance, entropy]
---

# L2 ClineRules — 収録基準

L0 = `.clinerules/00-CORE.md`（常時遵守）／L1 = `.clinerules/00-INDEX.md`（索引）／**L2 = ここ**。
L2 は「**MCP でも Charter でも代替できない施行手順**」だけを置く。

旧 L2（15ファイル 1,909行）は 2026/08/01 にエントロピー破綻で**全件削除**した。実測した破綻の内容:

| 指標 | 実測値 |
|---|---|
| 参照先が存在しないパス | 30件（Charter 本体3本を含む） |
| 実行不能な起動手順 | 存在しないスクリプトを指示していた |
| ポート宣言 | 宣言4件のうち実際に稼働していたもの **0件** |
| Action キー誤記 | ゲートが指示するキーが実キーと 1 文字違い（区切りが `_` と `.`）→ dispatch 失敗 |
| 索引の自己矛盾 | 宣言ファイル数と実体が不一致 |

**真因は内容の古さではない。** L2 が `rules.audit` の監査対象（`md_views`）に登録されておらず、
コード・設定からの参照も 0 件だった。つまり**壊れても誰も気づかない場所**にあったため、
ツリー移行のたびに黙って腐った。部分修正では同じ速度で再び腐るため、全件破棄して作り直した。

旧内容が必要になった場合は git 履歴から取得する（`git log --diff-filter=D -- .clinerules-detail/`）。
ただし上記の乖離を抱えたままなので、**復元して使ってはならない**。

同じ破綻を繰り返さないため、以下を契約とする。

## 1. 事実を本文に書かない（N/R/E 分類）

全記述を 3 クラスに分け、**R は値を書かず参照先だけを書く**。

| クラス | 内容 | 記述方法 |
|---|---|---|
| **N**（Norm） | 原則・禁止・ゲート条件・判定基準 | **L2 が SoT**。ここだけが本体 |
| **R**（Reference） | ポート・物理パス・件数・在庫一覧 | **値を書かない**。`.dodoai/repo-context.json` / `dodo_action_list` / catalog を参照 |
| **E**（Enforcement） | その N を検証する Action | **実在する Action** を最低 1 つ。無ければ「宣言的原則」と明示 |

**偽のゲートは、無いゲートより有害である。** 実在しない Action を「HARD GATE」と書くと、
Agent は「ゲートは飾り」と学習し、その学習が実在するゲートへも波及する。

## 2. 収録してよいもの / いけないもの

| ✅ 収録する | ❌ 収録しない（正本の場所） |
|---|---|
| HARD GATE の施行手順（順序・停止条件・Evidence 形式） | 禁止事項 P1-P23 の条文 → **Charter** |
| MCP/Action の**組み合わせ手順**（単発の使い方ではなく順序と分岐） | DD 反復・A02/A03 の定義 → **Charter** |
| ローカル環境の復旧手順（Action 化されていないもの） | Action 一覧・schema → **`dodo_action_list`** |
| | ポート・パス・件数 → **`repo-context.json`** / catalog |
| | Issue 候補・ルール配信 → **`dodo_project_bootstrap`** |

## 3. 禁止事項

- ❌ ポート番号・物理パス・在庫件数を本文にハードコードする（`code.hardcode_audit` が落とす）
- ❌ 実在しない Action / スクリプト / ファイルを手順に書く
- ❌ Charter や MCP レスポンスの内容を複製する（劣化コピーになる）
- ❌ ファイル追加・改名・削除時に `.clinerules/00-INDEX.md` と `AGENTS.md` を同時更新しない

## 4. 再腐敗の検知

`dodo_core/tests/test_clinerules_l2_integrity_l1.py` が以下を機械保証する。

| 検査 | 内容 |
|---|---|
| 参照実在 | 本文の repo 相対パスがすべて実在する |
| Action 実在 | 名指しした Action キーがすべて実在する（幽霊ゲート禁止） |
| 索引整合 | L1 索引の列挙と実ファイルが 1:1（件数の宣言を本文に書かない） |
| 事実混入 | ポート番号リテラルが本文に無い |

## 5. 現行ファイル

| ファイル | 役割 | 主クラス |
|---|---|---|
| `10-preload-gate.md` | コード変更前の Preload + CallGraph 影響調査 | N + E |
| `11-completion-gate.md` | 完了主張前の仕様適合・Evidence・status 同期 | N + E |
| `20-navigation.md` | 次に何をやるか（Ops Status → route → 優先度キュー） | N + E |
| `30-environment.md` | 環境の位置付けと起動・復旧（値は参照のみ） | **R** + N |
| `40-domain-gates.md` | 領域別ゲート（Architecture / SDT / UI / 運用資産） | N + E |
