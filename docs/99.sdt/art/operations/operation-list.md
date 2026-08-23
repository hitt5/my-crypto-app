# Operations — CRON / 定期実行定義（{{PROJECT_NAME}}）

> 本テーマの**定期実行タスク**の正本。Operation → Skill → Action の紐付けを定義する。
> Skill 定義は `agn/3.skills/README.md`。

| Key | Value |
| --- | --- |
| Status | ⬜ **未稼働**（定義のみ） |
| Updated | {{DATE}} |

---

## 1. 観測系 Operation

> **TODO: 定期的に情報を取得・更新する Operation を定義してください**
> 何を観測するかはプロジェクトタイプで変わる（ルート README §1.1）。
> 例: A=外部一次情報・競合動向 / B=KPI・業務ログ / C=新規文献・公式発表 / D=テスト結果・フィードバック / E=実態スキャン

| Operation ID | Schedule | 目的 | 使用 Skill / Action | risk_level | 状態 |
| --- | --- | --- | --- | --- | --- |
| `{operation-id}` | `0 */6 * * *` | - | - | low | ⬜ 未稼働 |

> ⚠️ 自動実行は **HIL 前段まで**に留める。人間の判断が必要な結果は `PROPOSED` で停止させ、
> **CRON が SoT を確定させない**設計にする。

---

## 2. 統治系 Operation（整合性検証）

> **TODO: スキーマ整合性・孤立データ・重複を検出する Operation を定義してください**

| Operation ID | Schedule | 目的 | 使用 Skill / Action | risk_level | 状態 |
| --- | --- | --- | --- | --- | --- |
| `{operation-id}` | `0 9 * * *` | - | - | low | ⬜ 未稼働 |

---

## 3. Operation → Skill 対応表

| Skill | 紐づく Operation |
| --- | --- |
| `{skill-id}` | `{operation-id}` |

立ち上げ時に 1 回だけ実行する Skill は CRON 化しない。

---

## 4. 稼働開始の前提

| # | 前提 | 状態 |
| --- | --- | --- |
| 1 | 入力資産が存在する | ⬜ |
| 2 | `.dodoai/workspace-profile.json` が作成済み | ⬜ |
| 3 | 使用する Action が実装・登録済み | ⬜ |

> 前提が未達のまま観測系を起動しても、**空のデータに対して空の結果を積むだけ**になる。

---

## 改版履歴

| バージョン | 日付 | 内容 |
| --- | --- | --- |
| v0.1.0 | {{DATE}} | 初版作成（テンプレート） |
