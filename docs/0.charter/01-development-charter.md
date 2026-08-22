# Development Charter — {{PROJECT_NAME}}

本 Charter はこの workspace の開発憲法であり、`AGENTS.md` と ClineRules より上位に置く。

## Principles

1. Intent SoT: 人間が承認した Concept/Spec/Charter を意図の正本とする。
2. Traceability: Feature、UC、FR、Task、実装、テスト、Evidence を接続する。
3. Safety: 既存資産を保護し、破壊的操作と外部 publish は明示承認を要する。
4. Confidentiality: 秘密情報、個人情報、顧客実値を repository と fixture に保存しない。
5. Evidence: 実行していない検証を PASS と報告しない。

## Mandatory Gates

- P1: 明示指示なしの commit/push/merge を禁止する。
- P2: production behavior の mock fallback を禁止する。
- P3: テスト失敗または未実施を隠した完了報告を禁止する。
- P4: Custom Action 実装は CONTRACT.md なしで開始しない。
- P5: 秘密情報と顧客実値をハードコードしない。
- P6: 既存 SoT を確認せず派生成果物で上書きしない。
- P7: HIL 判断を Agent が代行して完了扱いしない。
- P8: 対象ルールと仕様を読まずに実装しない。
- P9: Task Graph JSON なしで DD 実装を開始しない。
- P10: 全 SR/FR/UC の適合確認なしに Feature 完了を宣言しない。
