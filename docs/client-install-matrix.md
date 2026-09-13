# Client install matrix (Agent Plugins v1)

Source of client list: [agent-plugins.org/compatible-clients](https://agent-plugins.org/compatible-clients) (`lib/compatible-clients.ts` in agentplugins/agent-plugins-site, 2026-09-13).

Portable package under test: `plugins/siglata` (skills + Streamable HTTP MCP → `https://www.siglata.com/v1/mcp`).

**v1 gate:** every listed client must be able to install / enable / run this package. Rows mark automated smoke vs manual client UI.

## Shared automated gates (all clients)

| Check | Result | How |
| --- | --- | --- |
| Pinned schemas 1.0.0 | PASS | `schemas/1.0.0/{plugin,mcp}.schema.json` |
| `validate-plugin.py plugins/siglata --schema-dir schemas/1.0.0` | PASS | CI + `scripts/smoke-client-matrix.py` |
| MCP Streamable HTTP reachable | PASS | `POST /v1/mcp` → **401/403** (auth required; endpoint live) |
| Skills layout (4 × `SKILL.md`) | PASS | validator |

Run: `python3 scripts/smoke-client-matrix.py`

## Per-client matrix

| Client | Skills | Streamable HTTP | Install / enable | Automated smoke | Manual gap |
| --- | --- | --- | --- | --- | --- |
| VS Code | yes | yes | Install Agent Plugins package from folder/marketplace; enable `chat.plugins.enabled` ([docs](https://code.visualstudio.com/docs/agent-customization/agent-plugins)) | Package gates only | UI marketplace/folder install + OAuth in VS Code |
| Cursor | yes | yes | Customize → Plugins or Marketplace; Agent Plugins format ([docs](https://cursor.com/docs/plugins)) | Package gates only | UI install + OAuth in Cursor |
| GitHub Copilot | yes | yes | Agent Plugins 1.0 `$schema` in `plugin.json`; install via Copilot plugin surfaces ([docs](https://docs.github.com/en/copilot/concepts/agents/about-plugins)) | Package gates only | Copilot app/CLI/cloud UI install + OAuth |
| ChatGPT & Codex | yes | yes | `codex plugin marketplace add siglata/agent-plugins` then `codex plugin add siglata@siglata-agent-plugins` ([docs](https://developers.openai.com/plugins)) | **PASS** install+enable (`media/client-matrix/codex-install.log`) | Interactive OAuth / tools/list in a live Codex session |
| Kiro | yes | yes | Powers follow Agent Plugins; install from marketplace/GitHub ([docs](https://kiro.dev/docs/powers/)) | Package gates only | Kiro IDE/CLI Power install UI |
| Hermes Agent | yes | yes | Portable Agent Plugins v1 packages ([docs](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins#portable-agent-plugins-v1-packages)); dashboard agent-plugins API | Package gates; `hermes plugins install siglata/agent-plugins` clones repo (native-plugin warning) | Enable portable package via Hermes dashboard / documented portable path; OAuth |
| OpenClaw | yes | yes | `openclaw plugins install ./plugins/siglata` (or archive) ([docs](https://docs.openclaw.ai/plugins/bundles)) | **PASS** install+enable; skills+mcp.json present (`media/client-matrix/openclaw-install.log`) | Gateway restart + OAuth against Siglata MCP |
| Grok Bot | yes | yes | Settings → Plugins ([docs](https://docs.x.ai/grok-bot/skills-routines-and-automations)) | Package gates only | Desktop Settings → Plugins UI + enable per Bot |
| NanoClaw | yes | yes | Stamp Agent Plugins directory as template (`plugin.json` + `mcp.json`) ([docs](https://github.com/nanocoai/nanoclaw/blob/main/docs/templates.md)) | Package gates only | Local `nanoclaw.sh` stamp into `templates/` / group |

## Install recipes (copy/paste)

### ChatGPT & Codex (automated)

```sh
codex plugin marketplace add siglata/agent-plugins
codex plugin add siglata@siglata-agent-plugins
codex plugin list
```

### OpenClaw (automated)

```sh
openclaw plugins install ./plugins/siglata
openclaw plugins list   # siglata = enabled bundle
```

### Path / folder clients (VS Code, Cursor, Copilot, Kiro, Grok, NanoClaw, Hermes portable)

Point the client at this repository’s `plugins/siglata` directory (or a release archive of that directory). Do **not** install skills alone — include `plugin.json` + `mcp.json`. Complete Siglata sign-in through the client’s OAuth when the Streamable HTTP MCP connects.

### Hermes notes

`hermes plugins install` targets **native** Hermes plugins (`plugin.yaml` / `__init__.py`). For portable Agent Plugins v1, follow Hermes’ Portable Agent Plugins docs / dashboard agent-plugins install against `plugins/siglata`, not the repo root.

## Evidence

Cloud Agent store: `/cursor/stores/bc-9684df28-e834-4758-8409-c6f5c1ec7950/media/client-matrix/`

| Artifact | Meaning |
| --- | --- |
| `validate-pinned.log` | Schema validation with vendored schemas |
| `mcp-unauth.*` | Prod MCP 401 boundary |
| `codex-*.log` | Codex marketplace + plugin enable |
| `openclaw-*.log` / `openclaw-extension-tree.txt` | OpenClaw bundle install |
| `hermes-*.log` | Hermes native-plugin install attempt + help |
| `*-install.snip.txt` | Snippets from official install docs |
| `compatible-clients.ts` | Snapshot of site client list |
