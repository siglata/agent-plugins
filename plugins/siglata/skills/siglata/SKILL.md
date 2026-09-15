---
name: siglata
description: Routes Siglata requests for files, folders, Excel sheet and relation reads, members, invitations, and organization administration. Also use to create or improve reusable agent skills for any domain.
---

# Siglata

Read the matching guides:

- For files, folders, and Excel (`.xlsx`) sheet or relation extract, read [Siglata Drive](../siglata-drive/SKILL.md).
- For members, invitations, permissions, and organization administration, read [Siglata Admin](../siglata-admin/SKILL.md).
- For creating or improving agent skills, read [Skill creator](../skill-creator/SKILL.md).

Read all relevant guides for mixed requests. Reuse guides already loaded. Skill authoring works offline; use the workflow below only for Siglata service operations.

The MCP server brand is **siglata**. CallScript is the script engine behind `search` and `execute` only. Do not call the product "CallScript MCP."

## Workflow

If Siglata tools are missing, pause service operations and direct the person to install or enable the full Siglata plugin and its MCP connection in a supported client. Installing skills alone does not connect the service.

The server exposes two tools. `search` lists the operation signatures the current grant may call. `execute` runs a script that calls those operations.

1. Run `principal_get` through `execute` to learn which organization this grant is bound to (`organizationId`), plus the role and granted scopes. Call `organization_get` in the same script when you need the organization name or slug. Each grant is one organization; a different workspace needs a separate OAuth connection. Resolve any mismatch with the person before proceeding.
2. Call `search` to find the operations this grant can call and the arguments each one takes.
3. Write one script that calls those operations and run it through `execute`. A script runs in a single pass and cannot wait for another call, so read everything a later step needs in the same script.
4. Report confirmed results or returned items. Identify anything still pending or blocked.

### Access tiers

Self-serve signup lands the org in the **testing** tier (limited scopes and teammates). An operator can later set **upgraded** for fuller access. **revoked** denies MCP for that org. Do not tell the person to wait for an operator before first connect. Prefer read scopes for a first testing session.

### Connection and operation failures

- If the server requests authentication, direct the person to reconnect through the client's OAuth flow. Let the person initiate sign-in. Keep credentials in the client, not in chat or files.
- For denied access, use the server's reason to identify the required organization, role, tier, or approval. Report the access blocker rather than repeatedly reconnecting or trying another identity.
- If the person needs a different organization, they must authorize a new OAuth grant for that org. Do not invent an org-switch or grant-rebind operation.
- If scopes are too narrow, they must revoke the session and reconsent. Do not invent a post-grant `scopes_update` operation.
- To leave the grant org without deleting it, use `organization_leave` (or the app Leave organization control). Entitlement on the org is separate from membership.
- If an operation is unavailable or the connection fails, report the limitation and stop dependent calls. Continue independent local work. Use available schemas rather than guessed tools or alternate access paths.
- If an `execute` response is lost, report the outcome as unknown until a later read confirms it.
