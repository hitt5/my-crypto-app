# クリーンアーキテクチャ施行規則

正本: `docs/5.reference/templates/EPIC-template-2.system/2.common-architecture/application-architecture.md`

## 1. 共通5層レイヤー

全デプロイメント単位に適用される Clean Architecture:

```
API Layer          ← Router / Command handler / Component
Application Layer  ← UseCase / Orchestration / DTO
Agent Decision     ← Prompt Build / LLM Parse / Validate (LLM 機能がある場合のみ)
Domain Layer       ← Entity / Value Object / Repository Interface
Infrastructure     ← Repository Impl / DB / External API / LLM Client
```

**依存方向: 外側 → 内側のみ（API → Application → Domain ← Infrastructure）**

## 2. デプロイメント単位別の適用

> **TODO: プロジェクトのデプロイメント単位に合わせてカスタマイズしてください**

### 2.1 Backend

| レイヤー | フォルダ | 具体例 |
|---------|---------|--------|
| API | `src/feature/{feat}/api/` | Router / Endpoint |
| Application | `src/feature/{feat}/application/` | UseCase, Service |
| Agent Decision | `src/feature/{feat}/decision/` | LLM 呼び出し（該当する場合のみ） |
| Domain | `src/feature/{feat}/domain/` | Entity, Repository Protocol |
| Infrastructure | `src/feature/{feat}/infrastructure/` | DB Impl, External API Client |
| Shared | `src/shared/` | DB engine, Events, Contracts |

### 2.2 Frontend

| レイヤー | フォルダ |
|---------|---------|
| API (Presentation) | `src/app/` (Router/Layout) |
| Application (Hooks/State) | `src/modules/{feat}/hooks/` |
| Domain (Types/Logic) | `src/modules/{feat}/types/` |
| Infrastructure (API Client) | `src/shared/lib/api.ts` |

Frontend ルール:
- Feature-based organization: `src/modules/{feature-name}/`
- Shared は cross-cutting のみ: `src/shared/{components,hooks,types}/`
- Feature 間の直接 import 禁止（shared 経由のみ）

## 3. 禁止パターン

| # | 禁止事項 | 根拠 |
|---|---------|------|
| A1 | Domain が Infrastructure に依存 | DIP 違反 |
| A2 | API Layer から Infrastructure を直接呼び出し | Application Layer スキップ禁止 |
| A3 | Feature 間の直接 import（Frontend） | shared/ 経由のみ |
| A4 | Module 間の DB 直接アクセス（Backend） | Repository Interface 経由のみ |

## 4. 新規ファイル作成時のチェックリスト

- [ ] どのデプロイメント単位か？
- [ ] どのレイヤーか？ (API / Application / Domain / Infrastructure)
- [ ] 正しいフォルダに配置しているか？
- [ ] 依存方向は外側→内側か？
- [ ] 禁止パターンに該当しないか？
- [ ] doc comment に CONTRACT / SR / FR の参照を記載しているか？
