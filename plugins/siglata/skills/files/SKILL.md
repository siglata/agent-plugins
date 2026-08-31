---
name: files
description: Manage Siglata Organization files through the hosted MCP server.
compatibility: Requires Codex 0.147 or newer and an authorized Siglata MCP connection.
license: Apache-2.0
---

Use the connected Siglata MCP server for every file action. Do not replace a tool call with a shell command, invent arguments, or ask the operator to paste a token.

Start with the `context` tool when it is available. Confirm the active Organization and role before reading or changing files. Use `search` for read-only work.
Read `catalogue.md` for the live operation names and argument and result schemas. Keep those schemas out of this workflow entry point.

Use `execute` for mutations. Submit one operation batch per intent in `plan` mode first. Review the returned mutations, input revisions, and plan digest, then submit the same batch in `apply` mode with the digest and a fresh idempotency key. Reuse that key when retrying an interrupted apply. If the plan is stale, plan again instead of forcing the apply.

Keep aliases and references inside the batch. References may target only outputs from earlier steps. Let the server validate operation arguments and report its stable error code.

Treat download URLs as capability secrets. Pass them directly to the requested downloader and never print or expose them. File attachments supplied by Codex transit OpenAI file storage before the hosted server receives them.
