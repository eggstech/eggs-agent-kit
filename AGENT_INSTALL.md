# Cài skill /eggs (hướng dẫn cho agent)

Bạn là agent trong IDE của một thành viên Eggstech. Hãy cài skill `/eggs` theo đúng các bước dưới đây. Chạy từng lệnh và báo kết quả ngắn gọn cho người dùng.

**Không bao giờ hỏi, đọc, in hay tự nhập Jira PAT của người dùng.** PAT do chính người dùng gõ vào terminal.

## 1. Kiểm tra Python

Cần Python 3: kiểm tra bằng `python3 --version` (Windows: `python --version`). Nếu chưa có, trên Windows hướng dẫn người dùng cài bằng `winget install Python.Python.3.12`. Không cần git.

## 2. Người dùng tự chạy lệnh cài

Lệnh cài tải kit về `~/eggs-agent-kit` (không cần git clone) rồi hỏi PAT ở chế độ gõ ẩn, nên **người dùng phải tự chạy lệnh này trong terminal của họ**. Không chạy hộ.

Hướng dẫn người dùng:

1. Tạo PAT: Jira → ảnh đại diện → Profile → Personal Access Tokens → Create token.
2. Mở terminal và chạy một lệnh:

   macOS / Linux:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh
   ```

   Windows (PowerShell):
   ```powershell
   irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex
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

Tự động: mỗi lần dùng `/eggs`, server báo nếu có bản mới và agent tự cập nhật. Muốn cập nhật tay: gõ `update skill eggs` trong IDE, hoặc chạy:

```bash
curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh -s -- --update
```

Windows (PowerShell): `$env:EGGS_KIT_UPDATE='1'; irm https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.ps1 | iex`

Máy đã cài bằng git clone vẫn dùng được các lệnh này (chúng chạy `git pull`). Chỉ cần chạy lại lệnh cài ở bước 2 khi đổi PAT.
