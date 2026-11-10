# eggs-agent-kit

Skill `/eggs` cho agent trong IDE (Claude Code, Cursor, OpenCode, Antigravity, Hermes) làm việc với Jira Eggstech qua MCP `eggs-jira-mcp` (toolset `eggs`). Thiết kế: `docs/2026-11-09-jira-agent-workflow-design.md` §9.3–9.4.

```
skills/eggs/
├─ SKILL.md          quy trình 3 bước, tham số, giới hạn cứng
└─ references/       dev.md, qc.md, ba.md, lead.md (agent chỉ đọc file của vai trò người dùng)
tests/               kịch bản thử và kết quả (xem tests/RESULTS.md)
```

Chưa có: `references/plan.md` (tạo card từ tài liệu, chờ tool `eggs_plan_*`), script cài `install.sh` / `install.ps1` (chờ MCP chạy dạng HTTP, Task 11).

Thử tay trên máy: symlink `skills/eggs` vào `~/.claude/skills/eggs`, kết nối MCP `eggs-jira-mcp` với PAT của chính mình, gõ `/eggs`.
