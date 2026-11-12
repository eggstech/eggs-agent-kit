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

Gửi cho agent của bạn file [AGENT_INSTALL.md](AGENT_INSTALL.md) để nó hướng dẫn cài; hoặc tự làm theo các bước dưới.

Cần: Python 3 (macOS có sẵn; Windows `winget install Python.Python.3.12`), Jira PAT của chính mình (Jira → Profile → Personal Access Tokens). Không cần git.

```bash
curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh
```

Windows (PowerShell): `irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex`

Lệnh này tải kit về `~/eggs-agent-kit` (bản nén từ GitHub, không clone) rồi chạy `install.sh` / `install.ps1` với URL MCP `https://jira.eggstech.io.vn/eggs-mcp/mcp`. Đổi URL: biến `EGGS_MCP_URL`; tham số thêm cho bộ cài: `curl ... | sh -s -- --keep-old` (Windows: `$env:EGGS_KIT_ARGS='--keep-old'`).

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

Cập nhật kit:

- Tự động: SKILL.md có dòng `Kit version`. Agent gửi giá trị này trong `eggs_next(kit=...)`; server đọc SKILL.md mới nhất trên GitHub (nhớ 10 phút) và khi bản của agent cũ hơn thì trả `kit_update` kèm lệnh, agent tự chạy rồi đọc lại SKILL.md.
- Tay: gõ `update skill eggs`, hoặc `curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh -s -- --update` (Windows: `$env:EGGS_KIT_UPDATE='1'; irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex`). Máy cài bằng git clone thì lệnh này chạy `git pull`.
- Skill là liên kết tới `~/eggs-agent-kit/skills/eggs` nên không cần cài lại; đổi PAT thì chạy lại lệnh cài.

**Người sửa kit:** mỗi lần đổi nội dung trong `skills/`, tăng `Kit version` trong SKILL.md (dạng `năm.tháng.ngày.số`, vd. `2026.11.12.2`). Không tăng thì máy người dùng không tự cập nhật.

Kiểm tra bộ cài: `python3 -m unittest discover -s tests` (HOME giả, `claude` giả, server MCP giả; không đụng máy thật).

Chưa có: `references/plan.md` (tạo card từ tài liệu, chờ tool `eggs_plan_*`). `install.ps1` chưa chạy thử trên Windows.
