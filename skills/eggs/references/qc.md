# QC (role Testers)

## Testing
- Queue: agenda items "Chờ kiểm thử". Start: `eggs_qc_start(key)`.
- Pass: `eggs_qc_pass(key, note, time_spent?)`. A **Story** needs the QC's own worklog: ask for `time_spent` if not given. For a part (Dev Task, Bug, Ad-hoc) time is optional.
- Defect found while testing a Story or Ad-hoc Task: log it at once as a Bug sub-task, `eggs_create_issue(project, issue_type="bug_sub", parent=<key>, summary)`, one per defect. The item stays in Test In Progress and the Dev fixes it meanwhile. QC Pass is refused until every sub-task is Done or Cancelled.
- Defect found while testing a Bug stand-alone, or after the test: a new Bug stand-alone with `related_to=<key>` (no Bug sub-task under a Bug stand-alone). Do not ask the user to pass or fail the tested item first.
- Fail (only when the user says the test failed or to send it back): `eggs_qc_fail(key, note, reason?, bugs?, time_spent?)`.
  - Story: at least one open Bug sub-task must exist; pass `bugs` = list of bug titles from the user (one per defect) unless the Bug already exists.
  - Dev Task, Bug, Ad-hoc Task: a comment describing the defect (`note`) is enough.
- An Ad-hoc Task or Bug stand-alone with open sub-tasks cannot pass; the tool lists them.

## User reports (phản ánh)
- Record: `eggs_triage_open(project, text, source_url, reported_by, reported_at?)`. Ask for the message link and who reported it if missing.
- Conclude: `eggs_triage_close(key, verdict, note, time_spent, bug_target?, link_key?)`. `verdict` is one of the values in the tool's parameter description; the verdict decides whether `bug_target` (Story key) or `link_key` (existing issue) is needed. Ask for `time_spent`.
- The result contains a suggested reply for the customer group chat. Show it in a quote block; send it only as SKILL.md "Messages to people" says.
