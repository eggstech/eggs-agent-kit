# Dev (role Developers)

## Taking and starting work
- Unscheduled item: `eggs_schedule(key, start, end, estimate)` then `eggs_start(key)`. `eggs_start` also accepts `start`, `end`, `estimate` to do both in one call. Ask for any of the three the user did not give.
- Dates can only be set once (the first schedule becomes the baseline). Later changes go through a reschedule request.

## Logging time
`eggs_log_work(key, time_spent, note, started?)`. "hôm qua làm 4h RFID-128" → `started` = yesterday's date. Never guess the hours or the note.

## Finishing: which call
Jira refuses Finish and Submit QC unless the user has logged work on that issue. If the user has not said they logged time on it, ask "Bạn làm bao lâu, nội dung gì?" and plan `eggs_log_work` before the finishing call (one confirmation for both).

| Issue | Call |
|---|---|
| Dev Task under a Story | Dev chooses: `eggs_submit_qc` (QC tests this part) or `eggs_finish` (no separate QC; QC tests the whole Story later). "chuyển QC" → submit_qc; "xong luôn" / "không cần QC" → finish; otherwise ask once. |
| Dev Task under an Ad-hoc Task or Bug stand-alone | `eggs_finish` (QC happens on the parent) |
| Bug (sub), Bug stand-alone | `eggs_submit_qc` (always QC) |
| Ad-hoc Task | `eggs_finish` (no QC) or `eggs_submit_qc(key, qc_owner=<username>)`; ask who tests if the user wants QC and did not name anyone |

An item with open sub-tasks cannot be finished or submitted; the tool says which ones are open.

## Delays and interruptions
- Ask to move the end date: `eggs_request_reschedule(key, proposed_end, reason, interrupted_by?)`. A BA approves it; the date does not change until then.
- Flag `NEED_RESCHEDULE` but the interruption does not affect the date: `eggs_request_reschedule(key, no_impact=true)`.
- Blocked: `eggs_block(key, reason, blocked_by)`; resolved: `eggs_unblock(key, note?)`.

## End of day
`eggs_end_day(entries=[{key, time_spent, note, move_to}])`, `move_to` = `ready_for_qc`, `done` or omitted. Build one entry per issue the user mentions; apply the "Finishing" table to choose `move_to`.
