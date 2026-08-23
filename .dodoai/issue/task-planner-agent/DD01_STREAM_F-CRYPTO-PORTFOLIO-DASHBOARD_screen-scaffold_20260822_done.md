---
type: issue-stream
title: DD01 - Portfolio visualization scaffold
tags: [crypto-wealth-os, dashboard, dd01, scaffold, test-skeleton]
---

# STREAM Portfolio visualization scaffold

| Field | Value |
| --- | --- |
| Task ID | `T-CRYPTO-PORTFOLIO-DASHBOARD-DD01-SCREEN-SCAFFOLD-20260822` |
| Feature | `F-CRYPTO-PORTFOLIO-DASHBOARD` |
| EPIC | `EPIC-VIABILITY` |
| CAP | `CAP-ONCHAIN-OBSERVE`, `CAP-VIABILITY-EVAL`, `CAP-EVIDENCE-LEDGER` |
| DD Phase | `DD01` |
| Status | ✅ Done |
| Task Graph Ref | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-CRYPTO-PORTFOLIO-DASHBOARD/task-dd01.json` |

## 目標

ED16 の銘柄一覧・価格履歴・資産配分を、Personal Custom UI と Python personal Actions の cross-deploy 実装として DD01 admission へ通す。

## 入力

- `docs/99.sdt/art/requirements/EPIC-VIABILITY/F-CRYPTO-PORTFOLIO-DASHBOARD/screen-design.json`
- `docs/99.sdt/art/contracts/F-SDT-TEST-EVIDENCE/adf-test-definition.json`
- `.dodoai/scaffolds/clean-architecture/frontend-custom-ui-module/scaffold.json`

## 完了条件

- [x] A03 が done
- [x] frontend Custom UI scaffold の template/module fingerprint を保存
- [x] UT-Schema / ITa-Workflow-FE / ITa-Harness-BE / QG-Governance の skeleton 契約を保存
- [x] TaskGraph / Issue を同期

## 次工程

DD02 で Action と manifest の happy path、DD03 で error path と local boundary を実装・検証する。
