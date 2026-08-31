# Siglata catalogue

Catalogue API version: 1
Catalogue revision: 0b483402220bec33fd7ca890b84402de11263ccda292f071c6dc9205bd5f71fc

## catalogue.describe

- Kind: read
- Role: member
- Summary: Return the JSON Schema of one catalogue operation on demand.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"op":{"type":"string","enum":["catalogue.describe","files.create","files.addRevision","files.list","files.search","files.download","files.move","files.setTags","files.trash","files.restore","files.purge","folders.create","folders.list","members.invite","members.list","members.setRole","members.remove","members.cancelInvitation","members.resendInvitation","audit.list"]}},"required":["op"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"inputSchema":{},"kind":{"type":"string","enum":["read","write"]},"name":{"type":"string","enum":["catalogue.describe","files.create","files.addRevision","files.list","files.search","files.download","files.move","files.setTags","files.trash","files.restore","files.purge","folders.create","folders.list","members.invite","members.list","members.setRole","members.remove","members.cancelInvitation","members.resendInvitation","audit.list"]},"outputSchema":{},"role":{"type":"string","enum":["admin","member"]},"summary":{"type":"string"}},"required":["inputSchema","kind","name","outputSchema","role","summary"],"additionalProperties":false},"definitions":{}}
```

## files.create

- Kind: write
- Role: member
- Summary: Create a file from bytes already staged in the vault under their sha256.

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
- Summary: Add a revision to a live file from bytes already staged in the vault.

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

## members.invite

- Kind: write
- Role: admin
- Summary: Invite an email address to the Organization with an inherited role.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"email":{"type":"string","minLength":1,"pattern":"^[^@]+@[^@]+[.][^@]+$","description":"an email address"},"role":{"type":"string","enum":["owner","admin","member"]}},"required":["email","role"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

## members.list

- Kind: read
- Role: member
- Summary: List the members of the Organization with their inherited roles.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"anyOf":[{"type":"object"},{"type":"array"}]},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1}},"required":["role","userId"],"additionalProperties":false}}},"required":["members"],"additionalProperties":false},"definitions":{}}
```

## members.setRole

- Kind: write
- Role: admin
- Summary: Set the inherited role of one member, keeping the last Owner.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1}},"required":["role","userId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1}},"required":["role","userId"],"additionalProperties":false}}},"required":["members"],"additionalProperties":false},"definitions":{}}
```

## members.remove

- Kind: write
- Role: admin
- Summary: Remove one member from the Organization, keeping the last Owner.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"userId":{"type":"string","minLength":1}},"required":["userId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"role":{"type":"string","enum":["owner","admin","member"]},"userId":{"type":"string","minLength":1}},"required":["role","userId"],"additionalProperties":false}}},"required":["members"],"additionalProperties":false},"definitions":{}}
```

## members.cancelInvitation

- Kind: write
- Role: admin
- Summary: Cancel a pending invitation.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

## members.resendInvitation

- Kind: write
- Role: admin
- Summary: Send a pending invitation again.

### Input schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
```

### Output schema

```json
{"dialect":"draft-2020-12","schema":{"type":"object","properties":{"invitationId":{"type":"string","minLength":1}},"required":["invitationId"],"additionalProperties":false},"definitions":{}}
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

