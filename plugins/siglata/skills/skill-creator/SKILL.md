---
name: skill-creator
description: >-
  Creates and improves reusable agent skills (SKILL.md) for any domain,
  including Siglata workflows. Use for /skill-creator, "create a skill",
  "write a SKILL.md", "turn this workflow into a skill", or updating an
  existing skill.
---

# Skill creator

Authoring works without a Siglata connection. Require a service connection only for steps that use that service.

## When to use this skill

Use this skill to create or improve a reusable agent skill for any domain.

- Reach here for `/skill-creator`, "create a skill", "write a SKILL.md", "turn this into a skill", or editing an existing skill.
- If the person invoked `siglata` for skill authoring, load this skill and continue here.
- For Siglata files and folders, use [Siglata Drive](../siglata-drive/SKILL.md).
- For members, invitations, and organization administration, use [Siglata Admin](../siglata-admin/SKILL.md).
- Do not put skill-authoring procedures into the drive or admin skills.

## Authoring baseline

Before drafting prose, load the platform skill-authoring guidance when it is available.

- On Claude Code, use `plugin-dev:skill-development`.
- On Codex, use the platform's skill-authoring guidance, or `writing-skills` when present. Keep `name` + `description` frontmatter and progressive disclosure.
- Prefer positive instructions. Delete prose that does not change a decision. Point at structural sources instead of restating them. Delegate to other skills by path.

This skill owns destination choice, Siglata-vs-general placement, verification, and packaging pointers. It does not replace the platform baseline.

## Create or improve a skill

1. Derive the goal, inputs, expected output, and trigger examples from the conversation and existing files. Ask only for missing decisions that change the workflow. Adapt an existing skill when it already covers the task.
2. Use the person's workspace or requested destination, following its skill-directory conventions. Keep changes out of the installed plugin package. Read existing files before updating them and preserve unrelated work.
3. Create `<name>/SKILL.md` with YAML frontmatter. Match `name` to the folder: 1–64 lowercase letters, digits, and single hyphens, with no leading or trailing hyphen. Write a nonempty `description` of at most 1024 characters that states the capability and concrete trigger contexts (slash command, quoted phrases, and nearby tasks that should activate it).
4. Write the shortest complete procedure: required inputs, decisions, actions, expected output, and relevant failure recovery. Include knowledge the agent would otherwise lack. Keep shared rules in one place.
5. Start with Markdown only. Add a script for deterministic work or a reference for substantial detail only when needed. Link bundled files relatively and say when to read or run them. Declare external tools, connections, or skill dependencies explicitly. Keep credentials and machine-specific paths out of the skill.
6. Validate the result as described below, revise it, and deliver the files with the checks actually performed. If the client cannot write files, return the complete content and intended path. Distinguish creating a skill from installing or publishing it.

## Siglata-domain vs general

- **General skills** land in the person's project or personal skills directory. Do not require Siglata MCP. Name triggers for the workflow, not for Siglata.
- **Siglata workflow skills** (Drive, Admin, or other product flows) may live in this plugin only when the person asked to change the plugin itself. Otherwise write them in the workspace and say how they should be packaged later. When the skill calls Siglata, declare the MCP dependency and point at [Siglata](../siglata/SKILL.md) for the shared connection workflow instead of copying it.
- Prefer improving an existing specialist (`siglata-drive`, `siglata-admin`, or this skill) over adding a near-duplicate.

## Verify behavior

- Check frontmatter, folder naming, and bundled links. Keep files inside the delivered skill or plugin package.
- Try a realistic task and a meaningful edge case in fresh contexts using the finished skill. Compare the actual output with the intended result. Check a nearby request that should not activate it.
- Use disposable inputs. Get permission before authentication or external changes. If a required tool or connection is unavailable, complete local authoring and report the service checks as unverified. Base tool instructions on available schemas or authoritative documentation rather than invented operations.
- For service-backed workflows, specify how to handle missing tools, authentication failures, insufficient permissions, and uncertain write outcomes. Load an existing integration skill when it owns those rules rather than duplicating them.

## Packaging references

Read these when format or distribution details are needed. Basic authoring does not require fetching them.

- [Agent Skills specification](https://agentskills.io/specification) defines the skill format.
- [Vercel's skills guide](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context) covers discovery, installation, and sharing.
- [Agent Plugins](https://agent-plugins.org/plugin-authors/build-an-agent-plugin) covers packaging skills with `plugin.json` and optional `mcp.json`. Use it when a plugin is requested. Skill-only installation does not configure its MCP connections.
