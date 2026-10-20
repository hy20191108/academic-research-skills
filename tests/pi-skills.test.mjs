import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const packageRoot = process.env.PI_CODING_AGENT_ROOT;
const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

test("標準のスキル読込みで全登録を自動選択の対象にする", {
  skip: !packageRoot && "PI_CODING_AGENT_ROOTでPiの場所を指定する",
}, async () => {
  const { loadSkillsFromDir } = await import(pathToFileURL(resolve(packageRoot, "dist/core/skills.js")).href);
  const manifest = JSON.parse(readFileSync(resolve(repoRoot, "package.json"), "utf8"));
  const names = [];
  for (const dir of manifest.pi.skills) {
    const result = loadSkillsFromDir({ dir: resolve(repoRoot, dir), source: "test" });
    assert.deepEqual(result.diagnostics, []);
    assert.equal(result.skills.length, 1);
    assert.equal(result.skills[0].disableModelInvocation, false);
    names.push(result.skills[0].name);
  }
  assert.equal(new Set(names).size, 5);
});
