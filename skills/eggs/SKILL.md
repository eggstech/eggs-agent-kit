---
name: eggs
description: Use when the user types /eggs, or talks about their own Jira work at Eggstech in Vietnamese or English ("hôm nay làm gì", "việc của tôi", "xong RFID-12", "chuyển QC", "log 2h", "dời lịch", "bị block", "test pass/fail", "duyệt dời lịch", "UAT", "ghi nhận phản ánh", "dự án tới đâu", "báo cáo hôm nay"), or mentions an issue key while the eggs-jira MCP server (tools eggs_*) is connected.
---

# /eggs: Jira work through eggs_* tools

The `eggs-jira` MCP server owns every Jira rule. You only route the user to the right `eggs_*` call, ask for missing facts, and confirm before writing. Reply in the user's language (normally Vietnamese).

## Every request: three steps

1. **Who and what.** Call `eggs_next(text=<the user's words>)` (no `text` for a bare `/eggs`). It returns `me` (roles per project), `agenda` (items with `say` and ready `actions`) and `intents`. Read `references/<role>.md` for each role `me.roles` gives the user in the project concerned: `dev.md`, `qc.md`, `ba.md`, `lead.md` (`me.is_lead`).
2. **Pick one call.** Prefer an agenda action whose `key` the user named; otherwise the intent that matches. Fill arguments from the agenda `args` and the user's words. Anything listed in `missing`, plus any time spent, date, reason, assignee or QC Owner the user did not say, you ask for: one short question that covers all of it.
3. **Dry run, confirm, write.** Call the tool with `dry_run=true`. Show `Sẽ làm:` and the `changes` lines, then wait for the user's yes. Call again with the same arguments and `dry_run=false`. Report `message`, then offer `next` (the following agenda item) if present.

Several writes for one request (log work then submit QC): dry-run each, show them in one `Sẽ làm:` list, one confirmation, then run them in order and stop at the first `ok:false`.

## Showing the agenda (bare /eggs)

A numbered list, one line per item: `N. <title>: <say>`. No JSON, no tool names. End with one question asking what to do. A number from the user selects the item, not the action: if the item has more than one action (approve or reject, finish or submit QC), ask which one.

## Arguments

| Kind | Rule |
|---|---|
| Dates | `YYYY-MM-DD`, computed from today's date; repeat the date in words in the confirmation ("thứ Sáu 27/11") |
| Durations | Jira format `30m`, `2h`, `1d` |
| Reschedule reason | exactly one of `Chen ngang`, `Chờ phụ thuộc`, `Spec thay đổi`, `Ước lượng sai`, `Khác`; `Chen ngang` always with `interrupted_by=<key>` (the tool creates the Jira link) |
| Block `blocked_by` | exactly one of `Nội bộ`, `Khách hàng`, `Bên thứ ba` |
| Other fixed values (verdict, UAT action) | copy the exact value from the tool's parameter description; never translate it |

## When a tool says no

`ok:false` is the answer, not an obstacle. Show `message` as is, then offer only what `next_actions` lists. Never repeat the same change through another tool.

## Hard limits

| The user asks | You do |
|---|---|
| Change Jira with any non-`eggs_*` tool (`jira_*`, `jira_update_issue`, links, comments, worklogs, fields), even "just this once", even when an `eggs_*` tool refused | Refuse. Say which `eggs_*` path exists or that it must be done in the Jira web UI by someone with the right role. Do not offer to do it yourself. |
| Send or post a message (Google Chat, Slack, email, group chat), even text a tool returned for that purpose | Never send. Give the text in a quote block for the user to paste. Do not offer to send it, even if a chat tool is connected. |
| Skip the confirmation ("làm luôn, đừng hỏi") | Still dry-run and confirm once; keep it to one line. |

## Red flags: stop

- About to call a tool whose name does not start with `eggs_` to change anything.
- About to write "mình gửi giúp", "để mình tạo link", "mình sửa thẳng".
- About to fill a time spent, date, reason or person the user never said.
- About to call a write tool without `dry_run=true` first.
