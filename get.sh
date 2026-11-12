#!/bin/sh
# Cài hoặc cập nhật kit /eggs, không cần git (macOS, Linux).
#   Cài:      curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh
#   Cập nhật: curl -fsSL https://raw.githubusercontent.com/eggstech/eggs-agent-kit/main/get.sh | sh -s -- --update
# Tham số thêm (sau --) chuyển cho install.sh, vd. --keep-old.
set -eu

REPO="eggstech/eggs-agent-kit"
BRANCH="${EGGS_KIT_BRANCH:-main}"
DIR="${EGGS_KIT_DIR:-$HOME/eggs-agent-kit}"
ARCHIVE="${EGGS_KIT_ARCHIVE_URL:-https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH}"
MCP_URL="${EGGS_MCP_URL:-https://jira.eggstech.io.vn/eggs-mcp/mcp}"

UPDATE=0
if [ "${1:-}" = "--update" ]; then
  UPDATE=1
  shift
fi

if [ -d "$DIR/.git" ] && command -v git >/dev/null 2>&1; then
  # Máy cài kiểu cũ (git clone): vẫn cập nhật bằng git.
  git -C "$DIR" pull --ff-only -q
else
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL "$ARCHIVE" | tar -xz -C "$TMP"
  SRC="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  if [ -z "$SRC" ] || [ ! -f "$SRC/skills/eggs/SKILL.md" ]; then
    echo "Tải kit lỗi: không thấy skills/eggs/SKILL.md." >&2
    exit 1
  fi
  OLD="$DIR.old.$$"
  if [ -e "$DIR" ]; then
    mv "$DIR" "$OLD"
  fi
  if ! mv "$SRC" "$DIR"; then
    [ -e "$OLD" ] && mv "$OLD" "$DIR"
    echo "Không chép được kit vào $DIR." >&2
    exit 1
  fi
  rm -rf "$OLD"
fi

VER="$(sed -n 's/.*Kit version: `\([0-9.]*\)`.*/\1/p' "$DIR/skills/eggs/SKILL.md" | head -n 1)"
echo "Kit /eggs ${VER:-?} tại $DIR"

if [ "$UPDATE" = 1 ]; then
  echo "Đã cập nhật. Đọc lại SKILL.md (hoặc mở phiên mới) để dùng bản mới."
  exit 0
fi

exec bash "$DIR/install.sh" --url "$MCP_URL" "$@"
