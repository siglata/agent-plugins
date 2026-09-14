---
name: siglata-drive
description: Manages Siglata Drive files and folders. Use for finding, uploading, downloading, organizing, deleting, or restoring files in Siglata.
---

# Siglata Drive

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Find files and folders with `files_list` and `folders_list` inside an `execute` script, then read one with `file_get` or `file_read`. The `search` tool lists operations, not files.
- Follow pagination until the requested set is covered. Resolve ambiguous names before making changes.
- Start an upload with `upload_begin` and complete the transfer it describes, or write small contents directly with `file_write`. If the client cannot transfer bytes, explain what it needs. An upload is complete when the server returns the saved file or revision.
- Read bytes through the `siglata:///files/{fileId}` resource, which needs the `files:read` scope. Deliver them as a usable file or client attachment.
- Move files into the requested folder. Omit the destination folder only when moving to the root.
- Use trash for deletion. Permanently purge only when explicitly requested.
- Trashing a folder does not require it to be empty, and each file inside keeps its own trashed or active state. Trash or restore a file directly when the person asks for that file.
- For sharing or restricted-object access, use `grants_list`, `grant_create`, and `grant_revoke` via `search` then `execute`. Those ops are object ACL shares, not the OAuth MCP grant. For organization roles or leaving an org, use the [admin skill](../siglata-admin/SKILL.md).
