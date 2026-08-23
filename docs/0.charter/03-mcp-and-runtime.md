---
type: charter
title: MCP 起点の開発と Runtime の使い分け
description: セッション開始手順・MCP 経由の原則・Runtime 選択規範
tags: [charter, mcp, runtime, agent]
timestamp: 2026-08-01T14:00:00Z
---

# MCP 起点の開発と Runtime の使い分け

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Updated | 2026/08/01 |
| Status | Approved |
| 種別 | **手順の正本**（条項は定義しない → 01 が正本） |

## 0. なぜ MCP を起点にするか

Agent のコンテキスト窓は有限で、セッションごとにリセットされる。**注意（attention）は希少資源**である。

ルール・Issue・仕様・グラフを全部 `read_file` すると、実装を考える前に窓が埋まる。
MCP は「必要なものを、必要な粒度で、必要な時に渡す」ための機構であり、
**ドキュメントを人間が読む代わりに、機械が要約して配る**という発想の転換である。

| 直読み（アンチパターン） | MCP 経由 |
| --- | --- |
| ルール群を全文 read | bootstrap が manifest + 必要分だけ返す |
| Issue を全件 read | 上限付き候補 → 選定した 1 件だけ read |
| 巨大グラフ JSON を丸読み（P19） | 走査 Action が該当部分だけ返す |
| 文書ツリーを ls して回る | 論理 URI 解決 / 検索 Action |

---

## 1. セッション開始手順

**STEP 0 = MCP bootstrap。** いかなる `read_file` / 検索 / ユーザーへの質問よりも前に、
セッションで最初に 1 回呼ぶ。

| # | ステップ | 目的 |
| --- | --- | --- |
| 0 | `project.bootstrap`（MCP 経由） | ルール manifest / Issue 候補（上限付き）/ 使い方ガイドを 1 コールで取得 |
| 1 | **Inventory** | 利用可能な Tool / Action を **list-only** で確認する。schema は dispatch 直前に対象 1 件だけ取得 |
| 2 | **Ops Status** | `autoloop.status` で自律開発の稼働状態（verdict / loops / roadmap 進捗）を把握し、作業開始時に 1 行明記 |
| 3 | **Route** | `agn.route_next` で標準 WF / 探索モードを判定し、作業ナビとして扱う |
| 4 | **Agent 選定** | 変更対象から Operation を特定し、Operation が宣言する Agent の context pack を初期メモリにする（§3） |
| 5 | **対象の特定** | 候補から 1 件を選び、**その 1 ファイルだけ** read する |

### Inventory を毎回取る理由

Action は増減する。**記憶で `action_key` を打つと、1 文字違いで dispatch が失敗する**か、
より悪い場合は「実在しないゲートを通した」と誤認する（CS-5 / P21 の再発）。
一覧は毎回取り、schema は使う直前に 1 件だけ引く。

### 接続不能時 — 即直読みしない

MCP が落ちても、すぐ `read_file` / grep へ降りてはならない。**bounded recovery** を実施する。

1. 短く待って**同じ呼び出しを 1 回だけ**再試行する（同一引数の乱打は P6）
2. readiness を確認する。liveness と readiness を区別する
3. listener / 常駐セッションを確認する。sandbox の loopback 拒否だけでプロセス死亡と断定しない
4. 非破壊に**1 回だけ**起動・再起動する（削除・port kill の乱用は禁止）
5. cold boot は 10 秒を超える。単発チェックで諦めず、一定間隔で上限まで poll する
6. 復旧後に bootstrap + Inventory を再実行する

**上記を尽くしてから**のみ read-only fallback を許す。その際は Evidence に
「最初のエラー / 復旧試行の内容 / 再試行結果 / fallback した理由」を必ず書く。
接続情報・ポート・起動手順の実値は `.dodoai/repo-context.json` が SoT である（本書に焼き付けない）。

---

## 2. 変更操作は Action 経由（カタログ優先）

同じ結果を出す経路が複数あるとき、**カタログに登録された経路を使う**。

| やること | 使う経路 | 直操作を避ける理由 |
| --- | --- | --- |
| SDT / status の更新 | 対応する Core Action | 手編集は主権違反（P24）で、次の再生成で消える |
| グラフ走査・影響調査 | 走査 Action | 巨大 JSON 直読みは窓を食い潰す（P19） |
| 定期処理の確認 | プロセス / CRON カタログ | 実体と宣言が乖離しても気づけない |
| 論理参照の解決 | 論理 URI 解決 Action | 物理パスの直書きは移動で切れる |

REST 直叩き・JSON 直編集・手動シェルは、**カタログ経路が利用不能なときの調査手段**に限り、
その事実を Evidence に明記する。

---

## 3. Runtime の使い分け

P3（Runtime replaceable）は「どれでも同じ」という意味ではない。
**どの Runtime を選んでも憲章のゲートが等しく効く**という意味である。

### 選定は勘で決めない

作業種別・変更対象から **Operation を特定し、Operation が宣言する Agent を機械的に採用する**。
Agent 一覧を目視で選ぶのではなく、context pack を取得して初期メモリに注入し、
作業開始メッセージに `Operation` と `Agent` を明記する。

### Runtime の性格

| Runtime | 統合形態 | 向く仕事 | 注意 |
| --- | --- | --- | --- |
| **Codex** | brokered（外部 CLI） | 定型的で範囲が明確な実装、テスト実行 | 実行可否は PATH 上の存在に依存する |
| **Claude Code** | brokered（外部 CLI） | 設計を伴う実装、コードレビュー、広い読解 | 同上 |
| **dodo coder** | native（dodoAI の Coding 境界） | ターン単位で追跡したい project editing、dodoAI 側 Coding 品質との統合検証 | resolver が返す公開境界の Coding API を使い、固定 endpoint や代替経路で置き換えない |
| **internal** | managed（Core 内） | スクリプト実行・決定論的処理 | LLM 判断を伴う仕事に使わない |

### 使い分けの原則

| # | 原則 | 理由 |
| --- | --- | --- |
| R-1 | **外部 Runtime にも憲章を届ける** | workspace instruction の読み込みに依存させず、Harness dispatch 側で必須 prompt を冪等に前置する。読み込まれなかった場合に P18 が消えるのは「届け方の設計ミス」である |
| R-2 | **native Coding を代替経路で置き換えない** | dodo coder の品質を測る仕事で別経路を使うと、測っている対象が実物ではなくなる |
| R-3 | **ファイル範囲を明示して dispatch する** | 対象を絞らない dispatch は無関係ファイルへ drift しやすい。drift した変更は成果として数えない |
| R-4 | **drift したら即中止** | 別 Issue / 別 Feature を触り始めたセッションは止める。続行して整合させる方が高コスト |
| R-5 | **可用性は health で判定する** | brokered Runtime は環境依存で使えないことがある。使えない Runtime を前提にした計画を立てない |

> **上流の参照実装と比較する**: dodo coder 自体を実装・評価するときは、pin 留めした上流実装と
> lifecycle / timeout+cancel / 永続化された進行状態 / event 完全性 / retry 分類 / 承認 /
> rollback の観点で突き合わせ、採用した不変条件を記録する。構文の移植ではなく境界の設計を借りる。

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2026/08/01 | 新設。MCP 起点手順（旧 ClineRules 側に散在）と Runtime 使い分け（旧憲章に規範が無かった）を憲章へ明文化。ポート・パスの実値は repo-context を参照し本書に書かない |
