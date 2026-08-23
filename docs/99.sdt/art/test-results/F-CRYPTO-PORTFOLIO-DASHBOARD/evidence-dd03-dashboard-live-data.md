---
type: test-result
execution_id: exec-20260822-crypto-dashboard-live-data-01
title: F-CRYPTO-PORTFOLIO-DASHBOARD populated dashboard evidence
tags: [crypto-wealth-os, personal-custom-ui, dd03, local-testnet]
---

# Populated dashboard evidence

## Verdict

ローカルテストネットの観測データを使うダッシュボード表示は実装・live render とも PASS。DD03 / Feature の完了 Gate は未達のため `running` を維持する。

## Implementation

- `crypto-wealth` manifest `1.1.1`: Crypto 用 header-only hero + valuation `stat-card` を追加し、汎用開発メトリクス表示を除去。
- manifest 回帰テスト: header/stat-card/data-table contract を固定。
- Git 非共有 `portfolio.json`: disposable Anvil address のみ。秘密鍵・seed・実 portfolio 値はなし。

## Live evidence

- Tauri owner: Desktop / Vite / Provider / Core が稼働。reload / restart は未実施。
- Personal Action hot hydration: spec / dispatch とも HTTP 200。
- Anvil: `chain_id=31337`, `local-dev-vault=100 test ETH`。
- snapshot / two-source price tick / valuation: すべて live PASS。
- headless dashboard: table `4`、unsupported `0`、alert `0`、Total / Stale / Wallet / Asset / Drift / Tick が表示。
- Screenshot: `dashboard-dd03-live-data.png`。

## Tests and gates

- Focused manifest tests: `2 passed in 0.05s`
- Full personal crypto suite: `32 passed in 0.07s`
- Strict content lint in canonical temporary placement: `checked=1 / errors=0 / warnings=0`
- Real personal path lint: `MANIFEST_PATH_OUTSIDE_WORKSPACE` — `.dodoai/personal/custom_ui` が現行 linter の許可範囲外。
- `roadmap.sync_gate`: `ok=false` — stale task `2` / missing milestone `1` / EPIC orphan `1` / CAP unbound `1`。

機械可読の対は `evidence-dd03-dashboard-live-data.json`。
