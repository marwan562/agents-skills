#!/usr/bin/env python3
"""Skill Validator for agents-skills.

Validates that all skills under `skills/` conform to repository standards
and the Agent Skills specification:
1. Frontmatter starts on line 1 with `---`
2. Valid YAML frontmatter containing `name` and `description`
3. `name` matches directory name and conforms to kebab-case regex
4. `description` length is strictly between 20 and 300 characters
5. Required standard Markdown sections are present
6. Relative links within markdown reference existing local files
"""

import re
import sys
import pathlib
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

NAME_REGEX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_SECTIONS = [
    "Purpose",
    "When to Use",
    "Workflow",
    "Constraints",
    "Examples",
]

LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FENCE_REGEX = re.compile(r"```.*?```", re.DOTALL)


def strip_fences(text: str) -> str:
    """Remove fenced code blocks so section/link checks ignore examples."""
    return FENCE_REGEX.sub("", text)


def validate_skill(skill_file: pathlib.Path) -> tuple[list[str], list[str]]:
    """Validate a single SKILL.md file. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = skill_file.parent
    dir_name = skill_dir.name

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read file: {e}"], []

    # 1. Frontmatter delimiters
    if not content.startswith("---"):
        errors.append("File does not start with '---' on line 1")
        return errors, warnings

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid frontmatter delimiters; expected matching '---'")
        return errors, warnings

    yaml_text = parts[1]
    body_text = parts[2]

    # 2. YAML parsing
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing error in frontmatter: {e}")
        return errors, warnings

    if not isinstance(data, dict):
        errors.append("Frontmatter is not a YAML mapping")
        return errors, warnings

    # 3. Name check
    name = data.get("name")
    if not name:
        errors.append("Frontmatter missing required 'name' field")
    elif not isinstance(name, str):
        errors.append("'name' field must be a string")
    else:
        if not NAME_REGEX.match(name):
            errors.append(f"'name' '{name}' does not match kebab-case regex ^[a-z0-9]+(-[a-z0-9]+)*$")
        if name != dir_name:
            errors.append(f"'name' '{name}' does not match directory name '{dir_name}'")

    # 4. Description check
    desc = data.get("description")
    if not desc:
        errors.append("Frontmatter missing required 'description' field")
    elif not isinstance(desc, str):
        errors.append("'description' field must be a string")
    else:
        desc_len = len(desc.strip())
        if desc_len < 20 or desc_len > 300:
            errors.append(
                f"'description' length ({desc_len} chars) outside required range 20-300 characters"
            )
        if not (desc.strip().startswith("Use when") or desc.strip().startswith("Use this skill") or desc.strip()[0].isupper()):
            warnings.append("'description' should start with an action verb or 'Use when...'/'Use this skill...'")

    # 5. Required sections (ignore fenced examples that mention headings)
    searchable = strip_fences(body_text)
    for section in REQUIRED_SECTIONS:
        section_heading = f"## {section}"
        if section_heading not in searchable:
            errors.append(f"Missing required section heading: '{section_heading}'")

    # 6. Check internal relative links (ignore fenced examples)
    for match in LINK_REGEX.finditer(searchable):
        target = match.group(2).strip()
        # Skip web URLs, mailto, and anchor-only links
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue

        # Strip anchor if present
        clean_target = target.split("#")[0]
        if not clean_target:
            continue

        try:
            resolved_target = (skill_dir / clean_target).resolve()
            # Reject escapes outside repo root (e.g. ../../etc/passwd)
            resolved_target.relative_to(REPO_ROOT.resolve())
        except (ValueError, RuntimeError, OSError):
            errors.append(f"Relative link escapes repo root: [{match.group(1)}]({target})")
            continue
        if not resolved_target.exists():
            errors.append(f"Broken relative link: [{match.group(1)}]({target}) -> file not found")

    return errors, warnings


def main() -> int:
    print("=" * 60)
    print(" agents-skills Repository Validator")
    print("=" * 60)

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: No skills found under skills/*/SKILL.md")
        return 1

    total_errors = 0
    total_warnings = 0

    for skill_file in skill_files:
        skill_name = skill_file.parent.name
        errors, warnings = validate_skill(skill_file)

        status = "✓ PASS"
        if errors:
            status = "✗ FAIL"
        elif warnings:
            status = "⚠ WARN"

        print(f"\n[{status}] {skill_name} ({skill_file.relative_to(REPO_ROOT)})")

        for err in errors:
            print(f"    - ERROR: {err}")
            total_errors += 1

        for warn in warnings:
            print(f"    - WARNING: {warn}")
            total_warnings += 1

    print("\n" + "=" * 60)
    print(f"Summary: {len(skill_files)} skills checked. {total_errors} error(s), {total_warnings} warning(s).")
    print("=" * 60)

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
