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

Move a Story with `eggs_story_step(key, step, comment?)`, dry run first like every write. Only a BA or the Lead may call it; the server checks everything below and lists every gap in one message: show it as is and ask for the missing facts.

| `step` | From → To | Needs |
|---|---|---|
| `analysis_done` | Open → Analyzed | exactly 1 Component, QC Owner, description with Acceptance Criteria |
| `reopen_analysis` | Analyzed → Open | `comment` = the reason (what is missing, who asked); ask for it if the user did not say |
| `ready_for_dev` | Analyzed → Ready For Dev | Dev Tasks with Part and estimate, a Due Date, QC Owner, 1 Component |
| `close_epic` | Epic Dev In Progress → Done | every issue in the Epic Done or Cancelled; the tool lists the open ones |

- Set a Story's Due Date while it is Open or Analyzed: `eggs_flow_reschedule(story_key, new_due, reason)`.
- Create a Story: SKILL.md "Creating issues" and "Components". Write or fix its description and AC: `eggs_update_description`.
- Move a Story's committed date after Ready For Dev: `eggs_flow_reschedule(story_key, new_due, reason)`.

## UAT by Actor
`eggs_uat(epic, actor, action, note, bugs?, stories?)`; `action` is `start`, `signoff` or `fail`. `actor` is the Component code (for example `KH`).
- `start`: every Story of that Actor in the Epic at Ready For UAT moves to UAT.
- `signoff`: refused while some Story of the Actor has not reached UAT, unless `stories` lists the ones being signed.
- `fail`: `stories` = the failing Stories, `bugs` = defects found.

## Cancel
`eggs_cancel(key, reason)`.
