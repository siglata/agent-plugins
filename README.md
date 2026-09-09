# Siglata

Manage Siglata files and organization access, and create reusable agent skills for any domain.

Use the `siglata` skill for all requests. It routes file tasks to Drive, organization tasks to Admin, and skill authoring to Skills. Skill authoring works without a Siglata connection.

## Connect

Install `plugins/siglata` from this repository using an [Agent Plugins compatible client](https://agent-plugins.org/compatible-clients) that supports skills and Streamable HTTP MCP. Sign in to Siglata through the client's OAuth flow.

Installing the whole plugin includes all four skills and the MCP connection configuration. Installing skills alone does not connect the service. If service tools are missing, enable the plugin and its connection in your client. If authentication expires, reconnect through the client's OAuth flow.

