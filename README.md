# eggs-agent-kit

Skill `/eggs` cho agent trong IDE (Claude Code, Cursor, OpenCode, Antigravity, Hermes) làm việc với Jira Eggstech qua MCP `eggs-jira-mcp` (toolset `eggs`). Thiết kế: `docs/2026-11-09-jira-agent-workflow-design.md` §9.3–9.4.

```
skills/eggs/
├─ SKILL.md          quy trình 3 bước, tham số, giới hạn cứng
└─ references/       dev.md, qc.md, ba.md, lead.md (agent chỉ đọc file của vai trò người dùng)
tests/               kịch bản thử skill (RESULTS.md) và test bộ cài (test_install.py)
scripts/install.py   bộ cài (install.sh / install.ps1 gọi file này)
```

## Cài đặt (mỗi người, một lần)

Cần: Python 3 (macOS có sẵn; Windows `winget install Python.Python.3.12`), Jira PAT của chính mình (Jira → Profile → Personal Access Tokens), URL MCP do Lead gửi.

```bash
git clone <repo kit> ~/eggs-agent-kit && cd ~/eggs-agent-kit
./install.sh --url https://<máy chủ MCP>/mcp
```

Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File .\install.ps1 --url https://<máy chủ MCP>/mcp`

Script hỏi PAT (gõ ẩn), rồi với mỗi công cụ có trên máy:

| Công cụ | Skill liên kết vào | Cấu hình MCP `eggs-jira` |
|---|---|---|
| Claude Code | `~/.claude/skills/eggs` | `claude mcp add --transport http --scope user` |
| Cursor | `~/.cursor/skills/eggs` | `~/.cursor/mcp.json` (`url` + `headers`) |
| OpenCode | `~/.config/opencode/skills/eggs` | `~/.config/opencode/opencode.json` (`mcp`, `type: remote`) |
| Antigravity | `~/.gemini/config/skills/eggs` | `~/.gemini/antigravity/mcp_config.json` và `~/.gemini/config/mcp_config.json` (`serverUrl` + `headers`) |
| Hermes | `~/.hermes/skills/eggs` | `~/.hermes/config.yaml` (`mcp_servers`, `url` + `headers`) |

- Gỡ cấu hình MCP Jira cũ (`jira-mcp`, hoặc mục có biến môi trường trỏ tới jira.eggstech) để agent không ghi Jira thẳng. Giữ lại: `--keep-old`.
- Sao lưu mọi file cấu hình trước khi sửa: `<file>.bak-eggs-<thời điểm>`. Thư mục `skills/eggs` lạ đã có sẵn được đổi tên thành `eggs.bak-eggs-<thời điểm>`.
- Cuối cùng gọi thử `eggs_whoami` trên server; báo lỗi nếu PAT hoặc URL sai (mã thoát 3).
- Tham số khác: `--tools claude,cursor` (chỉ vài công cụ), `--skills-only`, `--no-verify`, `--dry-run`. PAT có thể đưa qua biến `EGGS_JIRA_PAT`.

Cập nhật kit: `git pull` (skill là liên kết nên không cần cài lại). Đổi PAT: chạy lại `install.sh`.

Kiểm tra bộ cài: `python3 -m unittest discover -s tests` (HOME giả, `claude` giả, server MCP giả; không đụng máy thật).

Chưa có: `references/plan.md` (tạo card từ tài liệu, chờ tool `eggs_plan_*`). `install.ps1` chưa chạy thử trên Windows.
