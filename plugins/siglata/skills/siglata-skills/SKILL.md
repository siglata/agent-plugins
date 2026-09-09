---
name: siglata-skills
description: Creates and improves reusable agent skills for any domain. Use when asked to create a skill, update a SKILL.md, or turn a repeated workflow into a skill.
---

# Siglata Skills

Authoring works without a Siglata connection. Require a service connection only for steps that use that service.

## Create or improve a skill

1. Derive the goal, inputs, expected output, and trigger examples from the conversation and existing files. Ask only for missing decisions that change the workflow. Adapt an existing skill when it already covers the task.
2. Use the person's workspace or requested destination, following its skill-directory conventions. Keep changes out of the installed plugin. Read existing files before updating them and preserve unrelated work.
3. Create `<name>/SKILL.md` with YAML frontmatter. Match `name` to the folder: 1–64 lowercase letters, digits, and single hyphens, with no leading or trailing hyphen. Write a nonempty `description` of at most 1024 characters that states the capability and concrete trigger contexts.
4. Write the shortest complete procedure: required inputs, decisions, actions, expected output, and relevant failure recovery. Include knowledge the agent would otherwise lack. Prefer positive instructions and explain non-obvious constraints. Keep shared rules in one place.
5. Start with Markdown only. Add a script for deterministic work or a reference for substantial detail only when needed. Link bundled files relatively and say when to read or run them. Declare external tools, connections, or skill dependencies explicitly. Keep credentials and machine-specific paths out of the skill.
6. Validate the result as described below, revise it, and deliver the files with the checks actually performed. If the client cannot write files, return the complete content and intended path. Distinguish creating a skill from installing or publishing it.

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
