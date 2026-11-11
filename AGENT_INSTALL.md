# Cài skill /eggs (hướng dẫn cho agent)

Bạn là agent trong IDE của một thành viên Eggstech. Hãy cài skill `/eggs` theo đúng các bước dưới đây. Chạy từng lệnh và báo kết quả ngắn gọn cho người dùng.

**Không bao giờ hỏi, đọc, in hay tự nhập Jira PAT của người dùng.** PAT do chính người dùng gõ vào terminal.

## 1. Lấy kit

Nếu `~/eggs-agent-kit` đã có thì cập nhật, chưa có thì clone:

```bash
git -C ~/eggs-agent-kit pull || git clone https://github.com/eggstech/eggs-agent-kit ~/eggs-agent-kit
```

Windows (PowerShell): thay `~` bằng `$HOME`.

Nếu clone báo lỗi quyền truy cập: dừng lại và nhắn người dùng "Tài khoản GitHub của bạn chưa được thêm vào repo eggstech/eggs-agent-kit, nhờ Lead thêm."

Cần Python 3: kiểm tra bằng `python3 --version` (Windows: `python --version`). Nếu chưa có, trên Windows hướng dẫn người dùng cài bằng `winget install Python.Python.3.12`.

## 2. Người dùng tự chạy bộ cài

Bộ cài hỏi PAT ở chế độ gõ ẩn, nên **người dùng phải tự chạy lệnh này trong terminal của họ**. Không chạy hộ.

Hướng dẫn người dùng:

1. Tạo PAT: Jira → ảnh đại diện → Profile → Personal Access Tokens → Create token.
2. Mở terminal và chạy lệnh tương ứng:

   macOS / Linux:
   ```bash
   cd ~/eggs-agent-kit && ./install.sh --url https://jira.eggstech.io.vn/eggs-mcp/mcp
   ```

   Windows (PowerShell):
   ```powershell
   cd $HOME\eggs-agent-kit; powershell -ExecutionPolicy Bypass -File .\install.ps1 --url https://jira.eggstech.io.vn/eggs-mcp/mcp
   ```

3. Dán PAT khi được hỏi, rồi Enter.
4. Báo lại cho agent dòng cuối cùng của kết quả. Không gửi PAT.

Bộ cài tự lo các việc sau:

- Gắn skill vào mọi công cụ có trên máy: Claude Code, Cursor, OpenCode, Antigravity, Hermes.
- Cấu hình MCP `eggs-jira`.
- Gỡ MCP Jira cũ.
- Sao lưu các file cấu hình trước khi sửa.
- Gọi thử server để kiểm tra PAT.

Nếu bộ cài thoát với mã 3 hoặc báo lỗi PAT/URL: người dùng tạo lại PAT rồi chạy lại lệnh ở bước 2.

## 3. Kiểm tra

1. Nhắc người dùng **mở phiên mới** trong IDE (hoặc khởi động lại IDE), để skill và MCP mới được nạp.
2. Ở phiên mới, người dùng gõ `/eggs`.

Kết quả đúng là agent trả lời tên người dùng, vai trò theo từng dự án và danh sách việc cần làm.

Nếu agent báo "chưa có vai trò trong dự án nào": nhờ Lead thêm người dùng vào Project Role (Developers / Testers / Business Analysts) của dự án.

## Cập nhật sau này

Người dùng gõ `update skill eggs` trong IDE, hoặc tự chạy:

```bash
git -C ~/eggs-agent-kit pull
```

Sau đó mở phiên mới. Chỉ cần chạy lại bộ cài khi đổi PAT.
