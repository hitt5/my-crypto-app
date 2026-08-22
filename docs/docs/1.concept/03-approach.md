# 03 — アプローチ（Approach）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **標準**: [`README.md`（コンセプト設計標準）](README.md) の品質バーに従う。運用ループが閉じていること（観測→評価→更新→観測）。

## 全体フロー（フェーズ分解）

```text
Phase 0  Concept       → 1.concept/                  ← 今ここ
Phase 1  Preparation   → 2.manual/00.preparation/    オントロジー定義・カタログ雛形・MCP 接続
Phase 2  Structuring   → 2.manual/01.structuring/    初期データ投入（Policy・Wallet・Allowlist・観測ソース）
Phase 3  SDT ART       → 99.sdt/art/                 カタログ正本＋ログの継続生成
Phase 4  Evaluation    → 4.evaluation/               到達度評価・HIL ゲート統治
```

プロダクトとしての自律度は 3 段階で拡張する（信頼の段階的獲得）:

```text
Stage 1  Observe   分析と提案だけ（実行しない）
Stage 2  Approve   人間承認後に執行
Stage 3  Autopilot 限定された範囲だけ自律執行（Policy・回転数・Canary の枠内）
```

機能の実装順もリスクの低い順に積む: ①資産・ポジション統合表示 → ②Opportunity クロール・評価 → ③リスク・危険検知 → ④Airdrop / Claim / 期限管理 → ⑤Lending / Staking 比較 → ⑥人間承認による実行 → ⑦限定自律実行 → ⑧リバランス / DCA → ⑨LP / Borrow / デルタニュートラル → ⑩最後に少額の方向性トレーディング。

## 運用ループ（閉じていること）

```text
① 観測 → ② 差分検知 → ③ 評価 → ④ 意思決定支援 → ⑤ HIL → ⑥ 成果物更新 → ①へ戻る
```

| ステップ | 入力 | 出力 | 確度 |
|---|---|---|---|
| ① 観測 | オンチェーン実測（残高・Approval・価格）、プロトコル情報、Governance、GitHub、市場フロー（04 §観測の表に従う） | Portfolio 空間の Fact 更新、Opportunity 空間への Source 付き観測 | Fact（オンチェーン実測）〜 Belief（クロール情報） |
| ② 差分検知 | 正本（Policy・目標配分）と実態、Opportunity の前提条件、RiskSignal 閾値 | 配分乖離（DRIFTED）、機会候補、危険兆候 | 決定論的（閾値判定） |
| ③ 評価 | 機会候補・危険兆候 ＋ Source 信頼度 | 期待純収益・リスク調整評価（Yield/Airdrop/Portfolio Agent）、Risk/Red Agent による反証、Opportunity の成立/棄却 | Belief（confidence 付き） |
| ④ 意思決定支援 | 評価済み Opportunity / RiskSignal | 実行案（Execution 候補）または「何もしない」判定 ＋ 根拠 Evidence。Policy Gate・Simulation Gate の事前検査結果 | 決定論的検査 + Belief |
| ⑤ HIL | 実行案 ＋ Gate 検査結果 | 人間の承認/却下（Observe/Approve 段階は全件。Autopilot 段階は閾値超過・緊急退避のみ） | 人間判断 |
| ⑥ 成果物更新 | 承認済み実行の結果（Observation） | Position・Evidence Ledger・StrategyVersion 実績・Source 信頼度の更新 → 次の①の観測対象になる | Fact |

ループが閉じる要: ⑥で記録した Evidence と実績が、①の観測対象（StrategyVersion 実績・Source 信頼度）として再入力され、**Agent 介入の増分利益と情報源の的中実績が継続的に較正される**。

## ステップ分解

| Step | 内容 | 入力 | 出力 | 確度 |
|---|---|---|---|---|
| S1 | Policy（投資憲法）・Wallet 分離・RiskBudget の初期定義 | ユーザーの投資方針（自然言語） | 機械実行可能な Policy、Vault/Earn/Explore/Trade の Wallet 構成 | HIL 確定 |
| S2 | 観測ソースの登録と信頼度階層の設定 | 04 §観測の表 | Source ノード群＋クロールスケジュール | 確定 |
| S3 | 資産・ポジションの統合表示（Fact 化） | オンチェーン実測 | Portfolio 空間の初期状態 | Fact |
| S4 | Opportunity クロール・評価の開始（Observe 段階） | S2 のソース | 評価済み Opportunity・RiskSignal・提案（実行なし） | Belief |
| S5 | Guardian 常駐監視の開始 | RiskSignal 閾値 | 危険検知・停止フロー | 決定論的 |
| S6 | 人間承認つき実行（Approve 段階） | S4 の提案＋HIL 承認 | Execution＋Evidence | Fact |
| S7 | 増分利益の測定と Canary 昇格判定 | Evidence Ledger＋ベンチマーク | StrategyVersion の昇格/降格、限定 Autopilot への移行判断（HIL） | 実測 |

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.3.0 | 2026-08-22 | crypto.md を元に運用ループ・3 段階自律度・ステップ分解を記入 |
| v0.2.0 | {{DATE}} | 汎用化: プロジェクトタイプ別の運用ループ読み替え例を追加 |
| v0.1.0 | {{DATE}} | 雛形から生成（未記入） |
