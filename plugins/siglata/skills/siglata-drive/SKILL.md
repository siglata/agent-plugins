---
name: siglata-drive
description: Manages Siglata Drive files and folders. Use for finding, uploading, downloading, organizing, tagging, deleting, or restoring files in Siglata.
---

# Siglata Drive

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Find requested files or folders through `search`. Resolve ambiguous names before making changes.
- Follow pagination until the requested set is covered.
- Upload through the connection's supported file-transfer capability. If unavailable, explain what the client needs. An upload is complete when the server returns the saved file or revision.
- Deliver downloaded bytes as a usable file or client attachment.
- Preserve existing tags when adding a tag: `files.setTags` replaces the entire set.
- Move files into the requested folder. Omit the destination folder only when moving to the root.
- Use trash for deletion. Permanently purge only when explicitly requested.
- A folder must be empty before trashing. Trash its contents first when they are in scope; ask before removing anything else.
