# Siglata operation registry

Operation registry API version: 2
Operation registry revision: d1ca668c008f111832082f438d8a04de77131a2654e8ea7c49283c0b0fcdf0ea

## Writing a script

`search` and `execute` take a `script`. The tool descriptions carry the language card below.

```
## callscript

You act by sending ONE short script of tool calls, written as plain
JavaScript. It is parsed and validated - NEVER executed as JS: only
mounted tools can run, every issue is reported at once before anything
runs, and all fan-outs are bounded.

// close stale issues                                  <- first comment = intent
const issues = await repo.listIssues({ name: "api" });     // call a tool
const stale = issues.filter(i => i.stale);                 // derive a value (pure expression)
if (stale.length === 0) return { closed: 0 };              // guard: end the run early
const closed = await Promise.all(                          // fan out, bounded by the slice
  stale.slice(0, 10).map(i => repo.closeIssue({ name: "api", number: i.number })));
return { count: closed.length };                           // last statement = the run's output

More forms:
  const [a, b] = await Promise.all([x.one({}), y.two({})]); // independent calls run concurrently
  try { await repo.closeIssue({ ... }) }                    // without try/catch, a failed call
  catch (e) { await chat.post({ text: e.message }); }       //   fails the run; e = { message, code }
  const job = svc.export({ ... });   // no await: fire-and-forget; a LATER script joins it: await job
  await x.del({ id }, { reason: "why", suspend: true });    // per-call options: reason, suspend
                                                            //   (ask a human first), onError: "skip"

Rules:
- const only, single assignment; no while/for(;;), function, class, or import -
  fan out with .map over a bounded list
- awaited calls run in statement order; Promise.all runs them concurrently
- expressions are pure JS (arrows, ternaries, template literals, ?.) - no new,
  no regex; globals: Math, JSON, Object, Array, Number, String, Boolean, Base64
- `input` holds per-run data (auth codes, approvals) when a run is re-executed
- limits: 50 steps, 50 calls per fan-out, 50 calls total per script
- Date is not available: a plan must apply exactly as it was planned
```

## operations.describe

- Kind: read
- Role: member
- Summary: Return the JSON Schema of one operation registry entry on demand.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"op":{"type":"string","enum":["operations.describe","files.create","files.addRevision","files.list","files.search","files.download","files.move","files.setTags","files.trash","files.restore","files.purge","folders.create","folders.list","folders.trash","folders.restore","folders.purge","orgs.close","orgs.reopen","members.invite","members.list","members.setRole","members.setUsername","members.remove","members.cancelInvitation","members.resendInvitation","audit.list","spreadsheets.listSheets","spreadsheets.readRange","spreadsheets.inspectCell","spreadsheets.collate","spreadsheets.query","spreadsheets.extractTable","spreadsheets.unpivotMatrix","spreadsheets.inspectTemplate","spreadsheets.fillTemplate"]}},"required":["op"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"inputSchema":{},"kind":{"type":"string","enum":["read","write"]},"name":{"type":"string","enum":["operations.describe","files.create","files.addRevision","files.list","files.search","files.download","files.move","files.setTags","files.trash","files.restore","files.purge","folders.create","folders.list","folders.trash","folders.restore","folders.purge","orgs.close","orgs.reopen","members.invite","members.list","members.setRole","members.setUsername","members.remove","members.cancelInvitation","members.resendInvitation","audit.list","spreadsheets.listSheets","spreadsheets.readRange","spreadsheets.inspectCell","spreadsheets.collate","spreadsheets.query","spreadsheets.extractTable","spreadsheets.unpivotMatrix","spreadsheets.inspectTemplate","spreadsheets.fillTemplate"]},"outputSchema":{},"role":{"type":"string","enum":["admin","member","owner"]},"summary":{"type":"string"}},"required":["inputSchema","kind","name","outputSchema","role","summary"],"additionalProperties":false},"definitions":{}}
```

## files.create

- Kind: write
- Role: member
- Summary: Create a file from bytes already prepared in content storage under their sha256.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string","minLength":1},"source":{"type":"object","properties":{"mediaType":{"type":"string"},"name":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"},"size":{"type":"integer"}},"required":["mediaType","sha256","size"],"additionalProperties":false},"tags":{"type":"array","items":{"type":"string"}}},"required":["name","source"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"definitions":{}}
```

## files.addRevision

- Kind: write
- Role: member
- Summary: Add a revision to a live file from bytes already prepared in content storage.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"source":{"type":"object","properties":{"mediaType":{"type":"string"},"name":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"},"size":{"type":"integer"}},"required":["mediaType","sha256","size"],"additionalProperties":false}},"required":["file","source"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"wasDeduplicated":{"type":"boolean"}},"required":["file","wasDeduplicated"],"additionalProperties":false},"definitions":{}}
```

## files.list

- Kind: read
- Role: member
- Summary: Page the live or trashed files of the Organization, optionally by folder or tag.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"cursor":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer","minimum":1,"maximum":200},"state":{"type":"string","enum":["live","trashed"]},"tag":{"type":"string"}},"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"files":{"type":"array","items":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false}},"nextCursor":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]}},"required":["files","nextCursor"],"additionalProperties":false},"definitions":{}}
```

## files.search

- Kind: read
- Role: member
- Summary: Search live files by name, media type or tags.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"cursor":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer","minimum":1,"maximum":200},"mediaType":{"type":"string"},"name":{"type":"string"},"nameContains":{"type":"string"},"tags":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"files":{"type":"array","items":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false}},"nextCursor":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]}},"required":["files","nextCursor"],"additionalProperties":false},"definitions":{}}
```

## files.download

- Kind: read
- Role: member
- Summary: Read one revision of a live file as base64, inside the argument budget.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"revision":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"byteLength":{"type":"integer"},"contentBase64":{"type":"string"},"mediaType":{"type":"string"},"name":{"type":"string"},"revisionId":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","contentBase64","mediaType","name","revisionId","sha256"],"additionalProperties":false},"definitions":{}}
```

## files.move

- Kind: write
- Role: member
- Summary: Move a live file into a folder, or to the root when no folder is given.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"definitions":{}}
```

## files.setTags

- Kind: write
- Role: member
- Summary: Replace the whole tag set of a live file.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"tags":{"type":"array","items":{"type":"string"}}},"required":["file","tags"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"definitions":{}}
```

## files.trash

- Kind: write
- Role: member
- Summary: Move a live file to the trash.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"definitions":{}}
```

## files.restore

- Kind: write
- Role: member
- Summary: Restore a trashed file inside the retention window.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"definitions":{}}
```

## files.purge

- Kind: write
- Role: member
- Summary: Irreversibly purge a trashed file whose name the caller types back.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"confirmName":{"type":"string"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["confirmName","file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"name":{"type":"string"},"revisions":{"type":"array","items":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}}},"required":["name","revisions"],"additionalProperties":false},"definitions":{}}
```

## folders.create

- Kind: write
- Role: member
- Summary: Create a folder under an optional parent and return its path.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"name":{"type":"string","minLength":1},"parent":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["name"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"path":{"type":"array","items":{"type":"string"}}},"required":["id","path"],"additionalProperties":false},"definitions":{}}
```

## folders.list

- Kind: read
- Role: member
- Summary: Page the folders under an optional parent.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"cursor":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer","minimum":1,"maximum":200},"parent":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"folders":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"parentId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]}},"required":["id","name","parentId"],"additionalProperties":false}},"nextCursor":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]}},"required":["folders","nextCursor"],"additionalProperties":false},"definitions":{}}
```

## folders.trash

- Kind: write
- Role: member
- Summary: Move an empty live folder to the trash, refusing while it still holds anything live.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["folder"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"parentId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"state":{"type":"string","enum":["live","trashed","purged"]}},"required":["id","name","parentId","state"],"additionalProperties":false},"definitions":{}}
```

## folders.restore

- Kind: write
- Role: member
- Summary: Restore a trashed folder inside the retention window.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["folder"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"parentId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"state":{"type":"string","enum":["live","trashed","purged"]}},"required":["id","name","parentId","state"],"additionalProperties":false},"definitions":{}}
```

## folders.purge

- Kind: write
- Role: member
- Summary: Irreversibly purge an empty trashed folder whose name the caller types back.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"confirmName":{"type":"string"},"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"}},"required":["confirmName","folder"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"],"additionalProperties":false},"definitions":{}}
```

## orgs.close

- Kind: write
- Role: owner
- Summary: Close this Organization, freezing every write until an Owner reopens it inside the window.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"confirmName":{"type":"string"}},"required":["confirmName"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"closedAt":{"anyOf":[{"type":"string"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"state":{"type":"string","enum":["open","closed"]}},"required":["closedAt","id","name","state"],"additionalProperties":false},"definitions":{}}
```

## orgs.reopen

- Kind: write
- Role: owner
- Summary: Reopen a closed Organization inside the retention window.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"confirmName":{"type":"string"}},"required":["confirmName"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"closedAt":{"anyOf":[{"type":"string"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"state":{"type":"string","enum":["open","closed"]}},"required":["closedAt","id","name","state"],"additionalProperties":false},"definitions":{}}
```

## members.invite

- Kind: write
- Role: admin
- Summary: Invite an email address to the Organization with an inherited role. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"email":{"type":"string","minLength":1,"pattern":"^[^@]+@[^@]+[.][^@]+$","description":"an email address"},"role":{"type":"string","enum":["owner","admin","member"]}},"required":["email","role"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## members.list

- Kind: read
- Role: member
- Summary: List the members of the Organization with their inherited roles and usernames.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"anyOf":[{"type":"object"},{"type":"array"}]},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1},"username":{"type":"string"}},"required":["role","userId","username"],"additionalProperties":false}}},"required":["members"],"additionalProperties":false},"definitions":{}}
```

## members.setRole

- Kind: write
- Role: admin
- Summary: Set the inherited role of one member, keeping the last Owner. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1}},"required":["role","userId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## members.setUsername

- Kind: write
- Role: member
- Summary: Change your username in the current Organization. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"username":{"type":"string"}},"required":["username"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## members.remove

- Kind: write
- Role: admin
- Summary: Remove one member from the Organization, keeping the last Owner. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"userId":{"type":"string","minLength":1}},"required":["userId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## members.cancelInvitation

- Kind: write
- Role: admin
- Summary: Cancel a pending invitation. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## members.resendInvitation

- Kind: write
- Role: admin
- Summary: Send a pending invitation again. Prepare only: the change waits for a human to confirm it in the app.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"expiresAt":{"type":"string"},"pendingChangeId":{"type":"string","minLength":1},"status":{"anyOf":[{"type":"string","enum":["awaiting_confirmation"]}]}},"required":["expiresAt","pendingChangeId","status"],"additionalProperties":false},"definitions":{}}
```

## audit.list

- Kind: read
- Role: admin
- Summary: Page the audit events of the Organization in ascending order.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"after":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer","minimum":1,"maximum":200}},"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"events":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string"},"clientId":{"type":"string","minLength":1},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"inputRevisions":{},"operation":{"type":"string"},"planDigest":{"anyOf":[{"type":"string"},{"type":"null"}]},"resultHashes":{},"targets":{},"userId":{"type":"string","minLength":1}},"required":["at","clientId","id","inputRevisions","operation","planDigest","resultHashes","targets","userId"],"additionalProperties":false}},"nextCursor":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]}},"required":["events","nextCursor"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.listSheets

- Kind: read
- Role: member
- Summary: List all sheets in a spreadsheet workbook with dimensions and row/column counts.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"revision":{"type":"string"}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"name":{"type":"string"},"revisionId":{"type":"string"},"sheets":{"type":"array","items":{"type":"object","properties":{"columnCount":{"type":"integer"},"index":{"type":"integer"},"name":{"type":"string"},"rowCount":{"type":"integer"}},"required":["columnCount","index","name","rowCount"],"additionalProperties":false}}},"required":["file","mediaType","name","revisionId","sheets"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.readRange

- Kind: read
- Role: member
- Summary: Read structured cell values and rows from a spreadsheet workbook or CSV.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer"},"offset":{"type":"integer"},"range":{"type":"string"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"headers":{"type":"array","items":{"type":"string"}},"range":{"type":"string"},"rows":{"type":"array","items":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"sheet":{"type":"string"},"totalColumns":{"type":"integer"},"totalRows":{"type":"integer"}},"required":["file","headers","range","rows","sheet","totalColumns","totalRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.inspectCell

- Kind: read
- Role: member
- Summary: Inspect a single cell's cached value, type, and formula.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"cell":{"type":"string"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["cell","file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"cell":{"type":"string"},"formula":{"anyOf":[{"type":"string"},{"type":"null"}]},"sheet":{"type":"string"},"type":{"type":"string","enum":["text","number","boolean","blank","error"]},"value":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}},"required":["cell","formula","sheet","type","value"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.collate

- Kind: write
- Role: member
- Summary: Collate multiple spreadsheet sources into a uniform target report with arithmetic tie-out reconciliation.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"columns":{"type":"array","items":{"type":"string"}},"folder":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"includeSourceLabel":{"type":"boolean"},"locale":{"type":"string","enum":["en-US","pt-BR"]},"name":{"type":"string"},"sources":{"type":"array","items":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"label":{"type":"string"},"range":{"type":"string"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["file"],"additionalProperties":false}},"tags":{"type":"array","items":{"type":"string"}},"template":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"tieOutColumn":{"type":"string"}},"required":["columns","name","sources"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"reconciliation":{"type":"object","properties":{"collatedTotal":{"anyOf":[{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]},{"type":"null"}]},"formattedCollatedTotal":{"type":"string"},"formattedSourceTotal":{"type":"string"},"message":{"type":"string"},"sourceTotal":{"anyOf":[{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]},{"type":"null"}]},"status":{"type":"string","enum":["verified","variance","not_requested"]},"variance":{"anyOf":[{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]},{"type":"null"}]}},"required":["collatedTotal","message","sourceTotal","status","variance"],"additionalProperties":false},"sourceSummaries":{"type":"array","items":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"label":{"type":"string"},"rowsExtracted":{"type":"integer"},"subtotal":{"anyOf":[{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]},{"type":"null"}]}},"required":["file","label","rowsExtracted","subtotal"],"additionalProperties":false}},"totalRows":{"type":"integer"}},"required":["file","reconciliation","sourceSummaries","totalRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.query

- Kind: read
- Role: member
- Summary: Run a read-only SQL query over spreadsheet data.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"limit":{"type":"integer"},"query":{"type":"string"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]},"sources":{"type":"array","items":{"type":"object","properties":{"alias":{"type":"string"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["alias","file"],"additionalProperties":false}}},"required":["file","query"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"columns":{"type":"array","items":{"type":"string"}},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"rows":{"type":"array","items":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"sheet":{"type":"string"},"totalRows":{"type":"integer"}},"required":["columns","file","rows","sheet","totalRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.extractTable

- Kind: read
- Role: member
- Summary: Extract a normalized 1NF table from an Excel range with optional total row exclusion.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"excludeTotals":{"type":"boolean"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"headerRow":{"type":"integer"},"range":{"type":"string"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"columns":{"type":"array","items":{"type":"string"}},"excludedTotals":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"row":{"type":"integer"},"values":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"required":["label","row","values"],"additionalProperties":false}},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"rows":{"type":"array","items":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"sheet":{"type":"string"},"totalRows":{"type":"integer"}},"required":["columns","excludedTotals","file","rows","sheet","totalRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.unpivotMatrix

- Kind: read
- Role: member
- Summary: Unpivot a 2D cross-tab matrix into normalized 1NF relational tuples.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"colHeadersRange":{"type":"string"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"metricColumnName":{"type":"string"},"pivotColumnName":{"type":"string"},"revision":{"type":"string"},"rowHeadersRange":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]},"valuesRange":{"type":"string"}},"required":["colHeadersRange","file","rowHeadersRange","valuesRange"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"columns":{"type":"array","items":{"type":"string"}},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"rows":{"type":"array","items":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"sheet":{"type":"string"},"totalRows":{"type":"integer"}},"required":["columns","file","rows","sheet","totalRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.inspectTemplate

- Kind: read
- Role: member
- Summary: Inspect an Excel template workbook to extract structure, merged headers, placeholder styles, and summary formulas.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"revision":{"type":"string"},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]}},"required":["file"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"columnHeaders":{"type":"array","items":{"type":"string"}},"columnStyles":{"type":"array","items":{"type":"string"}},"dataStartRow":{"type":"integer"},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"headerRow":{"type":"integer"},"mergeCells":{"type":"array","items":{"type":"string"}},"sheet":{"type":"string"},"summaryRows":{"type":"array","items":{"type":"object","properties":{"formulas":{"type":"object","additionalProperties":{"type":"string"}},"label":{"type":"string"},"row":{"type":"integer"}},"required":["formulas","label","row"],"additionalProperties":false}}},"required":["columnHeaders","columnStyles","dataStartRow","file","headerRow","mergeCells","sheet","summaryRows"],"additionalProperties":false},"definitions":{}}
```

## spreadsheets.fillTemplate

- Kind: write
- Role: member
- Summary: Inject calculated relational rows into a pre-styled Excel template, preserving styling, formulas, and auto-calculating totals.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"anchorCell":{"type":"string"},"columnFormulas":{"type":"object","additionalProperties":{"type":"string"}},"columns":{"type":"array","items":{"type":"object","properties":{"column":{"type":"string"},"formula":{"type":"string"}},"additionalProperties":false}},"columnStyles":{"type":"array","items":{"type":"string"}},"file":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"oldRows":{"type":"integer"},"revision":{"type":"string"},"rows":{"type":"array","items":{"type":"array","items":{"anyOf":[{"type":"object","properties":{"kind":{"type":"string","enum":["text"]},"value":{"type":"string"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["number"]},"value":{"anyOf":[{"type":"number"},{"type":"string","enum":["Infinity","-Infinity","NaN"]}]}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["boolean"]},"value":{"type":"boolean"}},"required":["kind","value"],"additionalProperties":false},{"type":"object","properties":{"kind":{"type":"string","enum":["blank"]}},"required":["kind"],"additionalProperties":false}]}}},"sheet":{"anyOf":[{"type":"string"},{"type":"integer"}]},"tags":{"type":"array","items":{"type":"string"}}},"required":["anchorCell","file","name","rows"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"file":{"type":"object","properties":{"createdAt":{"type":"string"},"folderId":{"anyOf":[{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},{"type":"null"}]},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"name":{"type":"string"},"revision":{"anyOf":[{"type":"object","properties":{"byteLength":{"type":"integer"},"createdAt":{"type":"string"},"id":{"type":"string","pattern":"^([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}|00000000-0000-0000-0000-000000000000|[fF]{8}-[fF]{4}-[fF]{4}-[fF]{4}-[fF]{12})$","format":"uuid"},"mediaType":{"type":"string"},"sha256":{"type":"string","pattern":"^[0-9a-f]{64}$","description":"a lowercase hex sha256 digest"}},"required":["byteLength","createdAt","id","mediaType","sha256"],"additionalProperties":false},{"type":"null"}]},"revisions":{"type":"integer"},"state":{"type":"string","enum":["live","trashed","purged"]},"tags":{"type":"array","items":{"type":"string"}}},"required":["createdAt","folderId","id","name","revision","revisions","state","tags"],"additionalProperties":false},"injectedRows":{"type":"integer"},"name":{"type":"string"},"sheet":{"type":"string"}},"required":["file","injectedRows","name","sheet"],"additionalProperties":false},"definitions":{}}
```

