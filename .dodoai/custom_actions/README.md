# .dodoai/custom_actions — Custom Action 実装置き場

プロジェクト固有の dodoAI Custom Action をここに置く。dodoAI Core の Action Registry がこのディレクトリを読み込み、
MCP `dodo_action_dispatch` から実行できるようになる。

## 構成（1 Action = 1 フォルダ）

```text
.dodoai/custom_actions/
  README.md                      ← このファイル
  {action_name}/
    action.json                  ← Action メタデータ（key / version / risk_level 等）
    action.py                    ← 実装（entry 関数）
    CONTRACT.md                  ← DD01 Contract（入出力・合格条件・異常系）
  tests/
    test_{action_name}.py        ← pytest（CT-Harness 相当）
```

## action.json スキーマ（例）

```jsonc
{
  "key": "{namespace}.{action_name}",       // 例: verify.gate_check
  "version": "1.0.0",
  "summary": "{1行サマリ}",
  "description": "{何を・どう判定/生成するか。プロジェクト固有値はハードコードせず payload 駆動にする}",
  "owner": "{project-slug}",
  "entry": "entry",
  "tags": ["custom"],
  "risk_level": "low",                      // low | medium | high
  "timeout_seconds": 30,
  "idempotent": true
}
```

## 実装ルール

- **仕様（A02）が先**: `docs/98.dodoai-custom-spec/{FEATURE_ID}/` に BR/SR/UC/CAP/FR/MOD を定義してから実装する
- **CONTRACT.md なしの実装着手禁止**（Charter P4）
- 読み取り専用 Action を基本とし、書き込みを行う場合は dry-run（`write: false`）を必ずサポートする
- プロジェクト固有ルールをコードにハードコードせず、payload で駆動する
- テスト必須: `tests/test_{action_name}.py` を追加し、テスト PASS まで完了報告しない（Charter P3）
- 顧客実値・シークレットをテスト/fixture に書かない（Charter P5）
