# Defense MVP Demo Plugin

This project plugin exposes the existing MVP demo in
`/Users/hitoshimurakami/dodoai-defense` through Core Actions.

Actions:

- `defense.mvp.status@1.0.0`
- `defense.mvp.control@1.0.0`

The demo source of truth stays in `dodoai-defense`:

- `docs/0.product-version/v1.0/2.system/EPIC_01_Defense/2.system-requirements/application-architecture.md` section 7
- `mvp/`
- `mvp_demo.py`
- `scripts/launch-mvp.sh`

Typical dispatch payload:

```json
{
  "action": "start",
  "mode": "full",
  "workspace_id": "local",
  "org_id": "local",
  "user_id": "local",
  "deploy_tier": "desktop",
  "mission_id": "RECON-ALPHA"
}
```
