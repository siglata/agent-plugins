---
name: siglata
description: Routes Siglata requests for files, folders, members, invitations, and organization administration. Also use to create or improve reusable agent skills for any domain.
---

# Siglata

Read the matching guides:

- For files and folders, read [Siglata Drive](../siglata-drive/SKILL.md).
- For members, invitations, permissions, and organization administration, read [Siglata Admin](../siglata-admin/SKILL.md).
- For creating or improving agent skills, read [Siglata Skills](../siglata-skills/SKILL.md).

Read all relevant guides for mixed requests. Reuse guides already loaded. Skill authoring works offline; use the workflow below only for Siglata service operations.

## Workflow

If Siglata tools are missing, pause service operations and direct the person to install or enable the full Siglata plugin and its MCP connection in a supported client. Installing skills alone does not connect the service.

1. Check the organization and role with the connected Siglata server's `context` tool. Resolve any mismatch with the person before proceeding.
2. Discover available operations in `context`, and call `operations.describe` for argument schemas. Read and locate targets through `search`.
3. Make changes through `execute`, following its plan and apply instructions. Reuse the idempotency key when retrying an interrupted apply. Plan again if stale.
4. Report confirmed results or returned items. Identify anything still pending or blocked.

### Connection and operation failures

- If the server requests authentication, direct the person to reconnect through the client's OAuth flow. Let the person initiate sign-in. Keep credentials in the client, not in chat or files.
- For denied access, use the server's reason to identify the required organization, role, or approval. Report the access blocker rather than repeatedly reconnecting or trying another identity.
- If an operation is unavailable or the connection fails, report the limitation and stop dependent calls. Continue independent local work. Use available schemas rather than guessed tools or alternate access paths.
- If an apply response is lost, report the outcome as unknown until the server confirms it.
