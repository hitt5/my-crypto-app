---
type: issue
execution_id: crypto-portfolio-dashboard-mvp-20260822-01
title: F-CRYPTO-PORTFOLIO-DASHBOARD EVM Observe MVP
---

# F-CRYPTO-PORTFOLIO-DASHBOARD — EVM Observe MVP

- Task: `F-CRYPTO-PORTFOLIO-DASHBOARD-DD01-EVM-OBSERVE-MVP`
- Feature: `F-CRYPTO-PORTFOLIO-DASHBOARD`
- Status: `running`
- Spec: `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`
- User intent: Wallet を作りつつ資産管理を主軸に、価格 Tick 取得とダッシュボードを早めに欲しい。まず EVM から始める（ユーザー裁定 2026-08-22）。

## Done criteria

- Personal Custom Action 3 本（`personal.crypto_portfolio_snapshot` / `personal.crypto_price_tick` / `personal.crypto_portfolio_valuation`）が CONTRACT.md 付きで実装され、pytest が PASS する。
- Personal UI manifest `crypto-wealth`（dashboard ページ）が存在し、3 Action を data_source として参照する。
- `.dodoai/personal/config/portfolio.json` のサンプル（プレースホルダのみ）と `.gitignore` 整備により、実アドレス・実値が Git 追跡されない。
- 全 Action は read-only / `risk_level: low`。秘密鍵・シード・実値は repo / fixture / ログに存在しない（CR-1 / CR-8.3）。

## Notes / Governance

- AGN feature.json / task-dd*.json: 本プロジェクトの SDT workflow catalog は未初期化（`F-WORKSPACE-BOOTSTRAP` running）。TaskGraph JSON 正本は catalog 初期化後に登録する。本 Issue を暫定の人間可読 view とし、未登録は Finding として本 Issue に記録する。
- `roadmap.sync_gate` は roadmap SoT 未初期化のため resolve 不能（既知の負債、`F-WORKSPACE-BOOTSTRAP` Issue に記録済み）。
- Wallet 実アドレスは `.dodoai/personal/config/portfolio.json`（Git 非共有）にユーザー本人が記入する。

## Evidence

- HIL: EVM から開始（ユーザー回答 2026-08-22 13:49 JST）
- Personal UI 機構使用の裁定: ユーザー指摘により `.dodoai/personal/` scope に確定
- pytest: `.dodoai/personal/custom_actions/tests/test_crypto_actions.py` — **16 passed**（2026-08-22 13:57 JST、`PYTHONPATH=/Users/hitoshimurakami/myApps/dodoai python3 -m pytest`。外部 I/O は mock）
- JSON validity: manifest.json / portfolio.sample.json / 3× action.json すべて parse OK
- `.gitignore` 検証: `git check-ignore` により `.dodoai/personal/*/*` が全実装ファイルに適用（Git 非共有を確認、既存ルール line 109）
- 全 Action は `risk_level: low` / read-only / 追記のみ。秘密鍵・シード・実アドレスは repo / fixture / テストに不在

## Changed files（本作業）

- `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`（Git 追跡）
- `.dodoai/issue/20260822_TASK_F-CRYPTO-PORTFOLIO-DASHBOARD_evm-observe-mvp_in-progress.md`（Git 追跡）
- `.dodoai/personal/config/portfolio.sample.json`（local-only）
- `.dodoai/personal/custom_actions/crypto_shared/__init__.py`（local-only）
- `.dodoai/personal/custom_actions/crypto_portfolio_snapshot/{CONTRACT.md,action.json,action.py}`（local-only）
- `.dodoai/personal/custom_actions/crypto_price_tick/{CONTRACT.md,action.json,action.py}`（local-only）
- `.dodoai/personal/custom_actions/crypto_portfolio_valuation/{CONTRACT.md,action.json,action.py}`（local-only）
- `.dodoai/personal/custom_ui/crypto-wealth/manifest.json`（local-only）
- `.dodoai/personal/custom_actions/tests/test_crypto_actions.py`（local-only）

## Remaining（次ステップ・本 Issue は running のまま）

- `.dodoai/personal/config/portfolio.json` にユーザー本人が実アドレス・`EVM_RPC_URL_1` を設定（HIL）
- dodoAI Desktop での live dispatch / UI 表示確認（`custom_ui.manifest_lint(mode="strict")` を含む — Core Action registry に personal actions がロードされた状態で実施）
- SDT workflow catalog 初期化後の feature.json / task-dd*.json 正式登録（Finding として記録）
