#!/usr/bin/env bash
# Cài/cập nhật kit /eggs (macOS, Linux). Ví dụ:
#   ./install.sh --url https://<máy chủ MCP>/mcp
# Tham số: xem ./install.sh --help
set -euo pipefail
cd "$(dirname "$0")"
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "Cần python3. macOS: xcode-select --install; Ubuntu: sudo apt install python3" >&2
  exit 2
fi
exec "$PY" scripts/install.py "$@"
