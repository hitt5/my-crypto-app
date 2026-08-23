---
type: contract
title: ADF Test Definition SDT
description: ADF テスト分類・旧 L alias・DD Phase・deploy unit 選択の人間可読 view
tags: [adf, testing, sdt, test-evidence]
timestamp: 2026-08-10T13:20:00+09:00
---

# ADF Test Definition SDT

機械可読面は `adf-test-definition.json`。本書はその人間可読 view であり、分類や status が矛盾した場合は
JSON と同期して補修する。テスト体系の意味は ADF、数値閾値は Charter が所有し、本対へ独自定義を増やさない。

## 参照する ADF

- `adf/docs/ja/3.process/5.test/1.test-overview.md`
- `adf/docs/ja/3.process/5.test/2.8-layer-test-overview.md`
- `adf/docs/ja/3.process/5.test/4.8-layer-test-detailed.md`

## Canonical test types

| Level | Test types | 境界 |
| --- | --- | --- |
| UT | UT-Logic-FE / UT-Logic-BE / UT-Schema | 単一モジュール・関数内 |
| ITa | ITa-Workflow-FE / ITa-Harness-BE | 同一 deploy unit 内の内部結合 |
| IT | IT-Boundary / IT-Observability | deploy unit 境界を跨ぐ |
| ST | ST-E2E-HL / ST-E2E-HD / ST-AI-Visual / ST-Human | ユーザー視点のシステム全体 |
| QG | QG-Governance / QG-LLM | テストピラミッド外の品質ゲート |

旧 L1/L2/L3/L5、および `CT` / `CT-Workflow-FE` / `CT-Harness-BE` は互換 alias であり、新規 Evidence は canonical `ITa` test type を使用する。

## DD Phase

| Phase | Scope | 必須面 |
| --- | --- | --- |
| DD01 | per-UC | UT-Schema skeleton、対象 deploy unit の ITa skeleton、QG-Governance |
| DD02 | per-UC | 対象 deploy unit の UT/ITa、境界があれば IT-Boundary、QG-Governance |
| DD03 | per-UC | DD02 と同じ層の異常系 |
| DD04 | per-Feature | IT-Observability、QG-Governance、QG-LLM |
| DD05 | per-Feature | ST-E2E-HL/HD、ST-AI-Visual、ST-Human |

## Deploy unit selection

必要層は `feature.json.attributes.deploy_unit` 一つから決めない。実際に変更した deploy unit 全件の profile を合成する。
たとえば FE と Core を同時に変更した場合、`react-frontend` の UT-Logic-FE / ITa-Workflow-FE だけでは DD02/DD03 を
完了できない。`python-monolith` の UT-Logic-BE / ITa-Harness-BE / IT-Boundary も必要になる。

## Mock boundary

- ITa-Workflow-FE: mock BE を使う UI workflow 検証。
- ITa-Harness-BE: 自アプリは実起動し HTTP で検証。mock は外部サービスだけに限定。
- IT-Boundary / IT-Observability / ST: 検証対象境界を mock しない。

## Threshold ownership

coverage 等の数値は本対に複製しない。`docs/0.charter/01-development-charter.md` §3 から解決する。
