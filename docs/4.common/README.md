---
type: common-requirement
title: 3.common — 共通要件（Common Requirements）索引
tags: [common, requirements, crypto-wealth-os]
---

# 3.common — 共通要件（Common Requirements）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 全 EPIC / Feature に横断適用される共通要件層。**CR 正本 = [`0.common-requirements/00-common-requirements.md`](0.common-requirements/00-common-requirements.md)（CR-1〜CR-9）を本フォルダが所有**し、dodoAI 本体 `docs/2.common/` と同型の **ビジネス要件（BR）→ システム要件（SR）＋ 非機能要件（NFR）** の層で展開する（旧 `1.concept/06-common-requirements.md` からの移設）。
> **Requirements Model との関係**: 定義順は BR → SR →（各 EPIC の UC）→ CAP → Mod（AGENTS.md §Requirements Model）。本フォルダは BR / SR / NFR の共通層のみを所有し、UC・Feature 固有要件は各 EPIC 側で表現する。**BR / SR / NFR の新設・変更は HIL 裁定必須。**

## 構成

```text
3.common/
  README.md                              本索引
  0.common-requirements/                 共通要件（CR — 正本）
    00-common-requirements.md            CR-1〜CR-9（全 EPIC / Feature に横断適用）
  1.business-requirements/               ビジネス要件（BR）
    01-business-background-goals.md      事業背景・ゴール（大原則・4仮説・ポジショニング）
    02-business-requirement.md           ビジネス要件 BR-1〜BR-7
  2.system-requirements/                 システム要件（SR）
    01-key-custody-requirements.md       SR-KEY: 鍵管理・署名（← CR-1）
    02-policy-governance-requirements.md SR-POL: 権限統治・Policy Engine（← CR-2）
    03-execution-pipeline-requirements.md SR-EXE: 実行パイプライン（← CR-3）
    04-evidence-requirements.md          SR-EVD: Evidence・記録（← CR-4）
    05-viability-risk-requirements.md    SR-VIA: 生存原理・リスク統制（← CR-5 / CR-9）
    nfr/                                 非機能要件（NFR）
      01-nfr-security.md                 NFR-SEC: Agent Security（← CR-6）
      02-nfr-regulatory.md               NFR-REG: 規制適合（← CR-7）
      03-nfr-personal-scope.md           NFR-SCOPE: パーソナル Custom App スコープ（← CR-8）
```

## CR → BR / SR / NFR 対応マトリクス

| CR | 内容 | 展開先 |
|---|---|---|
| CR-1 | 鍵管理・署名（二層構成） | [SR-KEY](2.system-requirements/01-key-custody-requirements.md) |
| CR-2 | 権限統治（Policy-Custodied Autonomy） | [SR-POL](2.system-requirements/02-policy-governance-requirements.md) |
| CR-3 | 実行パイプライン（Execution Safety） | [SR-EXE](2.system-requirements/03-execution-pipeline-requirements.md) |
| CR-4 | 根拠と記録（Evidence by Default） | [SR-EVD](2.system-requirements/04-evidence-requirements.md) |
| CR-5 | リスク統制（Risk Discipline） | [SR-VIA](2.system-requirements/05-viability-risk-requirements.md) |
| CR-6 | セキュリティ（Agent Security） | [NFR-SEC](2.system-requirements/nfr/01-nfr-security.md) |
| CR-7 | 規制適合（Regulatory Posture） | [NFR-REG](2.system-requirements/nfr/02-nfr-regulatory.md) |
| CR-8 | パーソナル Custom App スコープ | [NFR-SCOPE](2.system-requirements/nfr/03-nfr-personal-scope.md) |
| CR-9 | 生存原理（Viability Principle） | [SR-VIA](2.system-requirements/05-viability-risk-requirements.md) |

## 正本関係と優先順位

1. **[`0.common-requirements/00-common-requirements.md`](0.common-requirements/00-common-requirements.md) が CR の正本** — CR の追加・変更はまず HIL 裁定を経て CR 正本で行い、BR / SR / NFR は同一変更で追随する
2. 本フォルダの BR / SR / NFR は CR を**検証可能な要件文**（要件 ID・受入基準・数値閾値・トレーサビリティ）へ展開したもの
3. CR は Concept（`1.concept/`）の大原則・データモデル・Gate 定義と整合しなければならない。矛盾に気づいたら HIL へ。片側の先行変更でもう片側を上書きしない

## 記法

- 要件 ID: `BR-n` / `SR-XXX-n` / `NFR-XXX-n`（XXX = 3〜5 文字の領域コード）
- 各要件は**決定論的に検査可能**な形式で書く（曖昧語「適切に」「十分に」を単独で使わない）
- HARD = 違反したら実装・実行を拒否する要件 / SOFT = 逸脱時に Finding として記録する要件

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.2.0 | 2026-08-22 | CR 正本を `1.concept/06-common-requirements.md` から `0.common-requirements/00-common-requirements.md` へ移設（ユーザー HIL）。正本関係を本フォルダ内に統合 |
| v0.1.0 | 2026-08-22 | 初版。dodoAI `docs/2.common/` と同型（BR / SR / NFR）で構成を定義し、CR-1〜CR-9 の対応マトリクスを作成 |
