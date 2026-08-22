---
type: issue
title: F-VIABILITY-POLICY-CORE A02 spec 完了 / DD01 は H1+H2 待ち
tags: [crypto-wealth-os, personal-scope, a02, viability]
---

# F-VIABILITY-POLICY-CORE — A02 完了・DD01 入場待ち（ready）

## TaskGraph SoT

- Feature node: `docs/99.sdt/agn/features/F-VIABILITY-POLICY-CORE/task-f-viability-policy-core.json`（`ln://agn/F-VIABILITY-POLICY-CORE/task-f-viability-policy-core` — `agn.node_upsert` で登録済み）
- Feature: `F-VIABILITY-POLICY-CORE`
- Status: `draft`（Feature） / 本 Issue = A02 成果の人間可読 view + DD01 入場 Gate の HIL 面
- Spec: `docs/98.dodoai-custom-spec/F-VIABILITY-POLICY-CORE/00-spec.md`
- Roadmap: `docs/2.sdt-design/01-development-roadmap.md`（順 2）

## Intent

Concept `03-approach.md` S1（Viability Model 初期定義）を Feature 化する。生存制約（ε）・投資憲法（Policy）・Wallet 役割・RiskBudget・Ω を機械検査可能な JSON 正本として定義し、`F-CRYPTO-PORTFOLIO-DASHBOARD` の実態観測と突合して DRIFTED を検知する（Stage 1 Observe / read-only）。

## Done（本作業 = A02 spec 作成）

- [x] ロードマップ正本化: `docs/2.sdt-design/01-development-roadmap.md`（実装順①〜⑪の Feature 写像 + DODO 本体/カスタム分担）
- [x] A02 spec: `docs/98.dodoai-custom-spec/F-VIABILITY-POLICY-CORE/00-spec.md`（BR 5 / SR 8 / UC 3 / CAP 2 + 既存 CAP 追加 / データ設計）
- [x] AGN Feature node 登録（`agn.node_upsert` 経由、direct JSON 書込はガバナンスによりブロック → MCP 経由で実施）

## DD01 入場前提（HIL — 未充足のため着手禁止）

- [ ] **H1**: Concept v0.5 根本改訂の再承認（`docs/1.concept/00-overview.md` HIL テーブル）
- [ ] **H2**: 正本値（ε・総損失限度・最低流動性準備率・目標配分・Allowlist）のユーザー確定

## Known governance findings（既存負債 — 本作業で新規作成せず記録のみ）

- EPIC / CAP catalog 未初期化: CAP-VIABILITY-CANON / CAP-VIABILITY-DRIFT は fr_gap（`F-WORKSPACE-BOOTSTRAP` 帰属）
- roadmap SoT 未初期化: `roadmap.sync_gate` resolve 不能（同上）
- `agn.node_upsert` の書込先が `docs/99.sdt/agn/features/`（既存の手動配置 `docs/99.sdt/agn/1.workflows/crypto-wealth-os/features/` と layout が異なる）— `sdt_layout.resolve` / catalog 初期化時に統一する

## Next

1. `F-CRYPTO-PORTFOLIO-DASHBOARD` 完了（portfolio.json 実値・live 確認）
2. H1 + H2 の HIL
3. 本 Feature の A03 → DD01（task-dd*.json 作成は DD01 着手時）
