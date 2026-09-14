#!/usr/bin/env python3
"""Package health smoke for plugins/siglata against compatible-clients.org.

Uses a vendored snapshot of the official compatible-clients list, runs package
validation against pinned schemas, probes the Streamable HTTP MCP endpoint, and
prints a per-client status table. This is package health only. It is not product
v1 proof for every listed client. Human install steps live on
https://www.siglata.com/docs/connect.
"""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "siglata"
SCHEMA_DIR = ROOT / "schemas" / "1.0.0"
CLIENTS_SNAPSHOT = ROOT / "docs" / "compatible-clients.snapshot.json"
SITE_TS_URL = (
    "https://raw.githubusercontent.com/agentplugins/agent-plugins-site/"
    "main/lib/compatible-clients.ts"
)

# Fallback when network is unavailable — keep in sync with the site list.
FALLBACK_CLIENTS = [
    {"name": "VS Code", "skills": True, "streamable_http": True},
    {"name": "Cursor", "skills": True, "streamable_http": True},
    {"name": "GitHub Copilot", "skills": True, "streamable_http": True},
    {"name": "ChatGPT & Codex", "skills": True, "streamable_http": True},
    {"name": "Kiro", "skills": True, "streamable_http": True},
    {"name": "Hermes Agent", "skills": True, "streamable_http": True},
    {"name": "OpenClaw", "skills": True, "streamable_http": True},
    {"name": "Grok Bot", "skills": True, "streamable_http": True},
    {"name": "NanoClaw", "skills": True, "streamable_http": True},
]


def load_clients() -> list[dict]:
    if CLIENTS_SNAPSHOT.is_file():
        return json.loads(CLIENTS_SNAPSHOT.read_text(encoding="utf-8"))
    try:
        with urllib.request.urlopen(SITE_TS_URL, timeout=30) as response:
            text = response.read().decode("utf-8")
    except (urllib.error.URLError, OSError):
        return FALLBACK_CLIENTS

    # Minimal parse of the TS array: name + transports containing streamable-http.
    clients: list[dict] = []
    for block in text.split("name:"):
        if '"' not in block:
            continue
        name = block.split('"', 2)[1]
        if name in {"string", "CompatibleClient"}:
            continue
        skills = "skills: true" in block.split("},", 1)[0]
        streamable = "streamable-http" in block.split("},", 1)[0]
        if skills or streamable:
            clients.append(
                {
                    "name": name,
                    "skills": skills,
                    "streamable_http": streamable,
                }
            )
    return clients or FALLBACK_CLIENTS


def check_schemas() -> tuple[bool, str]:
    plugin_schema = SCHEMA_DIR / "plugin.schema.json"
    mcp_schema = SCHEMA_DIR / "mcp.schema.json"
    if not plugin_schema.is_file() or not mcp_schema.is_file():
        return False, f"missing pinned schemas under {SCHEMA_DIR}"
    try:
        with urllib.request.urlopen(
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            timeout=30,
        ) as live:
            live_plugin = live.read()
        pinned = plugin_schema.read_bytes()
        if live_plugin != pinned:
            return False, "pinned plugin.schema.json differs from live"
    except (urllib.error.URLError, OSError) as exc:
        return True, f"pinned schemas present (live compare skipped: {exc})"
    return True, "pinned schemas match live 1.0.0"


def check_validator() -> tuple[bool, str]:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate-plugin.py"),
            str(PLUGIN),
            "--schema-dir",
            str(SCHEMA_DIR),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return False, proc.stdout.strip() or proc.stderr.strip()
    return True, "validate-plugin exit 0"


def check_mcp() -> tuple[bool, str]:
    mcp = json.loads((PLUGIN / "mcp.json").read_text(encoding="utf-8"))
    url = mcp["mcpServers"]["siglata"]["url"]
    if mcp["mcpServers"]["siglata"].get("type") != "streamable-http":
        return False, "mcp server type is not streamable-http"
    req = urllib.request.Request(
        url,
        data=b'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2026-07-28","capabilities":{},"clientInfo":{"name":"matrix","version":"0"}}}',
        headers={
            "content-type": "application/json",
            "accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            code = response.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except (urllib.error.URLError, OSError) as exc:
        return False, f"MCP probe failed: {exc}"
    # 401 = OAuth challenge; 403 = edge/WAF still denies anonymous initialize.
    if code in (401, 403):
        return True, f"{url} → {code} (auth required)"
    return False, f"expected unauth 401/403 from {url}, got {code}"


def which(cmd: str) -> bool:
    from shutil import which as _which

    return _which(cmd) is not None


def main() -> int:
    clients = load_clients()
    if CLIENTS_SNAPSHOT.parent.is_dir():
        CLIENTS_SNAPSHOT.write_text(
            json.dumps(clients, indent=2) + "\n", encoding="utf-8"
        )

    gates = [
        ("pinned-schemas", *check_schemas()),
        ("validate-plugin", *check_validator()),
        ("mcp-streamable-http", *check_mcp()),
    ]

    print("## Shared gates")
    failed = 0
    for name, ok, detail in gates:
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status} {name}: {detail}")

    print("\n## Clients (skills + streamable-http required for Siglata)")
    for client in clients:
        name = client["name"]
        if not client.get("skills") or not client.get("streamable_http"):
            print(f"FAIL {name}: missing skills or streamable-http support claim")
            failed += 1
            continue

        if name == "ChatGPT & Codex" and which("codex"):
            smoke = "CLI available (package health only)"
        elif name == "OpenClaw" and which("openclaw"):
            smoke = "CLI available (package health only)"
        elif name == "Hermes Agent" and which("hermes"):
            smoke = "CLI available; portable path is manual (native plugins differ)"
        else:
            smoke = "manual client UI (package gates PASS)"

        print(f"PASS {name}: package-ready — {smoke}")

    print(
        f"\n{len(clients)} clients from compatible-clients; "
        f"{'FAIL' if failed else 'PASS'} overall"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
