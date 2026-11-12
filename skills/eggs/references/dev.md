# Dev (role Developers)

## Taking and starting work
- Unscheduled item: `eggs_schedule(key, start, end, estimate)` then `eggs_start(key)`. `eggs_start` also accepts `start`, `end`, `estimate` to do both in one call. Ask for any of the three the user did not give.
- Dates can only be set once (the first schedule becomes the baseline). Later changes go through a reschedule request.

## Logging time
`eggs_log_work(key, time_spent, note, started?)`. "hôm qua làm 4h RFID-128" → `started` = yesterday's date (`YYYY-MM-DD`, logged at 09:00; a future date is refused). Never guess the hours or the note.
- "Tuần này tôi log bao nhiêu giờ": `eggs_worklog_report()` (a Dev sees only their own hours; asking for someone else is refused, so do not offer it).

## Finishing: which call
Jira refuses Finish and Submit QC unless the user has logged work on that issue. If the user has not said they logged time on it, ask "Bạn làm bao lâu, nội dung gì?" and plan `eggs_log_work` before the finishing call (one confirmation for both).

| Issue | Call |
|---|---|
| Dev Task under a Story | Dev chooses: `eggs_submit_qc` (QC tests this part) or `eggs_finish` (no separate QC; QC tests the whole Story later). "chuyển QC" → submit_qc; "xong luôn" / "không cần QC" → finish; otherwise ask once. |
| Dev Task under an Ad-hoc Task or Bug stand-alone | `eggs_finish` (QC happens on the parent) |
| Bug (sub) | `eggs_submit_qc` (always QC; QC Owner comes from the parent) |
| Bug stand-alone | `eggs_submit_qc(key, qc_owner=<username>)` (always QC); if its QC Owner is empty, ask who tests. A Bug stand-alone created from a user report already has the triage QC as owner |
| Ad-hoc Task | `eggs_finish` (no QC) or `eggs_submit_qc(key, qc_owner=<username>)`; ask who tests if the user wants QC and did not name anyone |

An item with open sub-tasks cannot be finished or submitted; the tool says which ones are open.

## Splitting work: your own Dev Task
Each Dev creates the Dev Task for their own part; the BA does not split work for Devs. `eggs_create_issue(project, issue_type="dev_task", parent, summary, part, estimate)`, dry run first. Ask for `part` and `estimate` if the user did not give them; the server lists the valid Parts. `eggs_plan_apply` is not needed and the Story needs no Epic.

What the server does with the parent's status (show its message as is when it refuses):

| Parent | Status | Result |
|---|---|---|
| Story | Open, Analyzed | Created; it can Start only once the BA moves the Story to Ready For Dev |
| Story | Ready For Dev, Dev In Progress | Created |
| Story | QC TO DO, Test In Progress, Ready For UAT | Refused with `missing: ["confirm_reopen"]`: the Story would go back to Dev In Progress. If the user is reporting a defect, use a Bug sub-task instead. Otherwise ask the user, then call again with `confirm_reopen=true` |
| Story | Wait For Review, Done, Cancelled | Refused: a change after UAT or after Done is a new Story (BA) linked "relates to" the old one |
| Ad-hoc Task, Bug stand-alone | DEV To Do, Dev In Progress | Created |
| Ad-hoc Task, Bug stand-alone | QC TO DO, Test In Progress, Done, Cancelled | Refused: QC Fail first to bring it back, or a new issue |

After creating it, schedule and start it as usual (`eggs_start(key, start, end, estimate)`). The server warns when you already have an open Dev Task with the same Part under that parent; ask before keeping both.

## Creating and describing
- A Dev creates a Bug stand-alone, an Ad-hoc Task or their own Dev Task (SKILL.md "Creating issues"), never a Story: a BA or QC creates Stories.
- Notes on your own task go into its description: `eggs_update_description(key, text, mode="append")`.

## Delays and interruptions
- Ask to move the end date: `eggs_request_reschedule(key, proposed_end, reason, interrupted_by?)`. A BA approves it; the date does not change until then.
- Flag `NEED_RESCHEDULE` but the interruption does not affect the date: `eggs_request_reschedule(key, no_impact=true)`.
- Blocked: `eggs_block(key, reason, blocked_by)` (it also leaves the comment `Block (<blocked_by>): <reason>`); resolved: `eggs_unblock(key, note?)`.
- Logging work never changes Remaining Estimate; Eggs plans with Original Estimate only.

## End of day
`eggs_end_day(entries=[{key, time_spent, note, move_to}])`, `move_to` = `ready_for_qc`, `done` or omitted. Build one entry per issue the user mentions; apply the "Finishing" table to choose `move_to`. If the dry run says it is before 17:00, show that line and ask whether they are really ending the day.
