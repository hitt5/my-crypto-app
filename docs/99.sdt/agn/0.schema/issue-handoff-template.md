---
type: template
title: TaskGraph Issue and HANDOFF view
tags: [agn, issue, handoff, taskgraph]
---

# TaskGraph Issue / HANDOFF view

The matching `task-dd*.json` is the machine-readable SoT. Create or update that node before this Markdown view, keep status and Evidence synchronized, and do not use a filename suffix as the machine loop's primary state.

## Filename

- Task view: `{YYYYMMDD}_TASK_{FEATURE-ID}_{short-name}_{ready|in-progress|done}.md`
- STREAM: `{YYYYMMDD}_STREAM_{STREAM-ID}_{short-name}_{ready|in-progress|done}.md`
- HANDOFF: `{YYYYMMDD}_HANDOFF_{ready|in-progress|done}.md`

Normalize dynamic components to Windows-safe characters. Do not create free-form reports in `.dodoai/issue/`.

## Template

````markdown
---
type: issue
title: {Title}
tags: [{feature-id}, {phase}]
---

# {Task ID}: {Title}

TaskGraph SoT: `{task-node-path}`.

## Status

- Task: `{task-id}`
- Feature: `{feature-id}`
- Phase: `{DD01|DD02|DD03|DD04|DD05}`
- Status: `{ready|running|blocked|failed|done}`
- Operation: `{operation-id|unresolved (catalog absent)}`
- Agent: `{agent-id|unresolved (catalog absent)}`

## Intent

{One sentence outcome.}

## Inputs

- Spec: `{path-or-ln-uri}`
- TaskGraph: `{task-node-path}`
- MCP route: `{agn.route_next result}`
- CallGraph: `{action result|N/A for docs-only}`

## Done criteria

- `{machine-executable check and expected result}`
- `action: roadmap.sync_gate` → `ok=true`, or the task remains non-done with the exact pre-existing blocker recorded.

## Evidence

- `{command or Action}: {observed result}`

## Remaining findings

- `{finding or none}`
````

## Lifecycle

1. Create the task node with unique ID, Issue/spec refs, executable done criteria, size, success probability, and tick budget.
2. Create this view, stage both explicit paths, acquire the claim/lease, then transition `ready → running`.
3. Change scoped files only after the transition.
4. Write changed files, tests/Actions, Evidence, and remaining findings back to the same node and this view.
5. Run `roadmap.sync_gate`; use `done` only when all applicable gates pass. Otherwise keep `running`, `blocked`, or `failed` truthfully.
