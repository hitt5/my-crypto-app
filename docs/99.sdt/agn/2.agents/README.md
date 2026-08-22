# Agents — Agent 定義

Agent の宣言的定義を配置する。

## 構成

```
2.agents/
└── {agent-name}/
    └── agent.json
```

## agent.json スキーマ

```json
{
  "id": "{agent-id}",
  "name": "{Agent 名称}",
  "layer": "development|operations|coordination",
  "deploy_unit": "{deploy-unit}",
  "module_scope": ["{module-path}"],
  "epic_ref": ["EPIC-SEMANTIC-DIGITAL-TWIN"],
  "runtime": "harness"
}
```
