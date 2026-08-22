# アプリケーションアーキテクチャ — my-crypto-app

| Key | Value |
| --- | --- |
| Version | 1.0.0 |
| Status | Draft |

---

> **TODO: プロジェクトのアーキテクチャを定義してください**

## 1. Clean Architecture 5 層

```
API Layer          ← Router / Command handler / Component
Application Layer  ← UseCase / Orchestration / DTO
Agent Decision     ← Prompt Build / LLM Parse (LLM 機能がある場合のみ)
Domain Layer       ← Entity / Value Object / Repository Interface
Infrastructure     ← Repository Impl / DB / External API
```

**依存方向: 外側 → 内側のみ**

## 2. デプロイメント単位

| 単位 | 技術スタック | EPIC |
|------|------------|------|
| backend/ | {Stack} | EPIC-SEMANTIC-DIGITAL-TWIN |
| frontend/ | {Stack} | EPIC-SEMANTIC-DIGITAL-TWIN |

## 3. モジュール間依存ルール

> **TODO: モジュール間の依存方向を定義してください**

```
{module-a}/  ← 他のモジュールが参照可能
{module-b}/  → {module-a}/ のみ
shared/      ← 全モジュールが依存
```
