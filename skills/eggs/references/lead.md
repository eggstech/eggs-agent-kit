# Lead

Read-only views; present the returned table as is (Actor rows), then a two-line summary of what needs attention.
- "Epic/dự án tới đâu": `eggs_workstream_status(epic=<key>)` or `(project=<key>)`; no argument = whole company.
- "Báo cáo hôm nay": `eggs_daily_report(project?)`.
- "Ai đang chờ duyệt": `eggs_pending_approvals(project?)`.

The Lead may also take every BA action (see `ba.md`).
