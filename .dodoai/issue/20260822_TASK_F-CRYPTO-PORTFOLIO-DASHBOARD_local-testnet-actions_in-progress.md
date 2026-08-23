---
type: issue
execution_id: crypto-local-testnet-actions-20260822-01
title: F-CRYPTO-PORTFOLIO-DASHBOARD ローカルテストネット Personal Action / UI / ネットワークポリシー
---

# F-CRYPTO-PORTFOLIO-DASHBOARD — ローカルテストネット（Anvil）Action / UI / 方針

- Task: `F-CRYPTO-PORTFOLIO-DASHBOARD-DD02-LOCAL-TESTNET-ACTIONS`
- TaskGraph: `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd02-local-testnet-actions.json`
- Feature: `F-CRYPTO-PORTFOLIO-DASHBOARD`
- Status: `running`
- Spec: `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`
- User intent: Wallet ができたのでまずテストネットで試す。テストネットを起動する Personal UI/Action を定義する。「用途によるが、スピード重視のローカルを軸にすべき」（HIL 2026-08-22）。方針を文書化すること。

## Done criteria

- `docs/2.sdt-design/04-network-policy.md` が存在し、用途 → ネットワーク（local Anvil / 公開 testnet / mainnet）の写像を定義する。
- Personal Custom Action `personal.crypto_testnet_ctl`（op=start|stop|status、Anvil chain_id 31337）が CONTRACT.md 付きで実装される。
- Personal Custom Action `personal.crypto_testnet_fund`（ローカル anvil 限定の test ETH 注入。chain_id 31337 以外は拒否）が CONTRACT.md 付きで実装される。
- `portfolio.sample.json` に `anvil-local` chain（`network_class: local-testnet`）が追加される。
- Personal UI `crypto-wealth` に testnet 状態表示ブロックが追加される。
- pytest PASS（外部プロセス・RPC は mock）。
- live smoke: start → status running → fund → snapshot が残高を読める → stop。

## Evidence

- HIL: ローカル（Anvil）軸の方針で確定（ユーザー回答 2026-08-22 17:40 JST「スピード重視のローカルを軸にすべき」「用途による」→ 用途別 3 層ポリシーで文書化）
- Foundry インストール: `brew install foundry` → anvil 1.7.1（2026-08-22 17:41 JST）
- pytest: `.dodoai/personal/custom_actions/tests/` — **31 passed**（2026-08-22 17:48 JST、`PYTHONPATH=…/dodoai`。subprocess/RPC は mock。31337 以外拒否・無関係 PID kill 拒否・冪等 start を含む）
- live smoke: anvil start（chain_id=31337 実測）→ status running → fund 123.5 ETH（`eth_getBalance` 読み戻し = 123.5）→ stop → status not running — **SMOKE OK**（2026-08-22 17:48 JST）
- `custom_ui.manifest_lint(mode="strict")`: checked=1 / **error_count=0** / warning_count=0（2026-08-22 20:37 JST。personal 実パスは `MANIFEST_PATH_OUTSIDE_WORKSPACE` となる linter 制約のため正準一時配置 `/tmp/cw-lint` で lint — 既知制約は DD03 task node に記録済み）

## A02 / A03（2026-08-22 20:43 JST）

- A02: spec v0.2.0（SR-8/9・UC-4）+ feature.json へ `uc_ids: UC-4` / `epic_id: EPIC-VIABILITY` / `satisfies: BR-1, BR-7` / `network_policy` spec_ref を反映。testnet FR の CAP-ONCHAIN-OBSERVE 所有は **fr_gap として feature.json に記録**（FR 新設は HIL 必須のため未新設）。
- A03: `a03.sdt_agn_conformance_gate` dispatch — **ok=false**（authoring_validate 14 unclassified / placement NO_INPUT / SCO advisory）。指摘は本 Feature 起因ではなく workspace 全体の catalog bootstrap 負債（`F-WORKSPACE-BOOTSTRAP` running が所有）。feature.json `phase_gates.A03 = partial` として改ざんなしで記録。
- `roadmap.sync_gate`: **ok=false**（stale_task_status=2 / missing_milestone=1 / epic_orphan=1 / cap_unbound=1）— roadmap SoT / EPIC・CAP catalog ノード未初期化による既存負債（同上 F-WORKSPACE-BOOTSTRAP 所有）。本作業では改ざんせず記録のみ。

## Changed files（本作業）

- `docs/2.sdt-design/04-network-policy.md`（新規・Git 追跡）
- `docs/98.dodoai-custom-spec/F-CRYPTO-PORTFOLIO-DASHBOARD/00-spec.md`（v0.2.0・Git 追跡）
- `docs/99.sdt/agn/.../F-CRYPTO-PORTFOLIO-DASHBOARD/feature.json` / `task-dd02-local-testnet-actions.json`（agn.node_upsert 経由・Git 追跡）
- `.dodoai/personal/custom_actions/crypto_testnet_ctl/{CONTRACT.md,action.py,action.json}`（local-only）
- `.dodoai/personal/custom_actions/crypto_testnet_fund/{CONTRACT.md,action.py,action.json}`（local-only）
- `.dodoai/personal/custom_actions/tests/test_crypto_testnet_actions.py`（local-only）
- `.dodoai/personal/config/portfolio.sample.json`（anvil-local chain 追加・local-only）
- `.dodoai/personal/custom_ui/crypto-wealth/manifest.json`（v1.1.0 testnet ページ・local-only）
- 本 Issue（Git 追跡）

## Remaining（本 Issue は running のまま）

- dodoAI Desktop の Action registry へ personal actions をロードした live dispatch / UI 表示確認（runtime reload はユーザー承認後）
- HIL: catalog bootstrap 完了後に testnet FR を CAP-ONCHAIN-OBSERVE 配下へ正式登録（fr_gap 解消）
- roadmap SoT / EPIC・CAP catalog ノード初期化（F-WORKSPACE-BOOTSTRAP 側）
