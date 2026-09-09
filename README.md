# Siglata agent plugin

Manage Siglata files and organization access, and create reusable agent skills from your AI client.

This [Agent Plugins](https://agent-plugins.org/) package bundles four skills and the hosted Siglata MCP connection configuration. Invoke **`siglata`**; it loads the specialists needed for your request.

## Install in Codex

Run these native Codex commands. No npm is required.

```sh
codex plugin marketplace add siglata/agent-plugins
codex plugin add siglata@siglata-agent-plugins
```

Start a new Codex session after installation. Complete Siglata sign-in through the client's OAuth flow when prompted.

## Use Siglata

Ask for what you want through the `siglata` skill:

```text
Use siglata to find last month's invoices.
Use siglata to invite Alex as an organization member.
Use siglata to create a skill that summarizes meeting notes.
```

| Request | Routed skill |
| --- | --- |
| Find, upload, download, organize, tag, trash, or restore files and folders | `siglata-drive` |
| Manage members, invitations, roles, or organization lifecycle | `siglata-admin` |
| Create or improve reusable agent skills for any domain | `siglata-skills` |

Mixed requests load all relevant specialists. You do not need to invoke them separately.

## Connections and permissions

File and organization operations require a Siglata connection and the appropriate organization role. Skill authoring works offline.

- If Siglata tools are missing, enable the plugin and its MCP connection in your client.
- If authentication expires, reconnect through the client's OAuth flow. Keep credentials in the client.
- If access is denied, resolve the reported organization, role, or approval requirement.
- Some access changes require confirmation in the Siglata app. The agent reports them as pending until the service confirms completion.

## Other compatible clients

Install `plugins/siglata` from this repository using an [Agent Plugins compatible client](https://agent-plugins.org/compatible-clients) that supports skills and Streamable HTTP MCP. Sign in to Siglata through the client's OAuth flow.

Install the whole plugin to include its skills and MCP connection configuration. Installing skills alone does not connect the service. Installation and enablement are controlled by each client; Agent Plugins defines the portable package format.

