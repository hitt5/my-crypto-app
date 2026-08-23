# .dodoai/custom_ui — Custom UI 実装置き場

プロジェクト固有の dodoAI Custom UI（Cockpit へ差し込むカスタム画面・パネル）をここに置く。

## 構成（1 UI = 1 フォルダ）

```text
.dodoai/custom_ui/
  README.md            ← このファイル
  {ui_name}/
    ui.json            ← UI メタデータ（id / title / slot / 依存 Action）
    {実装ファイル}      ← 画面実装（dodoAI Core の UI slot 規約に従う）
```

## 実装ルール

- **仕様（A02）が先**: `docs/98.dodoai-custom-spec/{FEATURE_ID}/` に画面一覧・BR/SR/UC を定義してから実装する
- 画面が依存する Action は `.dodoai/custom_actions/`（Custom）または dodoAI Core 標準 Action を使い、直接 REST を叩かない
- Core への直書き禁止 — UI slot / Plugin manifest 経由で登録する
