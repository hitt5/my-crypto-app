# 98.dodoai-custom-spec — dodoAI Custom UI / Custom Action 仕様

本ディレクトリは my-crypto-app の DODO Custom UI / Custom Action に関する **A02 仕様正本**を置く。

| Feature | Spec | Status |
| --- | --- | --- |
| {F-EXAMPLE-CUSTOM-ACTION} | [{機能の説明}]({F-EXAMPLE-CUSTOM-ACTION}/index.md) | 📋 A02 Draft |

各 Feature は dodoAI A02 に従い、**BR → SR → UC → CAP → FR → MOD と全体設計を一組**で定義する。

## Feature フォルダ構成（1 Feature = 1 フォルダ）

```text
98.dodoai-custom-spec/
  00-overview.md                  ← このファイル（Feature 一覧）
  {FEATURE_ID}/
    index.md                      ← Feature 概要・ステータス
    business-requirement.md       ← BR
    system-requirements.md        ← SR
    uc.md                         ← UC
    capability-module.md          ← CAP / FR / MOD
    module-design.md              ← モジュール設計（必要に応じ）
```

## 実装との対応

| 対象 | 仕様（ここ） | 実装 |
|------|------------|------|
| Custom Action | `{FEATURE_ID}/` 一式 | `.dodoai/custom_actions/{action_name}/`（`action.json` + `action.py` + `CONTRACT.md` + tests） |
| Custom UI | `{FEATURE_ID}/` 一式 | `.dodoai/custom_ui/{ui_name}/` |
| AGN タスクグラフ | — | `docs/99.sdt/agn/1.workflows/{epic}/features/{FEATURE_ID}/`（`feature.json` + `task-dd*.json`） |

> A02 完了条件: 仕様 MD 一式 + AGN JSON（feature.json / task-dd*.json）の両方が揃っていること。
> どちらか一方だけで A02 完了と言わない。

## 画面一覧（Custom UI がある場合）

| ドキュメント | 内容 |
| --- | --- |
| {screen-list.md} | {必要なカスタム UI 画面一覧} |
