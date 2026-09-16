#!/usr/bin/env python3
"""Prove poteto-mode is visible to a real Codex CLI via prompt-input.

Codex lists skills by name/description/path; it does not inline SKILL.md bodies
into `codex debug prompt-input`. Visibility means `/poteto-mode` appears in the
available-skills list with a resolvable `*/poteto-mode/SKILL.md` path.

Supported roots Codex actually reads:
- Project: `<repo>/.agents/skills` when cwd is the Siglata checkout
- Home: `$CODEX_HOME/skills/poteto-mode` after skill-installer install
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    raise SystemExit(1)


def ok(msg: str) -> None:
    print(f"PASS {msg}")


def skill_roots_from_prompt(text: str) -> dict[str, str]:
    return dict(re.findall(r"`(r\d+)` = `([^`]+)`", text))


def main() -> int:
    codex = shutil.which("codex")
    if not codex:
        fail("codex CLI not on PATH (install @openai/codex)")

    version = run([codex, "--version"])
    if version.returncode != 0:
        fail(f"codex --version exited {version.returncode}")
    ok(f"codex available ({version.stdout.strip() or version.stderr.strip()})")

    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    home_skill = home / "skills" / "poteto-mode" / "SKILL.md"

    project_skill: Path | None = None
    cwd_project = Path.cwd() / ".agents" / "skills" / "poteto-mode" / "SKILL.md"
    if cwd_project.is_file():
        project_skill = cwd_project
    else:
        checkout = os.environ.get("SIGLATA_CHECKOUT", "").strip()
        if checkout:
            env_project = (
                Path(checkout) / ".agents" / "skills" / "poteto-mode" / "SKILL.md"
            )
            if env_project.is_file():
                project_skill = env_project

    if not home_skill.is_file() and project_skill is None:
        fail(
            "poteto-mode not found under $CODEX_HOME/skills or "
            ".agents/skills (install via skill-installer or open the Siglata checkout)"
        )

    if home_skill.is_file():
        ok(f"home skill present ({home_skill})")
    if project_skill is not None:
        ok(f"project skill present ({project_skill})")

    # Prefer the project root when present so Codex loads `.agents/skills`.
    # Otherwise stay in cwd and rely on `$CODEX_HOME/skills`.
    if project_skill is not None:
        cwd = project_skill.parents[3]
    else:
        cwd = Path.cwd()
    prompt = run([codex, "debug", "prompt-input", "/poteto-mode"], cwd=cwd)
    if prompt.returncode != 0:
        fail(f"debug prompt-input: {prompt.stderr.strip() or prompt.stdout.strip()}")

    try:
        payload = json.loads(prompt.stdout)
    except json.JSONDecodeError as exc:
        fail(f"prompt-input was not JSON: {exc}")

    blob = json.dumps(payload)
    if "poteto-mode" not in blob:
        fail("prompt-input missing poteto-mode skill name")
    if not re.search(r"file: r\d+/poteto-mode/SKILL\.md", blob):
        fail("prompt-input missing poteto-mode SKILL.md file ref")
    if '"text": "/poteto-mode"' not in blob and "/poteto-mode" not in blob:
        fail("prompt-input missing user invoke /poteto-mode")
    ok("codex debug prompt-input lists poteto-mode for /poteto-mode")

    roots = skill_roots_from_prompt(blob)
    if not roots:
        fail("prompt-input missing skill roots table")
    ok(f"skill roots: {', '.join(f'{k}={v}' for k, v in sorted(roots.items()))}")

    body_path = home_skill if home_skill.is_file() else project_skill
    assert body_path is not None
    body = body_path.read_text(encoding="utf-8")
    for needle in (
        "Platform Adaptation",
        "Non-negotiables",
        "Writing the reply",
        "Autonomous run",
    ):
        if needle not in body:
            fail(f"{body_path} missing marker {needle!r}")
    ok(f"SKILL.md body readable at {body_path}")

    print("PASS overall (poteto-mode visible to Codex; body on disk)")
    print(
        "NOTE: Codex does not inline SKILL.md into prompt-input; "
        "the model reads the listed path. Model-driven `codex exec` still needs "
        "`codex login` / OPENAI_API_KEY."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(0)
