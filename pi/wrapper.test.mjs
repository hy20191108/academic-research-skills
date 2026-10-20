import assert from "node:assert/strict";
import test from "node:test";
import wrapper from "./wrapper.js";

function handler() {
  const events = new Map();
  wrapper({ on: (name, fn) => events.set(name, fn) });
  assert.deepEqual([...events.keys()], ["before_agent_start"]);
  return events.get("before_agent_start");
}

test("独自コマンドや入力変換を登録せず，標準の選択を保つ", () => {
  const skills = [{ name: "deep-research", filePath: "/external/SKILL.md" }];
  const options = { skills, sections: { mcp: "既存の指示" } };
  handler()({ systemPromptOptions: options });
  assert.equal(options.skills, skills);
  assert.equal(options.sections.mcp, "既存の指示");
  assert.match(options.sections.ars_compatibility, /ClaudeのフックはPiでは動かない/);
  assert.equal(options.forceSystemPrompt, undefined);
});

for (const prompt of ["先行する拡張の指示", ["先行する拡張の指示"]]) {
  test(`既存の指示と形式を保つ: ${Array.isArray(prompt)}`, () => {
    const result = handler()({ systemPrompt: prompt, systemPromptOptions: { sections: {}, forceSystemPrompt: prompt } });
    if (Array.isArray(prompt)) {
      assert.deepEqual(result.systemPrompt.slice(0, -1), prompt);
      assert.equal(prompt.length, 1);
    } else assert.ok(result.systemPrompt.startsWith(prompt));
  });
}
