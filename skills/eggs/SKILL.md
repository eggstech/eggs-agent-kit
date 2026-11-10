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

## Messages to people (chat, email)

Tool results sometimes include a suggested message (a reply for the customer group, a note for the dev group). Show it in a quote block. If the user wants it sent and a chat or email tool is connected, show the exact text and where it goes (channel, group or person), wait for the user's yes, then send it and say where it went. No such tool connected: the quote block is for the user to paste.

## Hard limits

| The user asks | You do |
|---|---|
| Change Jira with a tool outside `eggs_*` | Only these tools of the **eggs-jira** server, for what they are (a note, a watcher, a link): `jira_add_comment`, `jira_edit_comment`, `jira_add_watcher`, `jira_remove_watcher`, `jira_create_issue_link`, `jira_create_remote_issue_link`. They have no dry run: show `Sẽ làm:` with the issue key and the exact text, watcher or link, wait for the user's yes, then call it once. A status, time, date, person, field, description or bug still goes through its `eggs_*` tool. |
| Anything else outside `eggs_*` (`jira_update_issue`, transitions, worklogs, fields, assignee, removing links), or any tool of another Jira server (`jira`, `jira-mcp`, `atlassian`), even "just this once", even when an `eggs_*` tool refused | Refuse. Say which `eggs_*` path exists, or that someone with the right role does it in the Jira web UI. Never offer another server. |
| Skip the confirmation ("làm luôn, đừng hỏi") | Still dry-run and confirm once; keep it to one line. |

## Red flags: stop

- About to change Jira with a tool that is neither `eggs_*` nor one of the six allowed eggs-jira tools.
- About to offer or use another Jira server ("dùng tạm jira MCP").
- About to write "để mình tạo link", "mình sửa thẳng".
- About to fill a time spent, date, reason or person the user never said.
- About to call a write tool without `dry_run=true` first.
