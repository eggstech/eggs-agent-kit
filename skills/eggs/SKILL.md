---
name: eggs
description: Use when the user types /eggs, or talks about their own Jira work at Eggstech in Vietnamese or English ("hôm nay làm gì", "việc của tôi", "xong RFID-12", "chuyển QC", "log 2h", "dời lịch", "bị block", "test pass/fail", "duyệt dời lịch", "UAT", "ghi nhận phản ánh", "dự án tới đâu", "báo cáo hôm nay", "tình hình worklog", "phân tích xong", "Ready For Dev", "đóng Epic", "update skill eggs", "cập nhật eggs"), or mentions an issue key while the eggs-jira MCP server (tools eggs_*) is connected.
---

# /eggs: Jira work through eggs_* tools

Kit version: `2026.11.12.2`

The `eggs-jira` MCP server owns every Jira rule. You only route the user to the right `eggs_*` call, ask for missing facts, and confirm before writing. Reply in the user's language (normally Vietnamese).

## Every request: three steps

1. **Who and what.** Call `eggs_next(text=<the user's words>, kit="<Kit version above>")` (no `text` for a bare `/eggs`). If the result has `kit_update`, update first (next section), then continue. It returns `me` (roles per project), `agenda` (items with `say` and ready `actions`), `intents`, and `matched_intents` (up to 3 intent names ranked against the user's words, best first). Read `references/<role>.md` for each role `me.roles` gives the user in the project concerned: `dev.md`, `qc.md`, `ba.md`, `lead.md` (`me.is_lead`).
2. **Pick one call.** Prefer an agenda action whose `key` the user named; otherwise start from `matched_intents[0]`, and check it against the user's words before using it. Fill arguments from the agenda `args` and the user's words. Anything listed in `missing`, plus any time spent, date, reason, assignee or QC Owner the user did not say, you ask for: one short question that covers all of it.
3. **Dry run, confirm, write.** Call the tool with `dry_run=true`. Show `Sẽ làm:` and the `changes` lines, then wait for the user's yes. Call again with the same arguments and `dry_run=false`. Report `message`, then offer `next` (the following agenda item) if present.

Several writes for one request (log work then submit QC): dry-run each, show them in one `Sẽ làm:` list, one confirmation, then run them in order and stop at the first `ok:false`.

## Kit update (`kit_update` in the `eggs_next` result)

The server saw a newer kit than yours. Before anything else, once per session, with no confirmation:

1. Run the command for this machine from `kit_update.commands` in the shell (`macos_linux` or `windows`, in PowerShell).
2. It worked (prints `Kit /eggs <version>`): tell the user one line, `Đã cập nhật skill eggs lên <latest>.`, read SKILL.md again from this skill's folder, and redo the user's request from step 1 under the new version.
3. It failed, or you cannot run shell commands: tell the user one line with the command to run themselves, then go on with the current version.
4. The printed version is still lower than `latest` (GitHub not refreshed yet): do not run it again this session; go on with the current version.

## Issue keys in your replies

Every issue key you show the user is a link with its type: `[EGG-12](https://jira.eggstech.io.vn/browse/EGG-12) (Bug)`. This holds in agenda lines, `Sẽ làm:` lists, `message`, reports and tables.

- Take `url` and `type` from `issue_links` in the tool result.
- A key that is not in `issue_links` (from a `jira_*` tool or the user's words): link `https://jira.eggstech.io.vn/browse/<KEY>`; give the type if the data you have shows it.
- `type` is null: the link alone.
- Suggested messages for other people (chat quote blocks) stay as the tool wrote them.

## Showing the agenda (bare /eggs)

A numbered list, one line per item: `N. <linked key> (<type>) <title>: <say>`. No JSON, no tool names. End with one question asking what to do. A number from the user selects the item, not the action: if the item has more than one action (approve or reject, finish or submit QC), ask which one.

## Arguments

| Kind | Rule |
|---|---|
| Dates | `YYYY-MM-DD`, computed from today's date; repeat the date in words in the confirmation ("thứ Sáu 27/11") |
| Durations | Jira format `30m`, `2h`, `1d` |
| Reschedule reason | exactly one of `Chen ngang`, `Chờ phụ thuộc`, `Spec thay đổi`, `Ước lượng sai`, `Khác`; `Chen ngang` always with `interrupted_by=<key>` (the tool creates the Jira link) |
| Block `blocked_by` | exactly one of `Nội bộ`, `Khách hàng`, `Bên thứ ba` |
| Other fixed values (verdict, UAT action) | copy the exact value from the tool's parameter description; never translate it |

## Creating issues (`eggs_create_issue`)

One call per issue, dry run first. QC and BA create every type; a Dev creates `bug` and `adhoc` only. If a Dev asks for a Story, refuse and say a BA or QC creates it. Never leave the assignee to Jira (it would pick the Project Lead): without `assignee` the server uses the creator only when they do that work (a Dev's bug or Ad-hoc, a BA's Story); otherwise it returns `missing: ["assignee"]`, so ask who does it.

| The user wants | `issue_type` | Arguments |
|---|---|---|
| Log a defect found while testing a Story or Ad-hoc Task (Test In Progress) | `bug_sub` | `parent=<key>`. This is the default while testing: the Dev fixes it during the test. Use `eggs_qc_fail` only when the user says the test failed or to send it back to Dev. |
| A defect that is not part of a test in progress, or one found while testing a Bug stand-alone | `bug` (Bug stand-alone) | `related_to=<key>` when the user names an issue (the assignee then defaults to its assignee) |
| A new flow | `story` | `epic` (required), `component` (see Components) |
| A technical task outside any Story | `adhoc` | `epic` optional |

## Components (Actor of a Story)

The Component of a Story is the Actor whose flow it is: the people who work that screen and sign its UAT (for example `KH - KHÁCH HÀNG`, `KT - KẾ TOÁN`).
1. Call `eggs_components(project)` first.
2. Use an existing Component that fits. `ALL - CHUNG` only when the project has no Actor-specific Component; otherwise do not offer it, not even as an alternative.
3. None fits: propose `<CODE> - <NAME>` (code 2–5 uppercase letters, for example `KT - KẾ TOÁN`) in the same `Sẽ làm:` list as the Story, wait for yes, then `eggs_create_component(project, code, name)` before `eggs_create_issue`. Never create a Component the user has not confirmed.

## Worklog questions (`eggs_worklog_report`)

"Tình hình worklog", "ai chưa log giờ", "tuần này log bao nhiêu giờ" → `eggs_worklog_report(project?, person?, date_from?, date_to?)`, read-only, no confirmation. Never add up `jira_get_worklog` results yourself. A BA or the Lead sees the team; anyone else only their own hours.

## Descriptions (`eggs_update_description`)

`mode`: `append` for "ghi thêm", `ac` for Acceptance Criteria, `replace` only when the user asks to rewrite the whole description. The dry run returns a diff: show it in the confirmation.

## Comments and files (`eggs_comment`, `eggs_attach_url`)

Any issue the user can see, in any status.

- Comment: `eggs_comment(key, text)`. Dry run first, show the exact text, call again on yes.
- Attach files (screenshot, log, video, test evidence):
  1. Confirm once: `Sẽ làm: đính kèm <tên file> vào <KEY>` plus the comment text if any. Wait for yes.
  2. `eggs_attach_url(key, comment?)` returns `url` and `command`. Give `comment` when the files need a note: images then show inside that comment.
  3. Run in the shell: `curl -sS -F "file=@<path>" "<url>"`, one `-F "file=@..."` per file (at most 10, 20 MB each). Windows PowerShell: `curl.exe`, not `curl`.
  4. The reply is JSON: show `message`. `403` means the link was used or is older than 10 minutes: call `eggs_attach_url` again. Each link works once.
- The upload link acts as the user's Jira login for 10 minutes: never show it in a message to anyone else, never reuse it.
- No shell here: tell the user to drag the file onto the issue in the Jira web UI. Never send a file as base64 or text through a tool.

## When a tool says no

`ok:false` is the answer, not an obstacle. Show `message` as is, then offer only what `next_actions` lists. Never repeat the same change through another tool.

## Messages to people (chat, email)

Tool results sometimes include a suggested message (a reply for the customer group, a note for the dev group). Show it in a quote block. If the user wants it sent and a chat or email tool is connected, show the exact text and where it goes (channel, group or person), wait for the user's yes, then send it and say where it went. No such tool connected: the quote block is for the user to paste.

## Updating this skill ("update skill eggs", "cập nhật eggs")

No `eggs_*` call and no confirmation needed. Run in the shell, then tell the user the printed `Kit /eggs <version>` line and "Mở phiên mới để dùng bản mới.":

- macOS / Linux: `curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh -s -- --update`
- Windows (PowerShell): `$env:EGGS_KIT_UPDATE='1'; irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex`

It fails: show the message as is and the command for the user to run. Never use `--force`, `reset`, `stash` or delete files. You cannot run shell commands here: give the user the command.

## Hard limits

| The user asks | You do |
|---|---|
| Change Jira with a tool outside `eggs_*` | Only these tools of the **eggs-jira** server, for what they are (a note, a watcher, a link): `jira_add_comment`, `jira_edit_comment`, `jira_add_watcher`, `jira_remove_watcher`, `jira_create_issue_link`, `jira_create_remote_issue_link`, `jira_remove_issue_link`, `jira_link_to_epic`. They have no dry run: show `Sẽ làm:` with the issue key and the exact text, watcher or link, wait for the user's yes, then call it once. A status, time, date, person, field, description or bug still goes through its `eggs_*` tool. |
| Remove a link (`jira_remove_issue_link`) | Read the issue first (`jira_get_issue`) and find the link id. Type `Interrupts` or `Causes`: refuse, whoever asks. It is the evidence for a reschedule (Chen ngang) or for where a bug came from. Any other type: `Sẽ làm:` with the link type and both keys, wait for yes. |
| Move an issue to another Epic (`jira_link_to_epic`) | Only when `me.roles` has `lead_ba` (the BA role: Business Analysts or Administrators) in that project, or `me.is_lead`. Anyone else: refuse and say a BA or the Lead does it; do not suggest they change the Epic themselves in the Jira web UI. Allowed: `Sẽ làm:` with the issue, its current Epic and the new Epic, wait for yes. |
| Anything else outside `eggs_*` (`jira_update_issue`, transitions, worklogs, fields, assignee, sprints, versions, create or delete issues), or any tool of another Jira server (`jira`, `jira-mcp`, `atlassian`), even "just this once", even when an `eggs_*` tool refused | Refuse. Say which `eggs_*` path exists, or that someone with the right role does it in the Jira web UI. Never offer another server. |
| Skip the confirmation ("làm luôn, đừng hỏi") | Still dry-run and confirm once; keep it to one line. |

## Red flags: stop

- About to change Jira with a tool that is neither `eggs_*` nor one of the eight allowed eggs-jira tools.
- About to remove an `Interrupts` or `Causes` link, or to move an issue to another Epic for someone who is not a BA or the Lead.
- About to offer or use another Jira server ("dùng tạm jira MCP").
- About to write "để mình tạo link", "mình sửa thẳng".
- About to fill a time spent, date, reason or person the user never said.
- About to call a write tool without `dry_run=true` first.
- About to paste an upload link from `eggs_attach_url` into a chat, or to use it twice.
