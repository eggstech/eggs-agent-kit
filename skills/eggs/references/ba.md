# BA (role Business Analysts; Lead-BA decisions)

## Reschedule requests
- See them: agenda items "Chờ duyệt dời lịch", or `eggs_pending_approvals(project?)`.
- Decide: `eggs_decide_reschedule(key, approved, reason?, new_end?)`. Rejecting needs `reason`. Approving a different date than proposed: pass `new_end`.
- Nobody approves their own request; the server refuses it.

## Stories (flows)
Status meaning:
- **Open**: the BA is analysing.
- **Analyzed**: the BA's material is complete. Devs add Dev Tasks (Part + estimate).
- **Ready For Dev**: the Due Date is set and Devs can start.

Moving between them is done by the BA in the Jira web UI; there is no `eggs_*` tool for it. Tell the user the transition name and what it needs:

| Transition | From → To | Needs |
|---|---|---|
| `Analysis Done` | Open → Analyzed | exactly 1 Component, QC Owner, description with Acceptance Criteria |
| `Reopen Analysis` | Analyzed → Open | a comment with the reason (what is missing, who asked) |
| `Set Due Date` | Open or Analyzed | the Due Date |
| `Ready For Dev` | Analyzed → Ready For Dev | Dev Tasks with Part and estimate, and a Due Date |

- Create a Story: SKILL.md "Creating issues" and "Components". Write or fix its description and AC: `eggs_update_description`.
- Move a Story's committed date after Ready For Dev: `eggs_flow_reschedule(story_key, new_due, reason)`.

## UAT by Actor
`eggs_uat(epic, actor, action, note, bugs?, stories?)`; `action` is `start`, `signoff` or `fail`. `actor` is the Component code (for example `KH`).
- `start`: every Story of that Actor in the Epic at Ready For UAT moves to UAT.
- `signoff`: refused while some Story of the Actor has not reached UAT, unless `stories` lists the ones being signed.
- `fail`: `stories` = the failing Stories, `bugs` = defects found.

## Cancel
`eggs_cancel(key, reason)`.
