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

The server exposes two tools. `search` lists the operation signatures the current grant may call. `execute` runs a script that calls those operations.

1. Run `principal_get` through `execute` to confirm the organization, the role, and the granted scopes. Resolve any mismatch with the person before proceeding.
2. Call `search` to find the operations this grant can call and the arguments each one takes.
3. Write one script that calls those operations and run it through `execute`. A script runs in a single pass and cannot wait for another call, so read everything a later step needs in the same script.
4. Report confirmed results or returned items. Identify anything still pending or blocked.

### Connection and operation failures

- If the server requests authentication, direct the person to reconnect through the client's OAuth flow. Let the person initiate sign-in. Keep credentials in the client, not in chat or files.
- For denied access, use the server's reason to identify the required organization, role, or approval. Report the access blocker rather than repeatedly reconnecting or trying another identity.
- If an operation is unavailable or the connection fails, report the limitation and stop dependent calls. Continue independent local work. Use available schemas rather than guessed tools or alternate access paths.
- If an `execute` response is lost, report the outcome as unknown until a later read confirms it.
