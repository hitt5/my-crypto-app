---
type: procedure
title: Environment — 環境の位置付けと復旧（値は参照のみ）
timestamp: 2026-08-01T11:45:00Z
tags: [clinerules, l2, environment, mcp-recovery, dual-node]
---

# Environment

> **このファイルは R クラス（Reference）である。**
> ポート番号・サービス一覧・物理パスの**値を本文に書かない**。旧 L2 が破綻した最大の原因がこれだった
> （宣言していた 4 ポートのうち実際に稼働していたのは 0 個）。値は必ず下の SoT から取得する。

## 事実の取得先（SoT）

| 知りたいこと | 取得先 |
|---|---|
| サービス名・ポート・起動コマンド | `.dodoai/repo-context.json` の `active_services` |
| 主要ディレクトリ（core / frontend / docs / SDT） | `.dodoai/repo-context.json` の `key_paths` |
| Charter / AGN / Issue の場所 | `dodo_project_bootstrap` のレスポンス |
| 利用可能な Action と schema | `dodo_action_list`（schema は dispatch 直前に対象のみ） |
| CRON / scheduler プロセス一覧 | `process_catalog.list` |
| ワークスペース構成 | `.dodoai/repo-context.json` の `workspace` |
| MCP 接続設定 | `.mcp.json` |
| 上流参照リポジトリ（ADF / Codex 等）の場所 | `.dodoai/repo-context.json` の `canonical_knowledge.resources` |

❌ 「ポートは XXXX」と本文に書く / スクリプト名を推測で書く / 一覧を本文に複製する

### 上流参照（Upstream Reference）

dodoAI の外にある参照専用リポジトリは、**複製せず参照で繋ぐ**。物理パスは
`canonical_knowledge.resources` が単独所有するので、**ここにも Issue にも literal を書かない**。

- 解決: `dodo_project_bootstrap` のレスポンス、または `canonical_knowledge.resources[id=<id>]`
- 各リソースは `exists` / `entry_exists` / `content_hash` を返すので、参照先の実在は推測せず確認する
- なぜその参照が存在するかは **CAP 側**が持つ（例: `CAP-CODING.attributes.upstream_reference`）
- 参照は read-only。上流の更新は再抽出で反映し、上流由来の成果物を本リポジトリの SDT へ手で書き写さない
- 他者コードを取り込む判断は license 継承を伴うため HIL 事項（Charter 準拠）

❌ 上流の物理パスを ClineRules / Issue / SDT 本文へ直書きする
❌ 上流由来の CallGraph や成果物を dodoAI の SDT へ複製し、正本を二重化する


## MCP Recovery Gate（接続不能時）

**MCP が落ちていても、即座に直読みへ降りてはならない。** 順に試す。

1. 2〜3 秒待って同じ MCP call を **1 回だけ**再試行
2. `/ready` を確認する（`/health` は liveness のみで不十分）
3. sidecar の listener を確認する（ポート番号は `repo-context.json` の `active_services` から取る）
4. `tmux ls` を確認する
5. listener 不在または stale の場合のみ、**非破壊の起動/再起動を 1 回**行う
   （既存の `dodo-core-8510*` tmux セッション、または repo 標準の起動経路）
   - `--ensure-sidecar` は既存 tmux セッションが無くても detached sidecar を cold start する。
     **したがって tmux セッションの不在それ自体は失敗の兆候ではない**
6. cold boot（FastAPI + SQLAlchemy + 全 Action registry の import）は 10 秒を超えることが普通なので、
   起動後は `/ready` を **3〜5 秒間隔で最大 45 秒程度** ポーリングする。1 回だけの即時確認では不足
7. `/ready` が通ったら `dodo_project_bootstrap` と `dodo_action_list(include_schema=false)` を再実行

ポーリング窓を使い切って初めて read-only の直接ファイル調査へ降りてよい。その場合 Evidence に
**初回エラー / 実施した復旧チェック / 再試行結果 / fallback 理由**を必ず記載する。

## Action Registry が stale な場合

built-in Action・schema・`register_builtin_actions`・MCP gateway 挙動・Chat Action セットを変更したら、
**稼働中の sidecar を再起動してから**検証する。Action Registry は sidecar 起動時に構築されるため、
古いプロセスは新規 Action に対して `Action not found` を返す。再起動後 `dodo_action_list` で実在を確認する。
Cockpit / AI Chat が古い状態を表示する場合は Vite/Tauri の dev セッションも再起動する。

意図された経路が Core Action であるとき、手動 UI 操作・直接 REST・JSON 手作成へ逃げてはならない。

## 環境の位置付け（Two-Plane / Dual-Node）

正本: `docs/4.operation/08-local-server-dual-node-development.md`
Control Plane: `docs/4.operation/02-agentic-dev-control-plane.md`
期間計画: `docs/4.operation/12-two-plane-soak-plan-202608.md`

原則: **両方の面が開発する。ただし同じ仕事はしない。**

| 面 | 役割 | 権限 |
|---|---|---|
| **Local**（Mac / local-core） | 品質・HITL レーン。現時点の自律開発の主戦場 | A02 設計 / A03 Conformance / DD01 Scaffold + CONTRACT / 難所 DD02 / High risk 全部 / **Merge 承認・Human Override / SDT・AGN 書き込み主権**。Git は `local/*` のみ |
| **Dev2**（EC2 / server-core） | スループットレーン（将来の本命）。現在は headless 連続稼働と可搬性の実証面 | Low/Medium risk の定型 DD のみ（解禁後）。**Merge Gate を持たない**。Git は `auto/server/*` のみ |

排他は 4 層で担保する。

1. **選定層**: 単一 Priority Queue（`roadmap.derive` → `priority_cycle`）から両面が取る
2. **実行権層**: `stream.claim`（共有 Postgres の lease）。`claimed_by` + `claim_token` を dispatch から writer まで伝播
3. **SoT 層**: Single Writer — token 保持者のみが task/feature/roadmap/Issue の status を更新し、完了は `roadmap.sync_gate`
4. **Git 層**: branch namespace 分離 + Merge Gate を Mac/人間に一元化

暫定運用: live な two-node claim Evidence が揃うまで、開発 dispatch 系 CRON は**一方のノードのみ**で有効化する
（現状 Local）。Dev2 は read-only 監視と自身の soak evidence 書き込みのみ。Evidence には `plane: local | dev2` を含める。

❌ live な共有 Postgres claim 実証なしに両ノードで開発 dispatch CRON を同時有効化
❌ active claim token（または Evidence 済みの静的割付）なしに当該 STREAM のコード・status・Issue へ書き込み
❌ Dev2 へ Merge 承認 / protected branch push を許可
❌ Dev2 側のドキュメント・Evidence に実クレデンシャルを記載（Charter P5 — `env://` 論理参照のみ）

## Git ブランチ衛生

- `develop` / `main` / `master` 上で直接 commit・merge commit を作らない（Charter P1）
- 保護ブランチに居るまま pull を頼まれたら、まず作業ブランチを作って切り替えてから merge/rebase する
- 保護ブランチ上に誤って commit したら、直ちに作業ブランチへ退避し、保護ブランチを `origin/<branch>` へ戻す
- 統合は作業ブランチ + PR で行う（明示指示がある場合を除く）

## 作業管理

Issue / HANDOFF は `dodo_project_bootstrap` が返す `issue_path` 配下に作成し、
テンプレートは `docs/99.sdt/agn/0.schema/issue-handoff-template.md` を使う。

| 種別 | 命名 |
|---|---|
| HANDOFF | `{YYYYMMDD}_HANDOFF_{status}.md` |
| STREAM | `{YYYYMMDD}_STREAM_{STREAM_ID}_{short-name}_{status}.md` |

status は `_ready` → `_in-progress` → `_done` と遷移させる。完了メッセージにはフルパスを記載する。
