---
type: test-evidence
execution_id: exec-crypto-p0-screens-20260822T1305Z
title: P0 画面実装 Evidence — OPS-1 / OPS-2
tags: [crypto-wealth-os, dd03, custom-ui, ops, partial]
---

# P0 画面実装 Evidence — OPS-1 / OPS-2

結論: `crypto-wealth-ops` の Network / Sources 2 画面と redacted Action はローカル実装・focused test・manifest Action 検証を通過した。正本は [`evidence-dd03-screen-roadmap-p0-implementation.json`](evidence-dd03-screen-roadmap-p0-implementation.json)。Task は A02、personal manifest lint、live registry、visual、`roadmap.sync_gate` 未達のため `running` のままにする。

| 層 | 結果 | Evidence |
| --- | --- | --- |
| 実装 | PASS | `.dodoai/personal/custom_ui/crypto-wealth-ops/manifest.json`、`personal.crypto_ops_status` |
| Focused test | PASS | 45 passed |
| Ruff | PASS | 新 Action 0 findings。test file は既存 E402 だけを除外 |
| Manifest authoring | PASS | `custom_ui.manifest_edit` strict dry-run/apply とも error 0 / warning 0 |
| Registry | PASS | `crypto-wealth` と `crypto-wealth-ops` を同時に確認。tenant collision は作業中に修復 |
| Direct Action | PASS | config valid、1 chain reachable、L1 observed、L1→L2 not_recorded、L3 execution frozen |
| Strict manifest lint | BLOCKED | personal path を `MANIFEST_PATH_OUTSIDE_WORKSPACE` で拒否 |
| Live Action | BLOCKED | 稼働 Core に新 Action 未登録。reload/restart は未実施 |
| Visual | 未計測 | live data source 未登録のため、画面表示を合格扱いにしない |
| Roadmap gate | 未実行 | resolver の workspace slot `8522` に listener なし。再起動は未実施 |

## 実装した境界

- OPS-1: chain/RPC 状態、Anvil 状態、L1→L2→L3 昇格 Evidence、mainnet Observe-only / execution-frozen guard。
- OPS-2: `portfolio.json` の hash/lint、`env://` 解決可否、snapshot/tick 鮮度、価格 source 実績。解決 URL・env 値・Wallet address・鍵情報は返さない。
- DOM-1: 既存 app を変更せず、focused test で回帰を確認。

## 未実装を隠さない

OPS-3 は新 Feature の EPIC/CAP HIL、LOOP-1 は catalog 初期化、LOOP-2 は owning Feature/A02、DOM-2 は H1/H2、DOM-3/4/5/7 は各 Feature A02、DOM-6 は Stage 2/H4 HIL が前提である。`全部開発済み` とは報告しない。

## Governance finding

新 OPS 画面の ED15/ED16 詳細を Feature A02 へ追加する前に実装へ入った。ロードマップ HIL は存在するが ADF 順序を満たさないため、後追い文書を「実装前作成済み」と扱わず Finding とする。

既存の screen-roadmap Issue が参照する `task-dd00-a02-screen-roadmap-ops-loop.json` は現在の worktree に存在しない。ユーザー報告の `done` を現 checkout で検証できないため、既存 TaskGraph 負債として残す。
