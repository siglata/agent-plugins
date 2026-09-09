---
name: siglata-admin
description: Manages Siglata organizations. Use for members, invitations, permissions, organization roles, usernames, or closing and reopening an organization.
---

# Siglata Admin

Follow the [shared workflow](../siglata/SKILL.md#workflow), reusing it if already loaded.

- Resolve the member or invitation from server results. Clarify ambiguous people or unspecified roles before changing access.
- Permissions are organization roles: `owner`, `admin`, and `member`. Preserve at least one owner.
- Invitations, role changes, removals, and username changes can require app confirmation after applying. For `awaiting_confirmation`, give the pending change details and direct the person to confirm in the Siglata app. Report completion when the server confirms the effect.
- Cancel or resend using the invitation ID from its record or link. A pending change ID identifies an approval request. If the invitation cannot be found, request its ID or direct the person to the app.
- Close or reopen an organization only on an explicit request. Closing freezes writes.
