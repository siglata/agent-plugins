---
name: files
description: Manage SIGLATA Organization files through the remote MCP tools, with the Rust CLI as a local fallback for hosts without the MCP connection.
compatibility: Requires an enabled SIGLATA remote MCP connection for the primary path, or the `siglata` Rust CLI on PATH for the local fallback. Network access to the SIGLATA API.
---

Use the connected SIGLATA MCP server first. Its `search` tool finds Organization files and its `execute` tool performs file actions. Follow each tool's input schema; do not translate a tool call into a shell command or invent an argument.

If the SIGLATA MCP tools are unavailable, check for the local CLI before taking a file action:

- POSIX shell: `command -v siglata`
- PowerShell: `Get-Command siglata -ErrorAction SilentlyContinue`

Use the CLI fallback below when that check finds `siglata`. If neither the MCP tools nor the CLI is available, stop and ask the operator to run `iex (irm https://www.siglata.com/mcp.ps1)` on Windows or connect the SIGLATA MCP server in the host. The Windows script downloads no executable and does not ask the operator to weaken Smart App Control, SmartScreen, Defender, or Gatekeeper.

## Session

With MCP, call `search` for the current Organization context when the host exposes that operation. The server keeps the session and Organization scope; never ask the operator to paste a token into a prompt.

With the CLI fallback:

```bash
siglata org current
```

When that command reports no credential, run `siglata login` and let the operator finish PKCE in the system browser. Do not pass `--token` on a human login; that flag is for CI.

To switch Organization with the CLI:

```bash
siglata org list
siglata org use ORG
```

`siglata status` reports whether a credential is stored (no secret is printed). `siglata logout` clears it.

## MCP file actions

Use the server's `search` tool to find or list captures. Use `execute` for the requested action:

- upload the local path supplied by the operator;
- retrieve a capability download URL for a capture;
- soft-delete a capture after confirming its id.

The MCP tool result is authoritative. Keep capture ids from the result instead of guessing from filenames. Treat a capability URL as a secret and pass it directly to a downloader without printing it.

## CLI fallback: upload

```bash
siglata files upload PATH
```

An Organization is created with one Feed. **Omit `--feed` when the Organization has one Feed** — the CLI calls `GET /feeds` and selects that single id. Pass `--feed FEED` only when the Organization has more than one Feed (the CLI refuses with `feed-required` if you omit it then), or when you already know which Feed to target.

```bash
siglata files upload ./invoice-jan.pdf --feed feed_abc123
```

Optional flags:

- `--filename NAME` — store a different name than the path's final component. Required when the path name is empty or not printable Latin-1 (code points `U+0020`–`U+00FF`). Em-dashes, CJK, and other non–Latin-1 characters are refused with `filename-invalid`.
- `--folder FOLDER` — file into an existing folder id. A missing folder is refused `no-such-folder`.

One invocation uploads the bytes. Do not split the work into declare/commit.

Rules the CLI enforces before or during the call:

- Empty files are refused: `cannot commit an empty upload`.
- Bodies larger than 32 MiB (33 554 432 bytes) are refused `capture-too-large`.
- The same bytes uploaded twice create two captures that share a content hash. They are not replaced and not collapsed to one row.
- Extension is not filtered at upload (`.csv`, `.pdf`, `.txt`, `.exe`, and others all commit if the rest of the request is valid).

JSON upload success looks like `{"report":{"captureId":"…","feedId":"…","filename":"…"}}`. Use `report.captureId` as the file id for later steps.

## CLI fallback: list

```bash
siglata files list
```

Add `--json` when a later step needs structured rows. Rows are under `captures` (each has `id`, `filename`, `contentHash`, …). Prefer `--json` when you will call `get` or `delete` next so you copy the id without guessing.

If catalogue search cannot run, the CLI falls back to `GET /captures` and still exits non-zero only on a real transport or auth failure.

## CLI fallback: retrieve (this is download)

There is no `siglata files download`. **Download is `siglata files get FILE_ID`.**

```bash
siglata files get FILE_ID
```

The CLI prints the capability download URL as `href: https://...`. The JSON form is `{"href":"https://..."}`. The CLI does not write file bytes to stdout.

When the agent needs the bytes, fetch that URL (no extra auth header — the query string is the capability):

```bash
url="$(siglata files get FILE_ID | sed -n 's/^href: //p')"
curl --fail --silent --show-error --location "$url" --output ./downloaded-file
```

Treat the URL query as a capability secret. Pass it directly to the downloader and do not print it.

If `files get` exits non-zero with `catalogue-unavailable` (often `LoaderUnbound` or `RunnerUnconfigured`), the deployment cannot mint a share link right now. Say that to the operator; do not invent a `download` subcommand and do not open a second MCP connection to work around it.

## CLI fallback: delete

```bash
siglata files delete FILE_ID
```

When a finalized Document still depends on the file, the API soft-deletes it and the CLI reports that outcome. Read the output before telling the operator the file is gone.

If delete exits non-zero with `catalogue-unavailable`, the delete did not run — do not claim the file is gone.

## Quick map

| Operator asks         | MCP primary                       | CLI fallback                                      |
| --------------------- | --------------------------------- | ------------------------------------------------- |
| Sign in               | Use the connected server session  | `siglata login` then `siglata status`             |
| Which org             | `search` for Organization context | `siglata org list` / `siglata org use ORG`        |
| Upload a file         | `execute` upload                  | `siglata files upload PATH`                       |
| What arrived          | `search` captures                 | `siglata files list --json`                       |
| Download / get a link | `execute` retrieve                | `siglata files get FILE_ID` then HTTPS-fetch href |
| Remove a file         | `execute` soft-delete             | `siglata files delete FILE_ID`                    |
