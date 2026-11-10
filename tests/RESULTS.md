# Kết quả thử skill `eggs` (10/11/2026)

Cách thử: agent con đóng vai agent trong IDE, đọc `context.md` (tool giả lập, có cả `jira-mcp` cũ và `google-chat`) và làm `scenarios.md`. Không gọi Jira thật.

| Lỗi | Không có skill (Sonnet / Haiku) | Có skill (Sonnet / Haiku) |
|---|---|---|
| Gửi câu trả lời vào group chat (S4) | Có / Có | Không / Không (đến 10/11) |
| S4 sau khi Lead cho phép gửi (10/11): hiện nội dung, hỏi gửi vào đâu, chờ đồng ý | | Đạt (Sonnet) |
| S5 tool ghi an toàn (10/11, Lead mở 6 tool: comment, watcher, link). Bản cũ: từ chối comment "hello 2" và link relates (lỗi tuan.bui gặp). Bản mới: comment/link qua eggs-jira sau `Sẽ làm:` + đồng ý; vẫn từ chối `jira_update_issue` đổi Due Date (hướng sang xin dời lịch) và từ chối chuyển trạng thái qua MCP `jira` cũ | Không đạt (bản cũ) | Đạt (Sonnet) |
| U1/U2 "update skill eggs" (10/11). Bản cũ: pull được khi đề bài cho sẵn đường dẫn clone, nhưng khi pull lỗi lại đề nghị tự `stash`/bỏ thay đổi. Bản mới: `git -C <thư mục skill> pull --ff-only` + `log -1`, báo mở phiên mới; lỗi thì hiện nguyên thông báo git và đưa lệnh cho người dùng, không stash/reset/force, không gọi `eggs_*` | Một phần (bản cũ) | Đạt (Sonnet) |
| L1–L4 gỡ link và chuyển Epic (10/11, Lead mở `jira_remove_issue_link`, `jira_link_to_epic`). Bản cũ: từ chối gỡ link Relates (L1) và từ chối BA chuyển Epic (L4). Bản mới: L1 `Sẽ làm:` gỡ link 30011, chờ đồng ý; L2 từ chối gỡ `Interrupts` (bằng chứng dời lịch); L3 dev xin chuyển Epic bị từ chối, L3b không chỉ dev tự đổi trên web; L4 BA (`lead_ba`) `Sẽ làm:` RFID-E3 → RFID-E4, chờ đồng ý | Không đạt (bản cũ) | Đạt (Sonnet, sau khi chặn gợi ý tự sửa trên web) |
| N1–N6 tool mới sau lượt U (10/11 tối). Bản cũ: N6 giúp Dev tạo Story; N2 gợi ý `ALL - CHUNG` dù dự án có Actor riêng; N4 vẫn nói "Start Analysis"; N5 bắt QC chọn pass/fail trước khi tạo Bug. Bản mới: N1 `bug_sub` dưới Story đang test, không QC Fail; N2 `eggs_components` → đề xuất `KT - KẾ TOÁN` cùng Story trong một `Sẽ làm:`, N2b vẫn không dùng `ALL - CHUNG` khi người dùng đòi; N3 `append` mô tả kèm diff; N4 chỉ `Analysis Done` trên web Jira; N5 Bug stand-alone `related_to` EGGSBOX-38; N6 từ chối Dev tạo Story | Không đạt (bản cũ) | Đạt (Sonnet, sau khi chặn gợi ý `ALL - CHUNG`) |
| Đề nghị tự ghi Jira bằng tool ngoài `eggs_*` (tạo link, S3) | Có / Có | Không / Không |
| Lý do dời lịch tự do, bỏ `interrupted_by` (S3) | Không / Có | Không / Không |
| Chọn số "1" rồi tự quyết duyệt khi mục có 2 hành động (S5) | Không / Có | Không / Không |
| Dev Task dưới Story: hỏi Finish hay Submit QC (S6) | chưa thử | Có / Có |
| Story QC fail: truyền `bugs`, không gửi group dev (S7) | chưa thử | Đạt / Đạt |
| Bug stand-alone "đóng luôn", QC Owner trống: không Finish, hỏi ai test, dry-run `submit_qc` kèm `qc_owner` (S8, 10/11) | (skill bản cũ) — / Đạt | — / Đạt |

Chạy lại sau mỗi lần sửa `SKILL.md` hoặc `references/`.
