---
name: siglata-admin
description: Manages Siglata organizations. Use for members, invitations, permissions, and organization roles.
---

# Siglata Admin

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Resolve the member or invitation from server results. Clarify ambiguous people or unspecified roles before changing access.
- Permissions are organization roles: `owner`, `admin`, and `member`. Preserve at least one owner.
- Run the `members_*`, `invitation_*`, and `organization_*` operations through `execute`. Report the result the server returns for each call.
- Cancel or resend using the invitation ID from its record or link. If the invitation cannot be found, request its ID or direct the person to the app.
