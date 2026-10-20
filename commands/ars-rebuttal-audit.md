---
disable-model-invocation: true
name: ars-rebuttal-audit
description: ARS academic-paper `rebuttal-audit` mode — QA an existing rebuttal draft against reviewer comments
---

Trigger the `academic-paper` skill in `rebuttal-audit` mode.

Invoke `academic-research-skills:academic-paper` with `rebuttal-audit $ARGUMENTS`.
Resolve its SKILL.md from the plugin root and follow that skill.
Mode names select the task, not a fixed sequence of stages.
