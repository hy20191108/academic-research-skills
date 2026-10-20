import { existsSync, readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const commandPattern = /^\/(ars-[a-z0-9-]+)(?:\s+([\s\S]*))?$/;
const skillNames = ["deep-research", "academic-paper", "academic-paper-reviewer", "academic-pipeline", "sr-screener"];
const skillPattern = new RegExp(`^/skill:(${skillNames.join("|")})(?:\\s|$)`);
const stateEntryType = "ars-pi-state";
const orchestrationPattern = /subagent|workflow|parallel[-_ ]agent|multi[-_ ]agent/i;
const webPattern = /websearch|web[-_ ]search|brave[-_ ]search|webfetch|web[-_ ]fetch|page[-_ ]retrieval/i;

function uniqueMatches(items, pattern) {
  return [...new Set(items.filter((item) => pattern.test(item.search)).map((item) => item.label))];
}

const xmlEntities = {
  amp: "&",
  lt: "<",
  gt: ">",
  quot: '"',
  apos: "'",
};

function decodeXml(text) {
  return text.replace(/&(amp|lt|gt|quot|apos);/g, (_match, entity) => xmlEntities[entity]);
}

function canonicalPath(path) {
  try {
    return realpathSync(path);
  } catch {
    return undefined;
  }
}

const skillLocations = new Set(
  skillNames
    .map((name) => canonicalPath(resolve(repoRoot, name, "SKILL.md")))
    .filter((location) => location !== undefined),
);

// Hide this package’s exact skill listings while ARS is inactive.
function hideArsSkills(systemPrompt) {
  if (Array.isArray(systemPrompt)) return systemPrompt.map(hideArsSkills);
  return systemPrompt.replace(
    /(?:\r?\n)?[ \t]*<skill>(?:(?!<skill>)[\s\S])*?<\/skill>/g,
    (block) => {
      const location = block.match(/<location>([^<]+)<\/location>/)?.[1];
      const canonicalLocation = location ? canonicalPath(decodeXml(location)) : undefined;
      return canonicalLocation && skillLocations.has(canonicalLocation) ? "" : block;
    },
  );
}

async function probe(pi, command, args) {
  try {
    const result = await pi.exec(command, args, { timeout: 3000 });
    if (result.code !== 0) return "missing";
    return (result.stdout || result.stderr).trim().split("\n")[0] || "available";
  } catch {
    return "missing";
  }
}

const compatibility = `
## Academic Research Skills compatibility for Pi

Apply only while an ARS skill or /ars-* prompt is active.
Read the selected SKILL.md; resolve its resources from ${repoRoot}.
Use the current session's equivalent tools and model.
Supporting files are optional; do not reinstate the upstream fixed workflow.
Delegate only when requested and supported; shared context is not independent review.
Use available search tools when needed; disclose unavailable or unverified sources.
Claude hooks do not run in Pi. Do not claim their write-scope guard is active.
`;

export default function (pi) {
  let arsActive = false;

  const setArsActive = (active) => {
    if (arsActive === active) return;
    arsActive = active;
    pi.appendEntry(stateEntryType, { active });
  };

  const restoreArsState = (ctx) => {
    const state = ctx.sessionManager.getBranch()
      .filter((entry) => entry.type === "custom" && entry.customType === stateEntryType)
      .pop();
    arsActive = state?.data?.active === true;
  };

  pi.on("session_start", (_event, ctx) => {
    restoreArsState(ctx);
  });

  pi.on("session_tree", (_event, ctx) => {
    restoreArsState(ctx);
  });

  pi.on("input", (event) => {
    const match = event.text.match(commandPattern);
    if (!match) {
      if (skillPattern.test(event.text)) setArsActive(true);
      return { action: "continue" };
    }

    const commandPath = resolve(repoRoot, "commands", `${match[1]}.md`);
    if (!existsSync(commandPath)) return { action: "continue" };

    setArsActive(true);
    const raw = readFileSync(commandPath, "utf8");
    const body = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "").trim();
    const args = match[2]?.trim() ?? "";
    const hasArgumentPlaceholder = body.includes("$ARGUMENTS") || body.includes("$@");
    const executableBody = body.replace(
      /\b(python3?|bash|sh) scripts\/([^\s`]+)/g,
      (_match, command, script) => `${command} "${repoRoot}/scripts/${script}"`,
    );
    const expanded = executableBody.replace(/\$ARGUMENTS|\$@/g, () => args);
    const commandText = args && !hasArgumentPlaceholder
      ? `${expanded}\n\nUser request / arguments:\n${args}`
      : expanded;
    const skillName = body.match(/^Trigger the `([^`]+)` (?:skill|orchestrator)/m)?.[1];
    const text = skillName ? `/skill:${skillName} ${commandText}` : commandText;

    return { action: "transform", text };
  });

  pi.registerCommand("ars-pi-start", {
    description: "Enable ARS compatibility and automatic skill selection in this session",
    handler: async (_args, ctx) => {
      setArsActive(true);
      ctx.ui.notify("ARS compatibility instructions enabled for this session", "info");
    },
  });

  pi.registerCommand("ars-pi-stop", {
    description: "Disable ARS compatibility and automatic skill selection in this session",
    handler: async (_args, ctx) => {
      setArsActive(false);
      ctx.ui.notify("ARS compatibility instructions disabled for this session", "info");
    },
  });

  pi.registerCommand("ars-pi-doctor", {
    description: "Check optional Pi capabilities and local ARS runtime dependencies",
    handler: async () => {
      const activeTools = new Set(pi.getActiveTools());
      const tools = pi.getAllTools().map((tool) => ({
        label: `${activeTools.has(tool.name) ? "active tool" : "installed tool"}: ${tool.name}`,
        search: `${tool.name} ${tool.description}`,
      }));
      const commands = pi.getCommands()
        .filter((command) => !command.name.startsWith("ars-") && !command.name.startsWith("skill:academic-"))
        .map((command) => ({
          label: `${command.source}: /${command.name}`,
          search: `${command.name} ${command.description ?? ""}`,
        }));
      const candidates = [...tools, ...commands];
      const orchestration = uniqueMatches(candidates, orchestrationPattern);
      const web = uniqueMatches(candidates, webPattern);
      const python = await probe(pi, "python3", ["--version"]);
      const pyyaml = await probe(pi, "python3", ["-c", "import yaml; print(f'PyYAML {yaml.__version__}')"]);
      const pandoc = await probe(pi, "pandoc", ["--version"]);
      const tectonic = await probe(pi, "tectonic", ["--version"]);
      const sandbox = pi.getCommands().some((command) => command.name === "sandbox")
        ? `detected; allow read access to ${repoRoot} when running outside the checkout`
        : "not detected";
      const format = (matches) => matches.length > 0 ? matches.join(", ") : "none; sequential/degraded mode";
      const report = [
        "ARS Pi doctor",
        `Repository: ${repoRoot}`,
        `Orchestration: ${format(orchestration)}`,
        `Web retrieval: ${format(web)}`,
        `Python: ${python}`,
        `PyYAML: ${pyyaml}`,
        `Pandoc: ${pandoc}`,
        `Tectonic: ${tectonic}`,
        `Sandbox: ${sandbox}`,
        "Claude hooks: unavailable in Pi; write-scope enforcement remains prompt-level",
      ].join("\n");

      pi.sendMessage({ customType: "ars-pi-doctor", content: report, display: true });
    },
  });

  pi.on("before_agent_start", (event) => {
    const options = event.systemPromptOptions;
    if (options?.sections && options.forceSystemPrompt === undefined) {
      // Compose with Pi's structured prompt instead of freezing a rendered snapshot.
      if (arsActive) {
        options.sections.ars_compatibility = compatibility;
      } else {
        options.skills = options.skills.filter((skill) => {
          const location = canonicalPath(skill.filePath);
          return !location || !skillLocations.has(location);
        });
        delete options.sections.ars_compatibility;
      }
      return;
    }

    // Older runners and earlier complete-prompt overrides require the rendered fallback (#880).
    if (!arsActive) return { systemPrompt: hideArsSkills(event.systemPrompt) };
    const sp = event.systemPrompt;
    return { systemPrompt: Array.isArray(sp) ? [...sp, compatibility] : `${sp}\n${compatibility}` };
  });
}
