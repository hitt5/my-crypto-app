---
type: charter
title: 品質ゲートとテスト戦略
description: テストレベル・Gate 一覧・完了ゲートの手順正本
tags: [charter, quality-gate, test, completion]
timestamp: 2026-08-01T14:00:00Z
---

# 品質ゲートとテスト戦略

| Key | Value |
| --- | --- |
| Version | 1.3.0 |
| Updated | 2026/08/16 |
| Status | Approved |
| 種別 | **手順の正本**（条項・閾値は定義しない → 01 が正本） |

## 0. Gate の役割

Gate は品質を「作り込む」仕組みではない。**壊れた状態が下流へ流れるのを止める**仕組みである。

Agent は人間より速く進むため、**止める機構がないと誤りも速く伝播する**。
そして Gate が意味を持つ条件は 1 つだけである。

> **FAIL したときに実際に止まること。** 止まらない Gate は、無い方がまだ正直である。
> 「FAIL したが影響は小さいので進めた」を一度許すと、Gate は装飾になる（CS-5）。

---

## 1. テストレベル

| 層 | 対象 | 判定するもの |
| --- | --- | --- |
| **UT** | 関数・クラス単位 | ロジック・スキーマの正しさ |
| **ITa** | 内部結合 | 同一deploy unit内の呼び出し側と実装側を結合し、**実機**で叩く |
| **IT** | モジュール結合 | 境界をまたいだ振る舞い・観測性（ログ / trace） |
| **ST** | システム全体 | 利用者視点の成立（E2E / Visual / Human 確認 / サーバー面） |
| **QG** | 横断 | ガバナンス・アーキテクチャ・LLM 品質 |

### 層の対応（L1 〜 L8）

| # | 層 | 対応 | DD Phase |
| --- | --- | --- | --- |
| L1 | ロジック単体 | UT | DD02 |
| L2 | スキーマ / 型 | UT | DD02 |
| L3 | 境界結合 | IT | DD02 |
| L4 | 契約（実機） | ITa | DD01 骨格 → DD02 |
| L4-LLM | LLM 品質評価 | QG | DD04 |
| L5 | fixture 実機 | ITa | DD02-DD03 |
| L6 | 観測性 | IT | DD04 |
| L7 | システム E2E | ST | DD05 Track A |
| L8 | リリースデプロイ検証 | ST | DD05 Track B（**リリース済み Feature のみ** — §4 Check 5） |

| # | 規律 | 内容 |
| --- | --- | --- |
| ST-SERVER | **リリース面の検証をローカルで代替しない** | **リリース済み**の Feature は、実際にリリース（deploy / 配布）した環境に対して readiness / smoke / 実 URL への browser E2E / 実行ログを検証する。ローカル起動 URL への E2E を「リリース検証済み」と主張してはならない（= 02 §5）。未リリースの Feature は本規律の対象外である（§4 Check 5） |

### 規律

| # | 規律 | 理由 |
| --- | --- | --- |
| T-1 | **ITa は自アプリを実機で叩く** | モックだけの内部結合テストは「自分の思い込み」を検証しているに過ぎない |
| T-2 | **fixture に顧客実値を書かない**（P5） | テストは最も secret が漏れやすい場所である。汎用ダミー値か sanitize 済みを使う |
| T-3 | **DD Phase に対応するテストを持つ** | どの Phase で何が保証されたか分からないと、退行の切り分けができない |
| T-4 | **一般回帰の PASS を受入テストの代替にしない** | 「壊れていない」と「要求を満たす」は別物である |

---

## 2. Gate 一覧

| Gate | いつ | 何を見るか | Action |
| --- | --- | --- | --- |
| **Inventory** | セッション開始時 | 利用可能な Tool / Action を list-only 確認 | Inventory（= 03） |
| **Task Graph** | DD01 着手前 | タスクグラフの存在（P9） | `agn.schema_check` |
| **A02** | A03 着手前 | 6 層 + NFR 適用判断の未確定 0 + マルチロール approved（P11 / P12） | HIL レビュー（P11）/ `agn.multi_agent_review`（P12） |
| **A03** | DD01 着手前 | SDT/AGN 構造検査 — スキーマ自己整合性 + 書き込み主権 + 要件語彙境界（P13） | `sdt.schema_self_conformance` / `sdt.authoring_validate` / `sdt.ontology_validate` |
| **Scaffold** | DD02 着手前（Feature 最初の UC の DD01 内） | 骨格生成 + 凝集性 + Invariant baseline 凍結（P28） | `a03.scaffold_gate` / `arch.layer_check` / `arch.module_boundary` |
| **Preload** | **コード変更前** | 影響 UC / Feature / EPIC の把握（P18） | `callgraph.focus` |
| **Contract** | DD02 着手前 | 契約の機械検証（P14） | `agn.contract_json_verify` |
| **Concept** | DD04 | コンセプトとの整合（P17） | `concept.alignment_review` |
| **Completion** | 完了主張前 | §4 の全項目 | 複数（§4） |

### Preload Gate — 変更前に影響を知る

コードを触る前に、**変更対象から辿れる影響範囲**を把握する。

| やること | 理由 |
| --- | --- |
| 変更対象に対し影響調査を実行する | 呼び出し元・呼び出し先・影響 UC を知らずに変更すると、無関係な機能が壊れる |
| 結果を Evidence として出力する | 出力するまでコード変更を開始しない |
| 静的な trace 参照で代替しない | 静的リストは古い。**実際に逆引きを実行する**ことが要件である |
| 巨大 JSON を丸読みしない（P19） | 窓を食い潰す。走査は Action 経由 |

**プロンプトで指示しただけでは要件を満たさない。** 実行系（Harness / native Coding）の
composition で機構として配線し、指示が届かなかった場合にも Gate が消えないようにする（R-1）。

---

## 3. 数値基準

**閾値の正本は 01 §3 である。** 本節は測り方だけを述べる。

| 測るもの | 測り方 |
| --- | --- |
| テスト成功 / カバレッジ | テスト実行の実測値。完了報告に実数を記載する |
| Evidence の欠落・リンク切れ | `test_evidence.audit` |
| 凝集度・レイヤ・循環 | `arch.layer_check` / `arch.module_boundary` |
| ガバナンス登録 | `sdt.governance_metrics` |
| status 同期 | `roadmap.sync_gate` |
| 憲章同期 | `rules.audit` |

**数値 NFR は現行の実行環境で実測する。** 「設計上満たすはず」は測定ではない。

---

## 4. 完了ゲート — status を証拠と取り違えない

これは最も違反されやすいゲートである。

> **`_done` / green gate / テスト PASS / 既存 Evidence は「登録」と「退行なし」の証拠であり、
> 「要求を満たした」証拠ではない。**

### Check 0 — 仕様適合性の実査（他の Check より先）

現在のチェックアウトに対して行う。

1. 対象 Feature の要求（SR / FR / UC）と契約を読み、**全件を列挙**する
2. 各行を**実装パスと受入テストへ対応付ける**
3. `PASS` / `PARTIAL` / `FAIL` / `NOT IMPLEMENTED` で判定する。**status から PASS を推定しない**
4. 設計上の責務配置と実ツリー / 実 import を比較する
5. 変更操作は非破壊性・冪等性・rollback・全書き込み先を個別に検証する
6. 「1 コールで完結する」「自動で合成される」要件は、**最小入力で実際に動かして**確認する。
   呼び出し側が手で前処理して通るなら `PARTIAL` である

**対象範囲に PASS 以外が 1 件でもあれば完了禁止。**

### Check 1-4 — 機械検証

| # | 確認 | Action |
| --- | --- | --- |
| 1 | ガバナンス登録 | `sdt.governance_metrics` |
| 2 | Evidence の欠落・リンク切れが 0 | `test_evidence.audit` |
| 3 | テスト PASS + カバレッジ（閾値 = 01 §3） | テスト実行 |
| 4 | status 同期（P20） | `roadmap.sync_gate` |
| 5 | 書き込み主権違反が 0（P24） | `sdt.authoring_validate` |

### Check 5 — Release Validation Gate（リリース連動 — done をブロックしない）

デプロイ検証・稼働実績の判定軸は**環境（ローカルかサーバーか）ではなく、リリース有無**である。

| Feature の状態 | 判定 |
| --- | --- |
| **未リリース**（`release_status: unreleased`） | Release Validation は**対象外**。デプロイ検証・稼働証跡の欠如を理由に Feature done をブロックしない。「未計測」ではなく「未リリース（対象外）」と記録する |
| **リリース済み**（`release_status: released`） | Track B 相当（deploy → readiness → smoke → **リリース先実 URL** への browser E2E → 実行ログ）を通す（= 02 §5）。リリース済みで稼働証跡がなければ **FAIL** |

- 本ゲートは Feature Complete（開発完了 = Check 0-4）とは**別軸のライフサイクルゲート**である。
  リリースイベントの発生が判定のトリガーであり、開発完了の前提条件ではない。
- リリース形態（サーバー deploy / ローカルアプリ配布）は**検証手段の選択**にのみ使い、免除条件にしない。
  旧 `deployment_validation: local-only / required` の環境ベース分岐は deprecated（= 02 §5）。
- 状態表示は 3 値を混同しない: **対象外**（未リリース）/ **未計測**（対象だが測定パイプ未整備 — blocker として可視化）/
  **FAIL**（リリース済みで証跡なし）。「invalid を fail に丸めない」原則を本ゲートにも適用する。

### 延期するときの規律

今回のスコープ外へ延期する場合も、**判定を PASS に書き換えない**。

- 各 gap を具体的な `_ready` の作業単位とタスクグラフ依存へ接続する
- Feature Complete は **pending のまま**にする
- 既存の Feature / Issue が同じ責務を持つならそこへ集約し、**重複を起票しない**

> **「実装して」「直して」に対し、既存の `_done` を根拠に「確認したら完了済みでした」と
> 返してはならない。** 未実装なら実装し、できないなら具体的な blocker を示す。
> 過大な status は再オープンして是正する。

---

## 5. Issue の閉じ方

Issue は自律開発の作業単位であり、claim 対象・優先度キューの入力・Evidence の起点である。
したがって「閉じる」判断は人間の目視や本文の文言ではなく、**SDT の実査に基づく機械判定**でなければならない（P22）。

### クローズ Gate（4 種）

| # | Gate | 内容 |
| --- | --- | --- |
| G1 | task status | 対応するタスクが done である |
| G2 | Evidence | Evidence が存在し成功系である |
| G3 | Evidence 整合 | 欠落・リンク切れが 0 である |
| G4 | status 同期 | ロードマップと同期している |

- 本文が完璧でも G1-G4 が揃わなければ**閉じられない**
- 本文が不完全でも G1-G4 が揃えば**閉じられる**
- Gate 入力が取得不能なら**閉じない（fail-closed）**

### ライフサイクルの規律（IL-1 〜 IL-8）

| # | 規律 | 内容 |
| --- | --- | --- |
| IL-1 | **定義の機械検証** | 必須フィールドはスキーマを単一 SoT として機械検証する。MD テンプレートはその人間可読 view であり、フィールド定義を MD 側で二重定義しない |
| IL-2 | **生成経路の準拠強制** | Issue を生成する全経路がスキーマ準拠を出力する。違反 Issue を生成する経路を残さない |
| IL-3 | **双方向束縛** | Issue と SDT は双方向に機械解決できること。参照にワイルドカードを書かない（実パスまたは論理 URI のみ）。archive 後も解決器で追従させ、registry を手編集しない |
| IL-4 | **Gate 駆動クローズ** | クローズ判定は G1-G4 の実査で行い、本文の文言は補助シグナルへ降格する |
| IL-5 | **非開発 Issue の判定経路** | 運用 Issue は宣言されたクローズ条件の充足で判定する。条件が未宣言のものはクローズ不可 |
| IL-6 | **非破壊・冪等** | archive は**移動であり削除ではない**。同一入力の再実行は追加の副作用を持たない。dry-run を既定の検証手段として提供する |
| IL-7 | **コスト帰属** | Issue 単位のコストは Evidence 側を正本として記録し、本文へ同じ数値を authoritative に転記しない（P10）。帰属可能なイベントが 0 件なら欠測として明示し、**「コスト 0」と記録しない**（P27） |
| IL-8 | **Gate 緩和の禁止** | 滞留の解消は Gate の緩和ではなく、正当なクローズと未充足分の可視化で達成する。Gate を緩める実装は P3 / P20 違反の自動化である（= 04 §2） |

## Version History

| Version | Date | Changes |
| --- | --- | --- |
| 1.3.0 | 2026/08/16 | Check 5 を「DD05 の分岐（`deployment_validation` 環境属性）」から「Release Validation Gate（リリース有無 = `release_status` で判定する別軸のライフサイクルゲート）」へ再定義。未リリース Feature の done をデプロイ稼働実績でブロックしない。対象外 / 未計測 / FAIL の 3 値を条文化。L8 / ST-SERVER をリリース連動へ更新。02 §5 / `.clinerules-detail/11-completion-gate.md` と同期 |
| 1.2.0 | 2026/08/08 | A02 Gate の NFR 条件を適用判断の未確定 0 へ変更。Feature 単位検証器が未実装の P11 を HIL レビューと明記し、性能用 Action を誤って HARD GATE として扱わないよう修正 |
| 1.1.0 | 2026/08/06 | A03 Gate の検証内容を「Scaffold + 凝集性 + Invariant baseline」から「SDT/AGN 構造検査（スキーマ自己整合性・書き込み主権・要件語彙境界）」へ更新し、旧内容は新設した Scaffold Gate（DD01 内・DD02 着手前）へ分離。Charter 01 §2.2 P13/P28、02 §3/§5 と同期 |
| 1.0.0 | 2026/08/01 | 新設。旧 `05-quality-gate` / `06-test-strategy`（584 行）+ ClineRules 側の完了ゲートを統合。数値閾値は 01 §3 を参照し本書に重複させない（旧版は閾値が 3 箇所に散在し不一致だった） |
