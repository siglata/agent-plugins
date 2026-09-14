---
name: siglata-admin
description: Manages Siglata organizations. Use for members, invitations, organization roles, and file or folder access grants.
---

# Siglata Admin

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Resolve the member or invitation from server results. Clarify ambiguous people or unspecified roles before changing access.
- Organization roles are `owner`, `admin`, and `member`. Preserve at least one owner.
- Object ACL grants are a second permission layer: `grants_list`, `grant_create`, `grant_revoke`. Discover args via `search`; run via `execute`. Listing needs `files:read`; create and revoke need `files:write`. Only the object's creator or an org admin (`owner`/`admin`) may list, create, or revoke.
- Run the `members_*`, `invitation_*`, `organization_*`, `grants_list`, and `grant_*` operations through `execute`. Report the result the server returns for each call.
- Cancel or resend using the invitation ID from its record or link. If the invitation cannot be found, request its ID or direct the person to the app.
