---
type: issue-stream
title: DD01 - Project SDT contract bootstrap
tags: [workspace-bootstrap, dd01, sdt-contract, dashboard-admission]
---

# STREAM Bootstrap project SDT contracts and dashboard admission gates

| Field | Value |
| --- | --- |
| Task ID | `T-WORKSPACE-BOOTSTRAP-DD01-SDT-CONTRACTS-20260822` |
| Feature | `F-WORKSPACE-BOOTSTRAP` |
| DD Phase | `DD01` |
| Priority | `P0` |
| Status | ✅ Done |
| Task Graph | `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/F-WORKSPACE-BOOTSTRAP/task-dd01-sdt-contract-bootstrap.json` |

## 結果

- [x] project-local SDT layout/schema contract source
- [x] ADF test-definition MD+JSON pair
- [x] EPIC/CAP physical catalog source
- [x] A03 conformance rerun — pass
- [x] `roadmap.derive` / `roadmap.sync_gate` rerun

## Finding

現行 `roadmap.derive` と `roadmap.sync_gate` の milestone model に互換差があるため、`require_milestone=false` の legacy waiver を明示して同期した。Feature の stale / drift / EPIC / CAP / phase count はすべて 0。この framework 所有負債は project Feature の完了に偽装して閉じない。
