# 禁止事項

正本: `docs/0.charter/01-development-charter.md`

## Charter 禁止（P1-P10）
- P1: Git操作（commit/push/merge）禁止 — 原則ユーザーが実行。例外は専用 Git 操作 Harness のみ
- P2: Mock data フォールバック禁止 — DD02以降は実機結合
- P3: テスト失敗での完了報告禁止
- P4: CONTRACT.md なしの実装着手禁止
- P5: シークレットハードコード禁止
- P6: 同一ツール×同一引数の2回以上呼び出し禁止
- P7: Feature/IUCからタスクグラフ直接生成禁止 — UC/FRから生成すること
- **P8: 開発憲章未読での開発タスク着手禁止** — セッション開始時に全 9 ファイルを読む
- **P9: タスクグラフ JSON なしでの開発着手禁止** — 存在しなければ UC/FR 単位で作成してから DD01 に進む
- **P10: SDT データの不整合な永続化禁止** — JSON ファイルが SoT

### P1 例外: Git 操作専用 Harness

Git 操作を自律化する場合は、以下の全条件を満たす専用 Harness に限定:

- 専用 WF / Agent / Skill / CRON が登録されている
- 対象 repo / branch pattern / stage 対象が定義されている
- secret scan / test status / dirty diff を Gate として検証する
- commit 結果と検証結果を Evidence に記録する
- push / merge は別 Gate とし、自動実行しない

## 運用禁止（O1-O8）
- O1: Docker リビルド禁止（明示指示なし）
- O2: 長いインラインスクリプト禁止 — ファイルに書いて実行
- O3: `rm -rf` 確認なし禁止 — `trash` 優先
- O4: 長いコマンド出力の無制限実行 — `| head -50` で制限
- O5: `_in-progress` 放置して新タスク開始禁止
- O6: ユーザー確認なし複数タスク同時着手禁止
- O7: 未登録 MCP 使用禁止（ユーザー明示なし）
- O8: Harness経由でないAgent直接実行禁止
