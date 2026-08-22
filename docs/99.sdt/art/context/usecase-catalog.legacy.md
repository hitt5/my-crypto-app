# UC カタログ — backend

> **TODO: プロジェクトの UC を定義してください**

## UC 定義方式 — CallGraph 接続型

各 UC は「どのモジュールの、どの関数/API を、どの順序で呼ぶか」を定義する。

## UC 一覧

### UC-001: {UC 名称}

| Key | Value |
|-----|-------|
| IUC | {IUC-ID} |
| Feature | {Feature-ID} |
| EPIC | EPIC-SEMANTIC-DIGITAL-TWIN |

**entry_point**: `POST /api/v1/{resource}`

**call_chain**:
```
src/feature/{feat}/api/router.py
  → src/feature/{feat}/application/use_case.py
    → src/feature/{feat}/domain/entity.py
    → src/feature/{feat}/infrastructure/repository.py
```

**FR**: FR-001-01, FR-001-02

---

<!-- 以下、UC を追加 -->
