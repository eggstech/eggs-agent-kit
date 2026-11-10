# BA (role Business Analysts; Lead-BA decisions)

## Reschedule requests
- See them: agenda items "Chờ duyệt dời lịch", or `eggs_pending_approvals(project?)`.
- Decide: `eggs_decide_reschedule(key, approved, reason?, new_end?)`. Rejecting needs `reason`. Approving a different date than proposed: pass `new_end`.
- Nobody approves their own request; the server refuses it.

## Stories (flows)
- Move a Story's committed date: `eggs_flow_reschedule(story_key, new_due, reason)`.
- Story analysis steps (Start Analysis, Set Due Date, Ready For Dev) are done in the Jira web UI.

## UAT by Actor
`eggs_uat(epic, actor, action, note, bugs?, stories?)`; `action` is `start`, `signoff` or `fail`. `actor` is the Component code (for example `KH`).
- `start`: every Story of that Actor in the Epic at Ready For UAT moves to UAT.
- `signoff`: refused while some Story of the Actor has not reached UAT, unless `stories` lists the ones being signed.
- `fail`: `stories` = the failing Stories, `bugs` = defects found.

## Cancel
`eggs_cancel(key, reason)`.
