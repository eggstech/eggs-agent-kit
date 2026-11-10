"""Kiểm tra scripts/install.py trong HOME giả. Chạy: python3 -m unittest discover -s tests"""

import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SCRIPT = KIT / "scripts" / "install.py"
PAT = "FAKE-PAT-123456"


class Stub(http.server.BaseHTTPRequestHandler):
    status = 200
    seen: list = []

    def do_POST(self):  # noqa: N802
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        Stub.seen.append((self.headers.get("Authorization"), body["params"]["name"]))
        if Stub.status != 200:
            self.send_response(Stub.status)
            self.end_headers()
            return
        if body["params"]["name"] != "jira_eggs_whoami":
            out = {"jsonrpc": "2.0", "id": 1, "error": {"code": -32602, "message": "Unknown tool"}}
        else:
            out = {"jsonrpc": "2.0", "id": 1,
                   "result": {"content": [{"type": "text", "text": '{"user":"henry"}'}]}}
        data = ("event: message\ndata: " + json.dumps(out) + "\n\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


HERMES = """model:
  default: x
mcp_servers:
  other:
    command: "npx"
    args: ["a"]
  jira-mcp:
    command: "npx"
    env:
      JIRA_DOMAIN: "jira.eggstech.io.vn"
display:
  skin: default
"""


class InstallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = http.server.HTTPServer(("127.0.0.1", 0), Stub)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.httpd.server_address[1]}/mcp"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def setUp(self):
        Stub.status = 200
        Stub.seen = []
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        h = self.home
        (h / ".claude").mkdir(parents=True)
        (h / ".cursor").mkdir()
        (h / ".cursor" / "mcp.json").write_text(json.dumps({"mcpServers": {"codegraph": {"command": "cg"}}}))
        (h / ".config" / "opencode").mkdir(parents=True)
        (h / ".config" / "opencode" / "opencode.json").write_text(json.dumps({
            "model": "m", "mcp": {
                "jira-mcp": {"type": "local", "command": ["npx", "x"]},
                "old-by-env": {"type": "local", "environment": {"JIRA_DOMAIN": "https://jira.eggstech.io.vn"}},
                "paper": {"type": "local", "command": ["p"]}}}))
        (h / ".gemini" / "antigravity").mkdir(parents=True)
        (h / ".gemini" / "config").mkdir()
        (h / ".gemini" / "antigravity" / "mcp_config.json").write_text(json.dumps({"mcpServers": {
            "jira-mcp": {"command": "npx", "env": {"JIRA_API_TOKEN": "old"}}, "shadcn": {"command": "s"}}}))
        (h / ".hermes").mkdir()
        (h / ".hermes" / "config.yaml").write_text(HERMES)
        # claude giả: ghi lại tham số; `mcp get jira-mcp` coi như có.
        self.bin = Path(self.tmp.name) / "bin"
        self.bin.mkdir()
        self.claude_log = Path(self.tmp.name) / "claude.log"
        stub = self.bin / "claude"
        stub.write_text(f"#!/bin/sh\necho \"$@\" >> {self.claude_log}\n"
                        "[ \"$2\" = get ] && [ \"$3\" = jira-mcp ] && exit 0\n"
                        "[ \"$2\" = get ] && exit 1\nexit 0\n")
        stub.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, *args, pat=PAT):
        env = {"HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin", "EGGS_JIRA_PAT": pat}
        return subprocess.run([sys.executable, str(SCRIPT), *args], env=env,
                              capture_output=True, text=True, timeout=60)

    def j(self, rel):
        return json.loads((self.home / rel).read_text())

    def test_full_install(self):
        r = self.run_install("--url", self.url)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn(PAT, r.stdout + r.stderr)
        auth = f"Token {PAT}"
        # skills
        for d in [".claude/skills", ".cursor/skills", ".config/opencode/skills",
                  ".gemini/config/skills", ".hermes/skills"]:
            link = self.home / d / "eggs"
            self.assertEqual(link.resolve(), (KIT / "skills" / "eggs").resolve(), d)
        # cursor
        cur = self.j(".cursor/mcp.json")["mcpServers"]
        self.assertEqual(cur["eggs-jira"], {"url": self.url, "headers": {"Authorization": auth}})
        self.assertIn("codegraph", cur)
        # opencode: gỡ jira-mcp và mục cũ theo env, giữ paper
        oc = self.j(".config/opencode/opencode.json")
        self.assertEqual(oc["model"], "m")
        self.assertEqual(set(oc["mcp"]), {"paper", "eggs-jira"})
        self.assertEqual(oc["mcp"]["eggs-jira"]["type"], "remote")
        self.assertEqual(oc["mcp"]["eggs-jira"]["headers"]["Authorization"], auth)
        # antigravity: cả IDE lẫn CLI
        ide = self.j(".gemini/antigravity/mcp_config.json")["mcpServers"]
        self.assertEqual(set(ide), {"shadcn", "eggs-jira"})
        self.assertEqual(ide["eggs-jira"]["serverUrl"], self.url)
        cli = self.j(".gemini/config/mcp_config.json")["mcpServers"]
        self.assertEqual(cli["eggs-jira"]["headers"]["Authorization"], auth)
        self.assertEqual(os.stat(self.home / ".gemini/config/mcp_config.json").st_mode & 0o777, 0o600)
        # hermes
        y = (self.home / ".hermes/config.yaml").read_text()
        self.assertNotIn("jira-mcp", y)
        self.assertIn("  other:\n    command: \"npx\"", y)
        self.assertIn(f'  eggs-jira:\n    url: "{self.url}"\n    headers:\n      Authorization: "{auth}"', y)
        self.assertIn("display:\n  skin: default", y)
        # claude
        log = self.claude_log.read_text()
        self.assertIn("mcp remove jira-mcp -s user", log)
        self.assertIn(f"mcp add --transport http --scope user eggs-jira {self.url} --header Authorization: {auth}", log)
        # sao lưu
        self.assertTrue(list((self.home / ".hermes").glob("config.yaml.bak-eggs-*")))
        self.assertTrue(list((self.home / ".cursor").glob("mcp.json.bak-eggs-*")))
        # kiểm tra server: đúng tool, đúng header
        self.assertEqual(Stub.seen[0], (auth, "jira_eggs_whoami"))
        self.assertIn("henry", r.stdout)

    def test_rerun_is_idempotent(self):
        self.run_install("--url", self.url)
        first = (self.home / ".hermes/config.yaml").read_text()
        r = self.run_install("--url", self.url)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        y = (self.home / ".hermes/config.yaml").read_text()
        self.assertEqual(y, first)
        self.assertEqual(y.count("eggs-jira:"), 1)
        self.assertIn("đã trỏ đúng kit", r.stdout)

    def test_keep_old(self):
        r = self.run_install("--url", self.url, "--keep-old", "--no-verify")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("jira-mcp", self.j(".gemini/antigravity/mcp_config.json")["mcpServers"])
        self.assertIn("jira-mcp", (self.home / ".hermes/config.yaml").read_text())
        self.assertNotIn("remove jira-mcp", self.claude_log.read_text())

    def test_dry_run_writes_nothing(self):
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        r = self.run_install("--url", self.url, "--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        after = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.home / ".claude/skills/eggs").exists())
        self.assertNotIn("mcp add", self.claude_log.read_text() if self.claude_log.exists() else "")
        self.assertEqual(Stub.seen, [])

    def test_bad_pat_exit_3(self):
        Stub.status = 401
        r = self.run_install("--url", self.url)
        self.assertEqual(r.returncode, 3, r.stdout)
        self.assertIn("HTTP 401", r.stdout)

    def test_hermes_without_mcp_section_and_only_selected_tools(self):
        (self.home / ".hermes/config.yaml").write_text("model:\n  default: x\n")
        r = self.run_install("--url", self.url, "--tools", "hermes", "--no-verify")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        y = (self.home / ".hermes/config.yaml").read_text()
        self.assertTrue(y.startswith("model:\n  default: x\n\nmcp_servers:\n  eggs-jira:\n"), y)
        self.assertFalse((self.home / ".claude/skills/eggs").exists())
        self.assertNotIn("eggs-jira", (self.home / ".cursor/mcp.json").read_text())

    def test_skills_only_needs_no_url_or_pat(self):
        r = self.run_install("--skills-only", pat="")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.home / ".cursor/skills/eggs/SKILL.md").exists())
        self.assertNotIn("eggs-jira", (self.home / ".cursor/mcp.json").read_text())

    def test_url_required(self):
        r = self.run_install()
        self.assertEqual(r.returncode, 2)
        self.assertIn("--url", r.stderr)

    def test_existing_foreign_skill_is_backed_up(self):
        d = self.home / ".claude/skills/eggs"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("old")
        r = self.run_install("--url", self.url, "--tools", "claude", "--no-verify")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(d.is_symlink())
        backups = list((self.home / ".claude/skills").glob("eggs.bak-eggs-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "SKILL.md").read_text(), "old")


if __name__ == "__main__":
    unittest.main()
