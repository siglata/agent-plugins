#!/usr/bin/env python3
"""Validate an Agent Plugins 1.0.0 package against official schemas and checklist items."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

import yaml
from jsonschema import Draft202012Validator

PLUGIN_SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
SCHEMA_VERSION = "1.0.0"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


@dataclass(frozen=True)
class Check:
    id: str
    path: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class Ctx:
    plugin_root: Path
    plugin_schema: dict[str, Any]
    mcp_schema: dict[str, Any]


CheckFn = Callable[[Ctx], list[Check]]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def display_path(path: Path, plugin_root: Path) -> str:
    base = plugin_root.parent.parent
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path)


def schema_version_from_url(schema_url: str) -> str | None:
    parts = urlparse(schema_url).path.strip("/").split("/")
    if len(parts) >= 3 and parts[-3] == "schemas":
        return parts[-2]
    return None


def load_schema(url: str, schema_dir: Path | None) -> dict[str, Any]:
    filename = url.rstrip("/").rsplit("/", 1)[-1]
    cached: Path | None = None
    if schema_dir is not None:
        schema_dir.mkdir(parents=True, exist_ok=True)
        cached = schema_dir / filename
        if cached.is_file():
            return json.loads(cached.read_text(encoding="utf-8"))

    try:
        with urlopen(url, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except (URLError, OSError) as exc:
        raise SystemExit(
            f"Failed to fetch schema {url}: {exc}. "
            "Pass --schema-dir with cached schema files, or fix network access."
        ) from exc

    data = json.loads(raw)
    if cached is not None:
        cached.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def schema_error(document: Any, schema: dict[str, Any]) -> str | None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda e: list(e.path),
    )
    if not errors:
        return None
    err = errors[0]
    location = ".".join(str(p) for p in err.path) or "<root>"
    return f"{location}: {err.message}"


def is_loopback_host(host: str) -> bool:
    hostname = host.strip("[]").lower()
    if hostname == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def remote_url_error(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return f"URL must be http or https, got {parsed.scheme!r}"
    if parsed.username is not None or parsed.password is not None:
        return "URL must not contain embedded credentials (user:pass@)"
    if "@" in (parsed.netloc or ""):
        return "URL must not contain embedded credentials (user:pass@)"
    host = parsed.hostname
    if not host:
        return "URL must include a host"
    if not is_loopback_host(host) and parsed.scheme != "https":
        return "Non-loopback URLs must use HTTPS"
    return None


def parse_skill_frontmatter(text: str) -> dict[str, Any] | str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "missing YAML frontmatter delimited by ---"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return "frontmatter must be a YAML mapping"
    return data


def check_plugin_manifest(ctx: Ctx) -> list[Check]:
    path = ctx.plugin_root / "plugin.json"
    display = display_path(path, ctx.plugin_root)
    if not path.is_file():
        return [Check("plugin-json-exists", display, False, "plugin.json is required")]

    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Check("plugin-json-parse", display, False, f"invalid JSON: {exc}")]

    error = schema_error(document, ctx.plugin_schema)
    if error:
        return [Check("plugin-json-schema", display, False, error)]

    schema_url = document.get("$schema", "")
    version = schema_version_from_url(schema_url) if isinstance(schema_url, str) else None
    if version != SCHEMA_VERSION:
        return [
            Check(
                "plugin-schema-version",
                display,
                False,
                f"$schema version must be {SCHEMA_VERSION}, got {version!r}",
            )
        ]

    return [
        Check("plugin-json-schema", display, True, "valid against plugin.schema.json"),
        Check("plugin-schema-version", display, True, f"$schema version is {SCHEMA_VERSION}"),
    ]


def check_mcp(ctx: Ctx) -> list[Check]:
    path = ctx.plugin_root / "mcp.json"
    display = display_path(path, ctx.plugin_root)
    if not path.exists():
        return [Check("mcp-json", display, True, "mcp.json absent (optional)")]

    if not path.is_file():
        return [Check("mcp-json", display, False, "mcp.json exists but is not a regular file")]

    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Check("mcp-json-parse", display, False, f"invalid JSON: {exc}")]

    checks: list[Check] = []
    error = schema_error(document, ctx.mcp_schema)
    checks.append(
        Check(
            "mcp-json-schema",
            display,
            error is None,
            "valid against mcp.schema.json" if error is None else error,
        )
    )

    plugin_version = None
    plugin_path = ctx.plugin_root / "plugin.json"
    if plugin_path.is_file():
        try:
            plugin_doc = json.loads(plugin_path.read_text(encoding="utf-8"))
            plugin_schema = plugin_doc.get("$schema", "")
            if isinstance(plugin_schema, str):
                plugin_version = schema_version_from_url(plugin_schema)
        except json.JSONDecodeError:
            plugin_version = None

    mcp_schema_url = document.get("$schema", "")
    mcp_version = (
        schema_version_from_url(mcp_schema_url) if isinstance(mcp_schema_url, str) else None
    )
    version_ok = plugin_version == SCHEMA_VERSION and mcp_version == SCHEMA_VERSION
    if version_ok:
        detail = f"mcp.json and plugin.json both target {SCHEMA_VERSION}"
    else:
        detail = (
            f"schema versions must both be {SCHEMA_VERSION} "
            f"(plugin={plugin_version!r}, mcp={mcp_version!r})"
        )
    checks.append(Check("mcp-schema-version", display, version_ok, detail))

    servers = document.get("mcpServers")
    if isinstance(servers, dict):
        for name, server in servers.items():
            if not isinstance(server, dict):
                continue
            if server.get("type") not in ("streamable-http", "sse"):
                continue
            url = server.get("url")
            server_path = f"{display}#mcpServers.{name}.url"
            check_id = f"mcp-url-{name}"
            if not isinstance(url, str):
                checks.append(Check(check_id, server_path, False, "url must be a string"))
                continue
            url_error = remote_url_error(url)
            checks.append(
                Check(
                    check_id,
                    server_path,
                    url_error is None,
                    "remote URL satisfies HTTPS and credential rules"
                    if url_error is None
                    else url_error,
                )
            )

    return checks


def check_skills(ctx: Ctx) -> list[Check]:
    skills_dir = ctx.plugin_root / "skills"
    display = display_path(skills_dir, ctx.plugin_root)
    if not skills_dir.exists():
        return [Check("skills", display, True, "skills/ absent (optional)")]

    if not skills_dir.is_dir():
        return [Check("skills-dir", display, False, "skills/ must be a directory")]

    checks: list[Check] = [Check("skills-dir", display, True, "skills/ is a directory")]
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = child / "SKILL.md"
        skill_display = display_path(skill_md, ctx.plugin_root)
        if skill_md.is_symlink() or not skill_md.is_file():
            checks.append(
                Check(
                    f"skill-md-{child.name}",
                    skill_display,
                    False,
                    "SKILL.md regular file is required",
                )
            )
            continue

        frontmatter = parse_skill_frontmatter(skill_md.read_text(encoding="utf-8"))
        if isinstance(frontmatter, str):
            checks.append(
                Check(f"skill-frontmatter-{child.name}", skill_display, False, frontmatter)
            )
            continue

        name = frontmatter.get("name")
        description = frontmatter.get("description")
        name_ok = (
            isinstance(name, str)
            and 1 <= len(name) <= 64
            and SKILL_NAME_RE.fullmatch(name) is not None
            and name == child.name
        )
        if name_ok:
            name_detail = f"name {name!r} matches directory and Agent Skills rules"
        elif not isinstance(name, str):
            name_detail = "name must be a string"
        elif name != child.name:
            name_detail = f"name {name!r} must match directory {child.name!r}"
        else:
            name_detail = (
                "name must be 1–64 chars of [a-z0-9-]+ with no leading/trailing "
                "hyphen and no consecutive hyphens"
            )
        checks.append(Check(f"skill-name-{child.name}", skill_display, name_ok, name_detail))

        if not isinstance(description, str) or not description.strip():
            desc_ok = False
            desc_detail = "description must be a nonempty string"
        elif len(description) > 1024:
            desc_ok = False
            desc_detail = f"description length {len(description)} exceeds 1024"
        else:
            desc_ok = True
            desc_detail = "description is nonempty and ≤1024 characters"
        checks.append(
            Check(f"skill-description-{child.name}", skill_display, desc_ok, desc_detail)
        )

    return checks


def check_package_boundary(ctx: Ctx) -> list[Check]:
    root = ctx.plugin_root.resolve()
    checks: list[Check] = []
    for path in sorted(ctx.plugin_root.rglob("*")):
        if not path.is_symlink():
            continue
        display = display_path(path, ctx.plugin_root)
        try:
            target = path.resolve()
        except OSError as exc:
            checks.append(
                Check(
                    f"symlink-{path.relative_to(ctx.plugin_root)}",
                    display,
                    False,
                    f"unresolvable symlink: {exc}",
                )
            )
            continue
        try:
            target.relative_to(root)
            ok = True
            detail = "symlink stays in package"
        except ValueError:
            ok = False
            detail = f"symlink escapes plugin root → {target}"
        checks.append(
            Check(f"symlink-{path.relative_to(ctx.plugin_root)}", display, ok, detail)
        )

    if not checks:
        checks.append(
            Check(
                "package-boundary",
                display_path(ctx.plugin_root, ctx.plugin_root),
                True,
                "no escaping symlinks",
            )
        )
    return checks


# Public docs must not publish operator unlock/upgrade CLI runbooks.
PUBLIC_DOC_FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("enable-mcp-pilot-from-email", re.compile(r"enable-mcp-pilot-from-email")),
    ("upsert-mcp-org-access", re.compile(r"upsert-mcp-org-access")),
    ("vp-run-enable-mcp", re.compile(r"vp\s+run\s+enable-mcp")),
    ("vp-run-upsert-mcp", re.compile(r"vp\s+run\s+upsert-mcp")),
    ("stage-flag-placeholder", re.compile(r"--stage\s+<stage>")),
    ("fde-readme-heading", re.compile(r"Testing access\s*\(FDE\)")),
]


def public_markdown_paths(plugin_root: Path) -> list[Path]:
    root = repo_root()
    paths: list[Path] = []
    readme = root / "README.md"
    if readme.is_file():
        paths.append(readme)
    paths.extend(sorted(plugin_root.rglob("*.md")))
    return paths


def check_public_docs_hygiene(ctx: Ctx) -> list[Check]:
    checks: list[Check] = []
    for path in public_markdown_paths(ctx.plugin_root):
        display = display_path(path, ctx.plugin_root)
        text = path.read_text(encoding="utf-8")
        hits = [label for label, pattern in PUBLIC_DOC_FORBIDDEN_PATTERNS if pattern.search(text)]
        check_id = f"public-docs-hygiene-{path.name}"
        if hits:
            checks.append(
                Check(
                    check_id,
                    display,
                    False,
                    "forbidden public operator runbook pattern(s): " + ", ".join(hits),
                )
            )
        else:
            checks.append(
                Check(check_id, display, True, "no public operator unlock/upgrade CLI runbook")
            )
    if not checks:
        checks.append(
            Check(
                "public-docs-hygiene",
                display_path(ctx.plugin_root, ctx.plugin_root),
                True,
                "no public markdown scanned",
            )
        )
    return checks


CHECKS: list[CheckFn] = [
    check_plugin_manifest,
    check_mcp,
    check_skills,
    check_package_boundary,
    check_public_docs_hygiene,
]


def run_checks(plugin_root: Path, schema_dir: Path | None) -> list[Check]:
    ctx = Ctx(
        plugin_root=plugin_root,
        plugin_schema=load_schema(PLUGIN_SCHEMA_URL, schema_dir),
        mcp_schema=load_schema(MCP_SCHEMA_URL, schema_dir),
    )
    results: list[Check] = []
    for fn in CHECKS:
        results.extend(fn(ctx))
    return results


def print_results(results: list[Check]) -> int:
    failed = 0
    for check in results:
        status = "PASS" if check.ok else "FAIL"
        if not check.ok:
            failed += 1
        print(f"{status} {check.id} ({check.path}): {check.detail}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plugin_root",
        nargs="?",
        default="plugins/siglata",
        help="Plugin root directory (default: plugins/siglata)",
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=None,
        help="Directory to read/write cached schema JSON files "
        "(default: schemas/1.0.0 when present)",
    )
    args = parser.parse_args(argv)

    plugin_root = Path(args.plugin_root)
    if not plugin_root.is_absolute():
        plugin_root = repo_root() / plugin_root
    if not plugin_root.exists():
        print(f"FAIL plugin-root ({plugin_root}): path does not exist", file=sys.stderr)
        return 1

    schema_dir = args.schema_dir
    if schema_dir is None:
        default_dir = repo_root() / "schemas" / "1.0.0"
        if (default_dir / "plugin.schema.json").is_file():
            schema_dir = default_dir

    return print_results(run_checks(plugin_root, schema_dir))


if __name__ == "__main__":
    sys.exit(main())
