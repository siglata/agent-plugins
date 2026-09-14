# Siglata agent plugin

Portable [Agent Plugins](https://agent-plugins.org/) 1.0.0 package for Siglata. Compatible clients load the plugin directory, its skills, and the hosted MCP connection. See [Build an Agent Plugin](https://agent-plugins.org/plugin-authors/build-an-agent-plugin), [compatible clients](https://agent-plugins.org/compatible-clients), and the [1.0.0 schemas](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).

Plugin v1 is proven on **Cursor** and **Codex**. Other Agent Plugins clients that support skills and Streamable HTTP MCP are installable / spec-compatible. Human install steps for each client live on Siglata: [Connect Siglata to your agent](https://www.siglata.com/docs/connect).

## Package layout

```text
plugins/siglata/
├── plugin.json
├── mcp.json
└── skills/
    ├── siglata/
    ├── siglata-drive/
    ├── siglata-admin/
    └── skill-creator/
```

Invoke **`siglata`**; it loads the specialists needed for your request. For skill authoring alone, invoke **`skill-creator`**.

`.agents/plugins/marketplace.json` is Codex distribution metadata. It sits outside the portable Agent Plugins v1 package, as in the official example guidance.

## Install in Codex

Codex is a proven v1 client. Run these native Codex commands. No npm is required.

```sh
codex plugin marketplace add siglata/agent-plugins
codex plugin add siglata@siglata-agent-plugins
```

Start a new Codex session after installation. Complete Siglata sign-in through the client's OAuth flow when prompted.

Human and agent install guides for Cursor, Codex, and other clients: [Connect Siglata to your agent](https://www.siglata.com/docs/connect).

## Validate

Requires Python 3 with `jsonschema` and `PyYAML`:

```sh
python3 -m pip install jsonschema PyYAML
python3 scripts/validate-plugin.py plugins/siglata
```

Optional: cache downloaded schemas with `--schema-dir /path/to/cache`.

Package health smoke (not a multi-client v1 proof):

```sh
python3 scripts/smoke-client-matrix.py
```

Schemas are pinned under `schemas/1.0.0/` for offline validation; the smoke script compares them to live URLs when network is available.

## Use Siglata

Ask for what you want through the `siglata` skill:

```text
Use siglata to find last month's invoices.
Use siglata to invite Alex as an organization member.
Use skill-creator to create a skill that summarizes meeting notes.
Use siglata to create a skill that summarizes meeting notes.
```

| Request | Routed skill |
| --- | --- |
| Find, upload, download, organize, trash, or restore files and folders | `siglata-drive` |
| Manage members, invitations, and organization roles | `siglata-admin` |
| Create or improve reusable agent skills for any domain (Siglata or general) | `skill-creator` |

Mixed requests load all relevant specialists. You do not need to invoke them separately. The `siglata` router also loads `skill-creator` when the request is skill authoring.

## Connections and permissions

File and organization operations require a Siglata connection and the appropriate organization role. Skill authoring works offline.

- If Siglata tools are missing, enable the plugin and its MCP connection in your client.
- If authentication expires, reconnect through the client's OAuth flow. Keep credentials in the client.
- If access is denied, resolve the reported organization, role, or approval requirement.
