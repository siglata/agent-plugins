# Siglata

Manage Siglata files and organization access, and create reusable agent skills for any domain.

Use the `siglata` skill for all requests. It routes file tasks to Drive, organization tasks to Admin, and skill authoring to Skills. Skill authoring works without a Siglata connection.

## Install in Codex

Run these native Codex commands. No npm is required.

```sh
codex plugin marketplace add siglata/agent-plugins
codex plugin add siglata@siglata-agent-plugins
```

Start a new Codex session after installation. Complete Siglata sign-in through the client's OAuth flow when prompted.

## Other compatible clients

Install `plugins/siglata` from this repository using an [Agent Plugins compatible client](https://agent-plugins.org/compatible-clients) that supports skills and Streamable HTTP MCP. Sign in to Siglata through the client's OAuth flow.

Installing the whole plugin includes all four skills and the MCP connection configuration. Installing skills alone does not connect the service. If service tools are missing, enable the plugin and its connection in your client. If authentication expires, reconnect through the client's OAuth flow.

