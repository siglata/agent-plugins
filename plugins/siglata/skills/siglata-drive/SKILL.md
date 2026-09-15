---
name: siglata-drive
description: Manages Siglata Drive files and folders, including multi-workbook Excel fill (heterogeneous .xlsx extract, CallScript reduce, sheet_write patch or export). Use for finding, uploading, downloading, organizing, deleting, or restoring files, and for reading or writing tables on stored workbooks without treating xlsx as download-first.
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

## Multi-Excel fill (extract → process → patch or export)

Use this when the person wants results from several different `.xlsx` inputs written into one existing output workbook (or downloaded as that edition). The common case is filling one period while other months stay intact. The same loop covers one or more A1 patches into an existing OUT workbook.

Keep uploads and downloads on the blob path above. Do not download sources to parse them locally. Do not assume DuckDB or SQL aggregation. Do not invent a second write op. `sheet_write` is the patch path. Prefer one `execute` script for extract, reduce, and write when those steps share values.

Needs `files:read` for scout, extract, and verify reads. Needs `files:write` for upload and `sheet_write`. If `search` does not mount write ops, report the scope gap and stop.

### 1. Resolve inputs and the OUT workbook

Resolve every input workbook `fileId` and the target workbook `fileId` (`files_list` / `file_get`, or `file_write` / `upload_*` for new files). Inputs may use different sheet names, header rows, and column layouts. The target is the existing OUT workbook the person already has (often with other periods already filled).

### 2. Scout each layout

Call `sheet_list` and `sheet_read` on the inputs. When layouts match, scout one file and reuse the same `sheet`, A1 `range`, `headerRow`, and `columns` on every later section (swap only `workbookFileId`). When layouts differ, treat each shape as its own format: scout that file and build a different section shape (same `relationName` is fine). Do not force one section shape across mismatched workbooks. Reusing Layout A `columns[].header` binds on Layout B yields section error `header_mismatch`. For pt-BR sheets, bind the trimmed header text exactly, for example `columns: [{ header: "Quantidade", field: "units" }, { header: "Região", field: "region" }]` on a `Vendas` sheet. Do not translate headers.

### 3. Relation extract across those shapes

Call `relation_extract` with one section per input table (up to 32 per call). Split into more calls when you need more than 32 sections. Read rows from the extract outcomes in the same script. Use `persist: true` only when you will call `relation_query` later. Sheet and relation ops accept `.xlsx` only. Legacy `.xls`, ODS, and CSV fail. Word, PDF, and PowerPoint have document read ops, not `relation_extract`, and have no structured write ops.

### 4. Process in CallScript

Reduce in CallScript JavaScript over those outcomes (or over paged `relation_query` rows). Build the dense `cells` matrix the OUT window needs. CallScript rejects unbounded `while`, `for..of` over `rows`, and reassignment. Prefer fixed-index sums (or a bounded `Promise.all` tool fan-out). Do not use `relation_query` for cross-file `SUM`, `GROUP BY`, or joins. It filters, projects, orders, and pages one persisted section only.

### 5. Patch the existing OUT workbook

Scout the target with `sheet_read` to locate each A1 window you will change (for period fill, only that month's rectangles). Call `sheet_write` once on that existing target `fileId` with a non-empty `patches` array. Each entry is `{ sheet, range, cells }` with a dense `cells` matrix for that range. Multi-sheet and non-contiguous ranges belong in the same call. A one-range period fill is a one-element `patches` array.

`sheet_write` patches every listed range, leaves every cell outside those windows unchanged (other months stay), and mints one new edition. The source `fileId` stays unchanged. Later reads and download use `written.file.id`. The receipt is `written.patches[n]` in input order.

Do not chain editions as the default for multi-range or multi-tab fill. Chaining successive edition ids is rare recovery only, not the fill recipe.

### 6. Verify and export

Verify with `sheet_read` on the edition for each patched range and for at least one untouched neighbor range when the OUT already held other periods. Then `file_download` the edition when the person needs the file.

Patch windows that hit formula cells fail. OCR is out of scope.
