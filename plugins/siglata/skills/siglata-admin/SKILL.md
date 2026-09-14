---
name: siglata-admin
description: Manages Siglata organizations. Use for members, invitations, organization roles, leave, and file or folder access grants.
---

# Siglata Admin

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Resolve the member or invitation from server results. Clarify ambiguous people or unspecified roles before changing access.
- Organization roles are `owner`, `admin`, and `member`. Preserve at least one owner.
- Object ACL grants are a second permission layer: `grants_list`, `grant_create`, `grant_revoke`. These are file or folder shares, not the OAuth MCP grant. Discover args via `search`; run via `execute`. Listing needs `files:read`; create and revoke need `files:write`. Only the object's creator or an org admin (`owner`/`admin`) may list, create, or revoke.
- Run the `members_*`, `invitation_*`, `organization_*`, `grants_list`, and `grant_*` operations through `execute`. Report the result the server returns for each call.
- Cancel or resend using the invitation ID from its record or link. If the invitation cannot be found, request its ID or direct the person to the app.
- To leave the current grant organization without deleting it, run `organization_leave`. Prefer the app Leave organization control when the person is a multi-org consultant. Leaving drops membership only; org entitlement (`testing` / `upgraded` / `revoked`) stays until an operator changes it.
- Org access tiers: `testing` is the self-serve default after signup; `upgraded` is operator graduation for more teammates or fuller access; `revoked` denies MCP. Do not invent org-switch or post-grant `scopes_update`. A different workspace needs a new OAuth connection.
