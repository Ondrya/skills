#!/usr/bin/env python3
"""Validate Agent Skills in this repository."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATEGORIES = {
    "code",
    "architecture",
    "devops",
    "testing",
    "security",
    "data",
    "process",
    "product",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_LINES = 500
MAX_DESCRIPTION = 1024
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SECRET_RE = re.compile(
    r"(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str, list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, ["missing YAML frontmatter (file must start with '---')"]
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text, ["unterminated YAML frontmatter"]
    try:
        data = yaml.safe_load("\n".join(lines[1:end])) or {}
    except yaml.YAMLError as exc:
        return {}, text, [f"invalid YAML frontmatter: {exc}"]
    if not isinstance(data, dict):
        return {}, text, ["frontmatter must be a YAML mapping"]
    return data, "\n".join(lines[end + 1 :]), errors


def check_links(skill_dir: Path, body: str) -> list[str]:
    errors: list[str] = []
    for raw in LINK_RE.findall(body):
        target = raw.strip().split(" ", 1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0])
        if not target:
            continue
        if target.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:[\\/]", target):
            errors.append(f"absolute link is not portable: {raw}")
            continue
        if not (skill_dir / target).exists():
            errors.append(f"broken relative link: {raw}")
    return errors


def scan_secrets(skill_dir: Path) -> list[str]:
    warnings: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_RE.search(text):
            warnings.append(f"possible secret in {rel(path)}")
    return warnings


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.is_file():
        return [f"{rel(skill_dir)}: missing SKILL.md"], warnings

    data, body, fm_errors = read_frontmatter(skill_file)
    errors.extend(f"{rel(skill_file)}: {message}" for message in fm_errors)

    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append(f"{rel(skill_file)}: 'name' is required")
    else:
        if name != skill_dir.name:
            errors.append(
                f"{rel(skill_file)}: name '{name}' must match directory '{skill_dir.name}'"
            )
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append(
                f"{rel(skill_file)}: name '{name}' must be lowercase kebab-case, 1-64 characters"
            )

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{rel(skill_file)}: 'description' is required")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(
            f"{rel(skill_file)}: description is {len(description)} characters "
            f"(max {MAX_DESCRIPTION})"
        )

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{rel(skill_file)}: 'metadata' mapping is required")
        metadata = {}
    else:
        for key, value in metadata.items():
            if not isinstance(value, str):
                errors.append(f"{rel(skill_file)}: metadata.{key} must be a string")
        category = metadata.get("category")
        if not category:
            errors.append(f"{rel(skill_file)}: metadata.category is required")
        elif category not in CATEGORIES:
            errors.append(
                f"{rel(skill_file)}: metadata.category '{category}' is not one of "
                f"{', '.join(sorted(CATEGORIES))}"
            )
        if not metadata.get("tags", "").strip():
            errors.append(f"{rel(skill_file)}: metadata.tags is required")
        if not metadata.get("version", "").strip():
            errors.append(f"{rel(skill_file)}: metadata.version is required")

    if not data.get("license"):
        warnings.append(f"{rel(skill_file)}: missing 'license' (expected MIT)")

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > MAX_LINES:
        warnings.append(
            f"{rel(skill_file)}: {line_count} lines exceeds the recommended {MAX_LINES}"
        )

    errors.extend(f"{rel(skill_file)}: {message}" for message in check_links(skill_dir, body))
    warnings.extend(scan_secrets(skill_dir))

    if shutil.which("skills-ref"):
        result = subprocess.run(
            ["skills-ref", "validate", str(skill_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stdout + result.stderr).strip()
            errors.append(f"{rel(skill_dir)}: skills-ref validate failed\n{detail}")

    return errors, warnings


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"error: {rel(SKILLS_DIR)} does not exist")
        return 1

    skill_dirs = sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not skill_dirs:
        print("error: no skills found")
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for skill_dir in skill_dirs:
        errors, warnings = validate_skill(skill_dir)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        status = "FAIL" if errors else ("WARN" if warnings else "OK")
        print(f"[{status}] {skill_dir.name}")

    for warning in all_warnings:
        print(f"warning: {warning}")
    for error in all_errors:
        print(f"error: {error}")

    if all_errors:
        print(f"\n{len(all_errors)} error(s), {len(all_warnings)} warning(s)")
        return 1
    print(f"\n{len(skill_dirs)} skill(s) valid, {len(all_warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
