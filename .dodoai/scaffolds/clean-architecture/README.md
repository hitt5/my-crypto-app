---
type: procedure
title: Project-local Clean Architecture scaffold templates
---

# Clean Architecture scaffold templates

Each project owns its language and framework scaffolds under this directory. Invoke
`arch.scaffold_generate` and `arch.scaffold_verify` with the same `template_id`; do not
add language-specific directory tables to either Action.

Every `<template_id>/scaffold.json` must declare:

- `schema: scaffold-template.v1`
- the four semantic `layer_roles`: `domain`, `application`, `infrastructure`, `interfaces`
- `placements` for `repository_port`, `repository_adapter`, and `entry`
- required directories/files and forbidden legacy paths

The loader rejects a Repository Port outside the Application role, an adapter outside
Infrastructure, or an entry point outside Interfaces. Generation creates missing paths
only and never overwrites existing implementation files.

DD01 records the selected template and its template/module fingerprints. Entry to DD02
is fail-closed unless `task.transition_status` can reproduce the same green verification
and fingerprints from the current workspace.

Example:

```json
{
  "workspace_root": ".",
  "feature_name": "billing",
  "base_dir": "dodo_core/module",
  "template_id": "python-module"
}
```

To support another language or framework, copy a template directory, change the
manifest and template files, then verify it with the Action. Project bootstrap copies
the templates from `project-template/.dodoai/scaffolds/clean-architecture/`.

Bundled project defaults are `python-module` for REST entry points and
`python-action-module` for Core Action entry points, plus `frontend-react-module` for
React presentation boundaries. Select the module's actual delivery boundary; all
templates enforce the same four dependency roles.
