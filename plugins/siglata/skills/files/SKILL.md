---
name: files
description: Read, search and change Siglata Organization files through the hosted Siglata MCP server, planning every mutation before applying it.
license: Apache-2.0
compatibility: Any client that loads Agent Plugins 1.0.0 and speaks Streamable HTTP MCP. Verified against Codex 0.146 or newer with an authorized Siglata connection.
---

# Siglata files

Every file action goes through the connected Siglata MCP server. Do not substitute a shell command, do not invent arguments, and do not ask the person to paste a token. Access is arranged by the client, never by this package.

## Start with context

Call `context` first. It reports the active Organization, the caller's role, the operation registry API version and the current limits. Confirm the Organization and the role before reading or changing anything.

## Write one script per intent

Both `search` and `execute` take a `script`: a short JavaScript program that calls operations, written the way the tool description shows. The server parses it into an inert plan and never runs it as code. Only registered operations execute. Every problem in the script is reported at once, before anything runs, with the spelling that fixes it.

- Call an operation with `await`, for example `const page = await files.list({ limit: 20 });`.
- Derive values between calls with plain expressions: `const stale = page.files.filter(f => f.tags.includes("draft"));`.
- Fan out over a bounded list with `Promise.all(items.slice(0, 10).map(item => files.trash({ file: item.id })))`. The visible `slice` is the bound; an unbounded fan-out is refused.
- End early with `if (stale.length === 0) return { trashed: 0 };` and return the run's result as the last statement.
- `Date` is not available; a plan must apply exactly as it was planned.
- Attached bytes are bound as `attachments` and referenced by index, for example `attachments[0]`.

The server enforces the budget: at most 50 calls per script, arguments of at most 64 KiB per call, 20 attachments per call.

## Read with search

Use `search` for read-only work. A script whose every call is a read runs at once and returns each step's output and the run's result. A write in a `search` script is refused before anything runs.

## Change with execute

Use `execute` for every mutation. Submit the script in `plan` mode first. Read back the mutations, the observed inputs and the plan digest, then submit the same script in `apply` mode with that digest and a fresh idempotency key. Reuse the same key when retrying an interrupted apply. When a plan is stale, plan again rather than forcing the apply.

Let the server validate operation arguments and report its stable error code rather than guessing locally. A refusal names the step id that failed.

## Operation reference

`operations.md` beside this file lists every operation, its kind, the role it needs, and its input and output schemas. Read it when you need an operation name or an argument shape. It is generated from the live operation registry, so it is the authority; do not restate its schemas here.

## Attached bytes transit OpenAI first

A file the person drops into ChatGPT is uploaded to OpenAI file storage before Siglata ever sees it. Codex rewrites the path into a `download_url`, Siglata fetches those bytes, verifies the SHA-256, the sniffed container and the size, and only then stores them in Siglata. Tell the person this when they ask where their file went, and never claim the file went straight from their machine to Siglata.

## Download URLs are secrets

A download URL is a capability. Pass it straight to the downloader that asked for it. Never print it, echo it back, or store it anywhere the person can read it.
