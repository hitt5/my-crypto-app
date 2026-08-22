# Knowledge Graph

| Key | Value |
| --- | --- |
| Version | 2.0.0 |
| Status | Active |
| Updated | 2026/05/29 |

---

## 概要

Knowledge Graph は、プロジェクト内の知識を抽象度を横断して接続するための知識コンテナである。

## 3 方向の抽象度横断

| 方向 | パターン | 説明 |
|------|---------|------|
| **上る** | Code → Feature 影響範囲 | ファイル/関数変更がどの UC / Feature に影響するかを逆追跡 |
| **下る** | Feature → Code 実装 | 仕様から実装ファイルへの正引き（CallGraph） |
| **横切る** | 同一抽象度レベルの横断 | 同じレイヤー内の関連ノード探索（Deployment Context 含む） |

## CallGraph 接続

UC は CallGraph で実装コードに接続される。

```
UC (HOW) → entry_point → call_chain → Code files
```

逆引き（ファイル → UC → Feature → EPIC）で影響範囲を特定できる。

---

## Deployment Context — Linked Knowledge によるサーバー/ローカル Agnostic

### 問題

EPIC-SOVEREIGN-RUNTIME-PLATFORM（Sovereign Runtime Platform）では同一コードベースが Desktop / Server / Edge で動作する。従来の Knowledge Graph は単一パスのトレーサビリティのみで、**デプロイメントコンテキストをまたぐ知識接続**が表現できなかった。

### 解決: deployment_scope + adapter_map

Link Registry（`ln-registry-schema.json`）の `RegistryEntry` に以下の属性を追加：

| 属性 | 型 | 説明 |
|------|------|------|
| `deployment_scope` | `"all" \| "desktop-only" \| "server-only" \| "edge-only"` | Feature/UC がどのデプロイトポロジーに属するか |
| `adapter_map` | `{ desktop: string[], server: string[], edge: string[] }` | Tier ごとに使用される Adapter/Module パス |

### 設計原則

1. **Port/Adapter パターンとの一体化**: コード実装レベルでは Port Protocol（`SDTStorePort`, `EventBusPort`, `ObjectStorePort`）が Agnostic を保証する。Knowledge Graph はこの Port/Adapter 関係を `adapter_map` として知識化する
2. **Feature レベルのスコーピング**: `deployment_scope` により「この Feature は Server-only」「この Feature は全 Tier 共通」を SDT が理解する
3. **影響分析の精度向上**: `adapter_map` により「`postgres_store.py` 変更 → F-PLATFORM-INFRA (server) にのみ影響」の自動判定が可能
4. **Agent タスク最適化**: Harness/CRON が `deployment_scope` を参照し「Desktop テスト不要」を自律判定

### EPIC-SOVEREIGN-RUNTIME-PLATFORM Deployment Scope マッピング

| Feature | deployment_scope | Desktop Adapters | Server Adapters |
|---------|-----------------|-----------------|-----------------|
| F-PLATFORM-INFRA | `all` | SQLite, InProcess, LocalFS | PostgreSQL, NATS, MinIO |
| F-PLATFORM-DEPLOY | `all` | DesktopTierConfig | ServerTierConfig, Docker |
| F-PLATFORM-TENANT | `server-only` | — | RLS, Organization, Workspace |
| F-PLATFORM-WEBAPI | `server-only` | — | FastAPI Server Mode, JWT, Health |
| F-PLATFORM-OBSERVE | `server-only` | NoOp Tracer | OTEL Tracer, OTEL Metrics |

### 横断検索パターン

```text
# 逆引き: ファイル変更 → 影響 Feature 特定（Tier 付き）
postgres_store.py
  → adapter_map.server で参照
    → F-PLATFORM-INFRA (scope: all, server adapter)
    → F-PLATFORM-DEPLOY (scope: all, server adapter)
  → 影響: Server tier テストのみ必要

# 正引き: Feature → Tier 別実装ファイル
F-PLATFORM-INFRA
  → desktop: [sqlite_store.py, inprocess_bus.py, local_object_store.py]
  → server:  [postgres_store.py, nats_bus.py, minio_store.py]

# Agent タスク判定
Task: "F-PLATFORM-TENANT DD02"
  → deployment_scope: "server-only"
  → テスト: Docker PostgreSQL 必須、Desktop テスト不要
```

---

## 禁止事項

- ❌ `deployment_scope` なしで EPIC-SOVEREIGN-RUNTIME-PLATFORM の Feature/UC を Link Registry に登録
- ❌ `adapter_map` を無視して全 Tier でテスト実行（不要な CI 負荷）
- ❌ コード内で `if mode == 'server'` 分岐（Port/Adapter + Config + DI で切替）
