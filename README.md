# Siglata agent plugin

Portable [Agent Plugins](https://agent-plugins.org/) 1.0.0 package for Siglata. Compatible clients load the plugin directory, its skills, and the hosted MCP connection. See [Build an Agent Plugin](https://agent-plugins.org/plugin-authors/build-an-agent-plugin), [compatible clients](https://agent-plugins.org/compatible-clients), and the [1.0.0 schemas](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).

## Package layout

```text
plugins/siglata/
├── plugin.json
├── mcp.json
└── skills/
    ├── siglata/
    ├── siglata-drive/
    ├── siglata-admin/
    └── siglata-skills/
```

Invoke **`siglata`**; it loads the specialists needed for your request.

`.agents/plugins/marketplace.json` is Codex distribution metadata. It sits outside the portable Agent Plugins v1 package, as in the official example guidance.

## Install in Codex

Codex is a proven v1 client. Run these native Codex commands. No npm is required.

```sh
codex plugin marketplace add siglata/agent-plugins
codex plugin add siglata@siglata-agent-plugins
```

Start a new Codex session after installation. Complete Siglata sign-in through the client's OAuth flow when prompted.

Human and agent install guides for Codex and other clients: [Connect Siglata to your agent](https://www.siglata.com/docs/connect).

## Validate

Requires Python 3 with `jsonschema` and `PyYAML`:

```sh
python3 -m pip install jsonschema PyYAML
python3 scripts/validate-plugin.py plugins/siglata
```

Optional: cache downloaded schemas with `--schema-dir /path/to/cache`.

## Use Siglata

Ask for what you want through the `siglata` skill:

```text
Use siglata to find last month's invoices.
Use siglata to invite Alex as an organization member.
Use siglata to create a skill that summarizes meeting notes.
```

| Request | Routed skill |
| --- | --- |
| Find, upload, download, organize, trash, or restore files and folders | `siglata-drive` |
| Manage members, invitations, and organization roles | `siglata-admin` |
| Create or improve reusable agent skills for any domain | `siglata-skills` |

Mixed requests load all relevant specialists. You do not need to invoke them separately.

## Connections and permissions

File and organization operations require a Siglata connection and the appropriate organization role. Skill authoring works offline.

- If Siglata tools are missing, enable the plugin and its MCP connection in your client.
- If authentication expires, reconnect through the client's OAuth flow. Keep credentials in the client.
- If access is denied, resolve the reported organization, role, or approval requirement.

## Other compatible clients

Install `plugins/siglata` from this repository using an [Agent Plugins compatible client](https://agent-plugins.org/compatible-clients) that supports skills and Streamable HTTP MCP. Sign in to Siglata through the client's OAuth flow.

For MCP-only setup without this plugin package, use the Siglata docs hub [Connect Siglata to your agent](https://www.siglata.com/docs/connect). Cursor and Codex are proven for v1. ChatGPT Desktop, Claude Desktop, and VS Code are listed as installable / spec-compatible.

Install the whole plugin to include its skills and MCP connection configuration. Installing skills alone does not connect the service. Installation and enablement are controlled by each client; Agent Plugins defines the portable package format.
