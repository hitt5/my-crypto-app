---
type: issue-stream
title: DD03 - Portfolio visualization hardening
tags: [crypto-wealth-os, dashboard, dd03, error-path]
---

# STREAM DD03 Portfolio visualization hardening

| Field | Value |
| --- | --- |
| Task ID | `T-CRYPTO-PORTFOLIO-DASHBOARD-DD03-SCREEN-VISUALIZATION-20260822` |
| Feature | `F-CRYPTO-PORTFOLIO-DASHBOARD` |
| Status | 🚧 Running — live registry dispatch pending |
| Task Graph | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd03-screen-visualization.json` |

## 結果

履歴不足、欠損価格、単一 source、stale、watch-only、不正入力、壊れた JSONL の実装と focused test は合格した。実 local data でも ETH held、BTC/BNB watch-only、13 履歴点を確認した。

## 完了条件

- [x] DD03 error-path UT / ITa / boundary — 26 focused tests passed
- [x] 欠損をゼロ値へ捏造しない
- [x] strict manifest lint — error 0 / warning 0（同一 bytes の正規 lint path 検証）
- [ ] project-scoped live dispatch / dashboard UI evidence
- [x] `roadmap.sync_gate` — `ok=true`、全 drift count 0（legacy milestone waiver）

## Blocker

稼働中 Core registry は新規 Action 登録前で、`personal.crypto_price_history` / `personal.crypto_asset_overview` が 404。ユーザー可視 runtime の reload/restart は明示承認がないため実施していない。

Evidence: `docs/99.sdt/art/test-results/F-CRYPTO-PORTFOLIO-DASHBOARD/evidence-dd03-screen-visualization.md`
