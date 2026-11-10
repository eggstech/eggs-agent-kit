# Kết quả thử skill `eggs` (10/11/2026)

Cách thử: agent con đóng vai agent trong IDE, đọc `context.md` (tool giả lập, có cả `jira-mcp` cũ và `google-chat`) và làm `scenarios.md`. Không gọi Jira thật.

| Lỗi | Không có skill (Sonnet / Haiku) | Có skill (Sonnet / Haiku) |
|---|---|---|
| Gửi câu trả lời vào group chat (S4) | Có / Có | Không / Không (đến 10/11) |
| S4 sau khi Lead cho phép gửi (10/11): hiện nội dung, hỏi gửi vào đâu, chờ đồng ý | | Đạt (Sonnet) |
| Đề nghị tự ghi Jira bằng tool ngoài `eggs_*` (tạo link, S3) | Có / Có | Không / Không |
| Lý do dời lịch tự do, bỏ `interrupted_by` (S3) | Không / Có | Không / Không |
| Chọn số "1" rồi tự quyết duyệt khi mục có 2 hành động (S5) | Không / Có | Không / Không |
| Dev Task dưới Story: hỏi Finish hay Submit QC (S6) | chưa thử | Có / Có |
| Story QC fail: truyền `bugs`, không gửi group dev (S7) | chưa thử | Đạt / Đạt |
| Bug stand-alone "đóng luôn", QC Owner trống: không Finish, hỏi ai test, dry-run `submit_qc` kèm `qc_owner` (S8, 10/11) | (skill bản cũ) — / Đạt | — / Đạt |

Chạy lại sau mỗi lần sửa `SKILL.md` hoặc `references/`.
