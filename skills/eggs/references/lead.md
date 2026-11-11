# Lead

Read-only views; present the returned table as is (Actor rows), then a two-line summary of what needs attention.
- "Epic/dự án tới đâu": `eggs_workstream_status(epic=<key>)` or `(project=<key>)`; no argument = whole company.
- "Báo cáo hôm nay": `eggs_daily_report(project?)`.
- "Ai đang chờ duyệt": `eggs_pending_approvals(project?)`.
- "Tình hình worklog", "ai chưa log giờ", "giờ làm của henry": `eggs_worklog_report(project?, person?, date_from?, date_to?)`. Default range is this week (Monday to today), at most 31 days. Show `message` as is; offer the per-day details only when asked.

The Lead may also take every BA action (see `ba.md`).
