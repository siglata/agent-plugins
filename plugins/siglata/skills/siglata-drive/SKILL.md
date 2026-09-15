---
name: siglata-drive
description: Manages Siglata Drive files and folders, including server-side Excel sheet reads and relation extract. Use for finding, uploading, downloading, organizing, deleting, or restoring files, and for reading tables from stored .xlsx workbooks without downloading them.
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

## Excel workbooks (`.xlsx`)

Do not use `file_read` or download when the person wants sheet contents or tabular data from a stored `.xlsx`. Those ops return opaque bytes. Use the sheet and relation operations under `files:read` instead. Workbook bytes stay on the server.

1. Resolve the workbook `fileId` (upload or `files_list` / `file_get`).
2. Call `sheet_list({ fileId })` to name worksheets.
3. Call `sheet_read({ fileId, sheet, range })` with an A1 range (for example `A1:D50`) to inspect headers and shape. Prefer a bounded range. Check `truncated`.
4. Call `relation_extract` with one or more named sections. Each section needs `id`, `relationName`, and `source` (`workbookFileId`, `sheet`, `range`, `headerRow`). Optional `columns` map header text to field names and `typeHint`. Set `persist: true` when the person will query the table later.
5. Call `relation_query` only after a successful persist. Select with `relationName` or `sectionKey`. Use `where`, `columns`, `orderBy`, `cursor`, and `limit` as needed. The workbook is not reopened.

Discover exact arguments with `search`. Run the steps in one `execute` script when later steps need earlier results. Non-xlsx files fail sheet and relation ops. Legacy `.xls`, ODS, and CSV are not workbook ops.
