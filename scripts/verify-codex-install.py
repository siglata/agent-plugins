#!/usr/bin/env python3
"""Prove the Siglata plugin installs and loads in a real Codex CLI.

Runs Codex marketplace, plugin, MCP, and skill checks. Optional authenticated
tools/list when SIGLATA_MCP_TOKEN is set (same env var Codex reads for bearer
auth). This is not a substitute for a human browser OAuth click on
`codex mcp login`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PLUGIN_REF = "siglata@siglata-agent-plugins"
MARKETPLACE = "siglata-agent-plugins"
MCP_URL = "https://www.siglata.com/v1/mcp"
REQUIRED_SKILLS = ("siglata", "siglata-drive", "siglata-admin", "skill-creator")
TEACH_NEEDLES = ("sql_query", "relation_list", "attach_workbook")


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        text=True,
        capture_output=True,
    )


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    raise SystemExit(1)


def ok(msg: str) -> None:
    print(f"PASS {msg}")


def main() -> int:
    codex = shutil.which("codex")
    if not codex:
        fail("codex CLI not on PATH (install @openai/codex)")

    version = run([codex, "--version"])
    if version.returncode != 0:
        fail(f"codex --version exited {version.returncode}")
    ok(f"codex available ({version.stdout.strip() or version.stderr.strip()})")

    marketplaces = run([codex, "plugin", "marketplace", "list"])
    if marketplaces.returncode != 0:
        fail(f"plugin marketplace list: {marketplaces.stderr.strip()}")
    if MARKETPLACE not in marketplaces.stdout:
        add = run([codex, "plugin", "marketplace", "add", "siglata/agent-plugins"])
        if add.returncode != 0:
            fail(f"marketplace add: {add.stderr.strip() or add.stdout.strip()}")
        ok("marketplace add siglata/agent-plugins")
    else:
        ok(f"marketplace {MARKETPLACE} already configured")

    plugins = run([codex, "plugin", "list"])
    if plugins.returncode != 0:
        fail(f"plugin list: {plugins.stderr.strip()}")
    if PLUGIN_REF not in plugins.stdout or "installed" not in plugins.stdout:
        add_plugin = run([codex, "plugin", "add", PLUGIN_REF])
        if add_plugin.returncode != 0:
            fail(
                f"plugin add: {add_plugin.stderr.strip() or add_plugin.stdout.strip()}"
            )
        plugins = run([codex, "plugin", "list"])
        if PLUGIN_REF not in plugins.stdout:
            fail("plugin add did not list siglata@siglata-agent-plugins")
        ok(f"plugin add {PLUGIN_REF}")
    else:
        ok(f"plugin {PLUGIN_REF} installed")

    if "enabled" not in plugins.stdout:
        fail("plugin listed but not enabled")
    ok("plugin enabled")

    mcp = run([codex, "mcp", "list"])
    if mcp.returncode != 0:
        fail(f"mcp list: {mcp.stderr.strip()}")
    if "siglata" not in mcp.stdout or MCP_URL not in mcp.stdout:
        fail("mcp list missing siglata Streamable HTTP URL")
    ok(f"mcp list includes siglata → {MCP_URL}")

    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skill_roots = list(
        (home / "plugins" / "cache" / MARKETPLACE / "siglata").glob("*/skills")
    )
    if not skill_roots:
        # Marketplace checkout also carries skills before cache copies.
        market_skills = (
            home / ".tmp" / "marketplaces" / MARKETPLACE / "plugins" / "siglata" / "skills"
        )
        if market_skills.is_dir():
            skill_roots = [market_skills]
    if not skill_roots:
        fail(f"no skills under {home}/plugins/cache/{MARKETPLACE}/siglata")

    skills_dir = skill_roots[0]
    for name in REQUIRED_SKILLS:
        skill = skills_dir / name / "SKILL.md"
        if not skill.is_file():
            fail(f"missing skill {skill}")
    ok(f"skills present: {', '.join(REQUIRED_SKILLS)}")

    drive = (skills_dir / "siglata-drive" / "SKILL.md").read_text(encoding="utf-8")
    missing = [n for n in TEACH_NEEDLES if n not in drive]
    if missing:
        fail(f"siglata-drive teach path missing {missing}")
    ok(f"siglata-drive teaches {', '.join(TEACH_NEEDLES)}")

    prompt = run([codex, "debug", "prompt-input", "use siglata"])
    if prompt.returncode != 0:
        fail(f"debug prompt-input: {prompt.stderr.strip()}")
    lowered = prompt.stdout.lower()
    for needle in ("siglata", "siglata-drive", "skill"):
        if needle not in lowered:
            fail(f"prompt-input missing {needle}")
    ok("codex debug prompt-input loads siglata skills")

    token = os.environ.get("SIGLATA_MCP_TOKEN", "").strip()
    if not token:
        ok("skip authenticated tools/list (set SIGLATA_MCP_TOKEN to enable)")
        print("PASS overall (install + skills; auth optional)")
        return 0

    if "SIGLATA_MCP_TOKEN" not in mcp.stdout and "Bearer token" not in mcp.stdout:
        print(
            "WARN mcp list does not show bearer auth yet; "
            "add to ~/.codex/config.toml:\n"
            '[mcp_servers.siglata]\n'
            f'url = "{MCP_URL}"\n'
            'bearer_token_env_var = "SIGLATA_MCP_TOKEN"'
        )

    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {
                "_meta": {
                    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                    "io.modelcontextprotocol/clientCapabilities": {},
                    "io.modelcontextprotocol/clientInfo": {
                        "name": "verify-codex-install",
                        "version": "0.0.0",
                    },
                }
            },
        }
    ).encode()
    req = urllib.request.Request(
        MCP_URL,
        data=body,
        method="POST",
        headers={
            "authorization": f"Bearer {token}",
            "accept": "application/json, text/event-stream",
            "content-type": "application/json",
            "mcp-protocol-version": "2026-07-28",
            "mcp-method": "tools/list",
            "user-agent": "verify-codex-install/0.0.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        fail(f"authenticated tools/list HTTP {exc.code}: {exc.read()[:200]!r}")
    except urllib.error.URLError as exc:
        fail(f"authenticated tools/list network: {exc}")

    tools = payload.get("result", {}).get("tools", [])
    names = {t.get("name") for t in tools if isinstance(t, dict)}
    if names != {"execute", "search"}:
        fail(f"tools/list expected execute+search, got {sorted(names)}")
    ok("authenticated tools/list via SIGLATA_MCP_TOKEN → execute, search")
    print("PASS overall (install + skills + authenticated tools/list)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(0)
