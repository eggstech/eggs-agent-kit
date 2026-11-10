#!/usr/bin/env python3
"""Cài/cập nhật kit /eggs cho Claude Code, Cursor, OpenCode, Antigravity, Hermes.

Làm 4 việc cho mỗi công cụ có trên máy:
1. Liên kết skills/eggs của kit vào thư mục skills toàn cục của công cụ.
2. Ghi cấu hình MCP `eggs-jira` (HTTP + header `Authorization: Token <PAT>`).
3. Gỡ cấu hình MCP Jira cũ (`jira-mcp`, hoặc mục nào trỏ tới jira.eggstech) trừ khi --keep-old.
4. Gọi thử `eggs_whoami` trên server.

Mọi file cấu hình bị sửa đều được sao lưu thành `<file>.bak-eggs-<thời điểm>` trước.
PAT lấy từ biến môi trường EGGS_JIRA_PAT hoặc hỏi ẩn; không bao giờ in ra.
Chỉ dùng thư viện chuẩn Python 3.8+.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SERVER = "eggs-jira"
OLD_NAMES = {"jira-mcp"}
OLD_MARKER = "eggstech"
KIT = Path(__file__).resolve().parent.parent
SKILL_SRC = KIT / "skills" / "eggs"
STAMP = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
ALL_TOOLS = ("claude", "cursor", "opencode", "antigravity", "hermes")


def home() -> Path:
    return Path(os.path.expanduser("~"))


def tool_specs() -> dict:
    h = home()
    return {
        "claude": {"detect": [h / ".claude"], "cmd": "claude",
                   "skills": [h / ".claude" / "skills"]},
        "cursor": {"detect": [h / ".cursor"], "cmd": None,
                   "skills": [h / ".cursor" / "skills"]},
        "opencode": {"detect": [h / ".config" / "opencode"], "cmd": "opencode",
                     "skills": [h / ".config" / "opencode" / "skills"]},
        "antigravity": {"detect": [h / ".gemini" / "antigravity", h / ".gemini" / "config"],
                        "cmd": "agy",
                        "skills": [h / ".gemini" / "config" / "skills"]},
        "hermes": {"detect": [h / ".hermes"], "cmd": "hermes",
                   "skills": [h / ".hermes" / "skills"]},
    }


class Ctx:
    def __init__(self, url: str | None, pat: str | None, dry_run: bool, keep_old: bool):
        self.url = url
        self.pat = pat
        self.dry_run = dry_run
        self.keep_old = keep_old
        self.lines: list[str] = []

    def say(self, msg: str) -> None:
        if self.pat:
            msg = msg.replace(self.pat, "***")
        print(msg)

    @property
    def auth(self) -> str:
        return f"Token {self.pat}"


# ---------- file helpers ----------

def backup(ctx: Ctx, path: Path) -> None:
    if path.exists() and not ctx.dry_run:
        shutil.copy2(path, path.with_name(f"{path.name}.bak-eggs-{STAMP}"))


def write_text(ctx: Ctx, path: Path, text: str) -> None:
    if ctx.dry_run:
        return
    existed = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(ctx, path)
    tmp = path.with_name(path.name + ".eggs-tmp")
    tmp.write_text(text, encoding="utf-8")
    if existed:
        shutil.copymode(path, tmp)
    else:
        os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8") or "{}")
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def looks_old(name: str, entry) -> bool:
    if name == SERVER:
        return False
    if name in OLD_NAMES:
        return True
    if isinstance(entry, dict):
        env = entry.get("env") or entry.get("environment") or {}
        if isinstance(env, dict) and any(OLD_MARKER in str(v) for v in env.values()):
            return True
    return False


def edit_json_servers(ctx: Ctx, path: Path, section: str, entry: dict, label: str) -> None:
    data = load_json(path)
    if data is None:
        ctx.say(f"  ! {label}: không đọc được {path} (không phải JSON thuần). Tự thêm mục `{SERVER}` theo README.")
        return
    servers = data.setdefault(section, {})
    if not isinstance(servers, dict):
        ctx.say(f"  ! {label}: `{section}` trong {path} không phải object; bỏ qua.")
        return
    removed = []
    if not ctx.keep_old:
        removed = [n for n, e in list(servers.items()) if looks_old(n, e)]
        for n in removed:
            del servers[n]
    action = "cập nhật" if SERVER in servers else "thêm"
    servers[SERVER] = entry
    write_text(ctx, path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    ctx.say(f"  - MCP: {action} `{SERVER}` trong {path}")
    for n in removed:
        ctx.say(f"  - MCP: gỡ cấu hình cũ `{n}` trong {path}")


# ---------- hermes (YAML, sửa theo dòng) ----------

def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def edit_hermes_yaml(ctx: Ctx, path: Path) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.splitlines()
    top = None
    for i, line in enumerate(lines):
        if re.match(r"^mcp_servers:\s*(\{\s*\})?\s*(#.*)?$", line):
            top = i
            lines[i] = "mcp_servers:"
            break
        if line.startswith("mcp_servers:"):
            ctx.say(f"  ! hermes: `mcp_servers` trong {path} viết dạng một dòng; tự thêm `{SERVER}` theo README.")
            return
    if top is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append("mcp_servers:")
        top = len(lines) - 1
    end = len(lines)
    for j in range(top + 1, len(lines)):
        if lines[j].strip() and not lines[j].lstrip().startswith("#") and _indent(lines[j]) == 0:
            end = j
            break
    child = 2
    for j in range(top + 1, end):
        if lines[j].strip() and not lines[j].lstrip().startswith("#"):
            child = _indent(lines[j])
            break
    drop = {SERVER} | (set() if ctx.keep_old else OLD_NAMES)
    removed = []
    out = lines[: top + 1]
    j = top + 1
    while j < end:
        m = re.match(r"^( *)([A-Za-z0-9_.\"'-]+):\s*$", lines[j])
        name = m.group(2).strip("\"'") if m else None
        if m and len(m.group(1)) == child and name in drop:
            if name != SERVER:
                removed.append(name)
            j += 1
            while j < end and (not lines[j].strip() or _indent(lines[j]) > child):
                j += 1
            continue
        out.append(lines[j])
        j += 1
    pad = " " * child
    block = [
        f"{pad}{SERVER}:",
        f"{pad}{pad}url: {json.dumps(ctx.url)}",
        f"{pad}{pad}headers:",
        f"{pad}{pad}{pad}Authorization: {json.dumps(ctx.auth)}",
    ]
    out[top + 1: top + 1] = block
    out.extend(lines[end:])
    write_text(ctx, path, "\n".join(out) + "\n")
    ctx.say(f"  - MCP: ghi `{SERVER}` trong {path}")
    for n in removed:
        ctx.say(f"  - MCP: gỡ cấu hình cũ `{n}` trong {path}")


# ---------- per tool ----------

def link_skill(ctx: Ctx, skills_dir: Path) -> None:
    dst = skills_dir / "eggs"
    try:
        if dst.is_symlink() or dst.exists():
            if dst.resolve() == SKILL_SRC.resolve():
                ctx.say(f"  - skill: {dst} đã trỏ đúng kit")
                return
            ctx.say(f"  - skill: {dst} đã có, sao lưu thành eggs.bak-eggs-{STAMP}")
            if not ctx.dry_run:
                dst.rename(dst.with_name(f"eggs.bak-eggs-{STAMP}"))
        if ctx.dry_run:
            ctx.say(f"  - skill: sẽ liên kết {dst} -> {SKILL_SRC}")
            return
        skills_dir.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(SKILL_SRC, dst, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                raise
            subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(SKILL_SRC)],
                           check=True, capture_output=True)
        ctx.say(f"  - skill: liên kết {dst} -> {SKILL_SRC}")
    except OSError as exc:
        ctx.say(f"  ! skill: không tạo được liên kết {dst}: {exc}")


def mcp_claude(ctx: Ctx) -> None:
    exe = shutil.which("claude")
    if not exe:
        ctx.say("  ! claude: không thấy lệnh `claude`; thêm MCP bằng tay theo README.")
        return
    names = [SERVER] + ([] if ctx.keep_old else sorted(OLD_NAMES))
    for name in names:
        found = subprocess.run([exe, "mcp", "get", name], capture_output=True, text=True).returncode == 0
        if not found:
            continue
        if not ctx.dry_run:
            subprocess.run([exe, "mcp", "remove", name, "-s", "user"], capture_output=True, text=True)
        if name != SERVER:
            ctx.say(f"  - MCP: gỡ cấu hình cũ `{name}` (claude, scope user)")
    if ctx.dry_run:
        ctx.say(f"  - MCP: sẽ thêm `{SERVER}` (claude, scope user)")
        return
    res = subprocess.run(
        [exe, "mcp", "add", "--transport", "http", "--scope", "user",
         SERVER, ctx.url, "--header", f"Authorization: {ctx.auth}"],
        capture_output=True, text=True,
    )
    if res.returncode == 0:
        ctx.say(f"  - MCP: thêm `{SERVER}` (claude, scope user)")
    else:
        ctx.say(f"  ! claude mcp add lỗi: {(res.stderr or res.stdout).strip()[:300]}")


def mcp_cursor(ctx: Ctx) -> None:
    edit_json_servers(ctx, home() / ".cursor" / "mcp.json", "mcpServers",
                      {"url": ctx.url, "headers": {"Authorization": ctx.auth}}, "cursor")


def mcp_opencode(ctx: Ctx) -> None:
    base = home() / ".config" / "opencode"
    path = base / "opencode.json"
    if not path.exists() and (base / "opencode.jsonc").exists():
        ctx.say(f"  ! opencode: chỉ có opencode.jsonc (có chú thích); tự thêm mục `{SERVER}` theo README.")
        return
    edit_json_servers(ctx, path, "mcp",
                      {"type": "remote", "url": ctx.url,
                       "headers": {"Authorization": ctx.auth}, "enabled": True}, "opencode")


def mcp_antigravity(ctx: Ctx) -> None:
    g = home() / ".gemini"
    targets = [g / "antigravity" / "mcp_config.json", g / "config" / "mcp_config.json"]
    for path in targets:
        if path.exists() or path.parent.exists():
            edit_json_servers(ctx, path, "mcpServers",
                              {"serverUrl": ctx.url, "headers": {"Authorization": ctx.auth},
                               "disabled": False}, "antigravity")


def mcp_hermes(ctx: Ctx) -> None:
    edit_hermes_yaml(ctx, home() / ".hermes" / "config.yaml")


MCP_WRITERS = {"claude": mcp_claude, "cursor": mcp_cursor, "opencode": mcp_opencode,
               "antigravity": mcp_antigravity, "hermes": mcp_hermes}


# ---------- verify ----------

def call_tool(url: str, auth: str, name: str, timeout: float = 20.0):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": {}}}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": auth, "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
    payload = raw
    if "data:" in raw and not raw.lstrip().startswith("{"):
        datas = [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]
        payload = datas[-1] if datas else "{}"
    return json.loads(payload)


def verify(ctx: Ctx) -> bool:
    for name in ("jira_eggs_whoami", "eggs_whoami"):
        try:
            msg = call_tool(ctx.url, ctx.auth, name)
        except urllib.error.HTTPError as exc:
            ctx.say(f"! Kiểm tra: server trả HTTP {exc.code}. PAT sai hoặc URL sai?")
            return False
        except (urllib.error.URLError, OSError, ValueError) as exc:
            ctx.say(f"! Kiểm tra: không gọi được {ctx.url}: {exc}")
            return False
        if "error" in msg:
            continue
        result = msg.get("result", {})
        text = " ".join(c.get("text", "") for c in result.get("content", []) if isinstance(c, dict))
        if result.get("isError"):
            if "Unknown tool" in text or "not found" in text.lower():
                continue
            ctx.say(f"! Kiểm tra: {name} báo lỗi: {text[:300]}")
            return False
        ctx.say(f"Kiểm tra: {name} OK: {text[:300]}")
        return True
    ctx.say("! Kiểm tra: server không có tool eggs_whoami (toolset eggs chưa bật?)")
    return False


# ---------- main ----------

def parse_args(argv):
    p = argparse.ArgumentParser(description="Cài/cập nhật kit /eggs.")
    p.add_argument("--url", default=os.environ.get("EGGS_MCP_URL"),
                   help="URL MCP, vd. https://<máy chủ>/mcp (hoặc biến EGGS_MCP_URL)")
    p.add_argument("--tools", default=",".join(ALL_TOOLS),
                   help="danh sách công cụ, cách nhau dấu phẩy (mặc định: mọi công cụ có trên máy)")
    p.add_argument("--skills-only", action="store_true", help="chỉ liên kết skill, không đụng cấu hình MCP")
    p.add_argument("--keep-old", action="store_true", help="giữ cấu hình MCP Jira cũ (jira-mcp)")
    p.add_argument("--no-verify", action="store_true", help="không gọi thử server")
    p.add_argument("--dry-run", action="store_true", help="chỉ in việc sẽ làm")
    args = p.parse_args(argv)
    wanted = [t.strip() for t in args.tools.split(",") if t.strip()]
    bad = [t for t in wanted if t not in ALL_TOOLS]
    if bad:
        p.error(f"công cụ không biết: {', '.join(bad)} (có: {', '.join(ALL_TOOLS)})")
    args.tools = wanted
    if not args.skills_only and not args.url:
        p.error("cần --url (hoặc biến EGGS_MCP_URL); Lead gửi địa chỉ này")
    if args.url and not re.match(r"^https?://", args.url):
        p.error("--url phải bắt đầu bằng https://")
    return args


def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if not (SKILL_SRC / "SKILL.md").exists():
        print(f"Không thấy {SKILL_SRC}/SKILL.md. Chạy script từ trong thư mục kit.")
        return 2
    pat = None
    if not args.skills_only:
        pat = os.environ.get("EGGS_JIRA_PAT") or getpass.getpass(
            "Jira Personal Access Token của bạn (Jira → Profile → Personal Access Tokens): ")
        pat = pat.strip()
        if not pat:
            print("Chưa có PAT. Dừng.")
            return 2
    ctx = Ctx(args.url, pat, args.dry_run, args.keep_old)
    specs = tool_specs()
    done = []
    for tool in args.tools:
        spec = specs[tool]
        present = any(p.exists() for p in spec["detect"]) or (spec["cmd"] and shutil.which(spec["cmd"]))
        if not present:
            continue
        ctx.say(f"{tool}:")
        for d in spec["skills"]:
            link_skill(ctx, d)
        if not args.skills_only:
            MCP_WRITERS[tool](ctx)
        done.append(tool)
    if not done:
        print("Không thấy công cụ nào (Claude Code, Cursor, OpenCode, Antigravity, Hermes) trên máy.")
        return 1
    if args.dry_run:
        print("(dry-run: chưa ghi gì)")
        return 0
    ok = True
    if not args.skills_only and not args.no_verify:
        ok = verify(ctx)
    print("Xong. Khởi động lại công cụ (hoặc mở phiên mới), rồi gõ /eggs.")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
