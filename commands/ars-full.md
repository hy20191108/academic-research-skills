---
disable-model-invocation: true
name: ars-full
description: ARS full pipeline — research → write → review → revise → finalize
---

Trigger the `academic-pipeline` skill.

Invoke `academic-research-skills:academic-pipeline` with `$ARGUMENTS`.
Resolve its SKILL.md from the plugin root and follow that skill.
Mode names select the task, not a fixed sequence of stages.
