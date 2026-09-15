---
name: siglata-drive
description: Manages Siglata Drive files and folders, including server-side Excel sheet reads, relation extract, and filling one period into an existing .xlsx with sheet_write. Use for finding, uploading, downloading, organizing, deleting, or restoring files, and for reading or writing tables on stored workbooks without treating xlsx as download-first.
---

# Siglata Drive

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Find files and folders with `files_list` and `folders_list` inside an `execute` script, then read one with `file_get` or `file_read`. The `search` tool lists operations, not files.
- Follow pagination until the requested set is covered. Resolve ambiguous names before making changes.
- Start an upload with `upload_begin` and complete the transfer it describes, or write small contents directly with `file_write`. For `.xlsx`, pass `blob` (base64), not `text`. If the client cannot transfer bytes, explain what it needs. An upload is complete when the server returns the saved file or revision. Use `completed.file.id` as the workbook `fileId`, not the upload id.
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

## Many inputs to one period in an existing workbook

Use this when the person asks to fill this month (or period) into a workbook that already has other months. Keep uploads and downloads on the blob path above. Do not download sources to parse them locally. Do not assume DuckDB or SQL aggregation. Do not invent a second write op. `sheet_write` is the patch path.

Needs `files:read` for scout, extract, and verify reads. Needs `files:write` for upload and `sheet_write`. If `search` does not mount write ops, report the scope gap and stop.

1. Resolve every input workbook `fileId` and the target workbook `fileId` (`files_list` / `file_get`, or `file_write` / `upload_*` for new files). The target is the existing out workbook that already contains other periods.
2. Scout with `sheet_list` and `sheet_read`. When layouts match, scout one file and reuse the same `sheet`, A1 `range`, `headerRow`, and `columns` on every later section (swap only `workbookFileId`). When layouts differ, scout each layout and use a different section shape.
3. Call `relation_extract` with one section per input (up to 32 per call). Read rows from the extract outcomes in the same script. Use `persist: true` only when you will call `relation_query` later.
4. Aggregate in CallScript JavaScript over those outcomes (or over paged `relation_query` rows). Do not use `relation_query` for cross-file `SUM`, `GROUP BY`, or joins. It filters, projects, orders, and pages one persisted section only.
5. Scout the target with `sheet_read` to locate this month's A1 window only. Call `sheet_write` on that existing target `fileId` with that one range and a dense `cells` matrix. `sheet_write` patches that rectangle, leaves every cell outside the window unchanged (other months stay), and mints a new edition. The source `fileId` stays unchanged. Later reads and download use the write result's `file.id`.
6. Verify with `sheet_read` on that edition for the patched range and for at least one untouched period range. Then `file_download` the edition when the person needs the file.

Patch windows that hit formula cells fail. Word, PDF, and PowerPoint have no structured write ops. Prefer one `execute` script for extract, reduce, and write when those steps share values.
