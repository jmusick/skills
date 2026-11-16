#!/usr/bin/env python3
"""Check every skill against the Agent Skills format and this repo's AGENTS.md rules.

Usage (from the repo root):
  python scripts/check_skills.py

Errors (exit 1):
  - each skills/<name>/ has SKILL.md, spelled exactly, and no README.md
  - frontmatter: --- delimiters; name matches the folder, is kebab-case, and avoids the reserved
    words claude and anthropic; description present and at most 1,024 characters; compatibility
    at most 500; no < or > anywhere in the frontmatter
  - every file in a skill's scripts/, references/ and assets/ is named in its SKILL.md, and every
    such path SKILL.md names exists
  - Python scripts compile and import only the standard library
  - README's skills table and options table, and REFERENCES.md's sections, name only skills on
    disk, and the skills table lists every one
Warnings: unknown frontmatter keys, no REFERENCES.md section, SKILL.md over 500 lines or
5,000 words (the guide's limits).
Standard library only; Python 3.10+.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWN_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools",
              "disable-model-invocation", "user-invocable", "argument-hint", "model"}
BUNDLED = ("scripts", "references", "assets")
errors, warnings = [], []


def frontmatter(path, text):
    if not text.startswith("---\n"):
        errors.append(f"{path}: frontmatter must open with --- on the first line")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        errors.append(f"{path}: frontmatter has no closing ---")
        return {}
    block = text[4:end]
    if re.search(r"[<>]", block):
        errors.append(f"{path}: frontmatter contains < or >, which the format forbids")
    keys = {}
    for line in block.splitlines():
        if m := re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line):
            keys[m.group(1)] = m.group(2).strip().strip("\"'")
    return keys


def imports(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    names = set(re.findall(r"^\s*import\s+([\w.]+)", src, re.M)) | set(re.findall(r"^\s*from\s+([\w.]+)\s+import", src, re.M))
    return {n.split(".")[0] for n in names}


def check_skill(name):
    folder = os.path.join(ROOT, "skills", name)
    rel = f"skills/{name}"
    files = os.listdir(folder)
    if "SKILL.md" not in files:
        errors.append(f"{rel}: no SKILL.md (the name is case-sensitive)")
        return
    if any(f.lower() == "readme.md" for f in files):
        errors.append(f"{rel}: a skill folder holds no README.md; put docs in SKILL.md or references/")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"{rel}: folder name must be kebab-case")
    with open(os.path.join(folder, "SKILL.md"), encoding="utf-8") as fh:
        text = fh.read().replace("\r\n", "\n")
    fm = frontmatter(f"{rel}/SKILL.md", text)
    if fm:
        if fm.get("name") != name:
            errors.append(f"{rel}/SKILL.md: name '{fm.get('name')}' doesn't match the folder")
        if re.search(r"claude|anthropic", fm.get("name", "")):
            errors.append(f"{rel}/SKILL.md: name uses a reserved word (claude, anthropic)")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{rel}/SKILL.md: no description")
        elif len(desc) > 1024:
            errors.append(f"{rel}/SKILL.md: description is {len(desc)} characters; the limit is 1,024")
        if len(fm.get("compatibility", "")) > 500:
            errors.append(f"{rel}/SKILL.md: compatibility is over 500 characters")
        for key in sorted(set(fm) - KNOWN_KEYS):
            warnings.append(f"{rel}/SKILL.md: unknown frontmatter key '{key}'")
    lines, words = text.count("\n") + 1, len(text.split())
    if lines > 500 or words > 5000:
        warnings.append(f"{rel}/SKILL.md: {lines} lines, {words} words; move detail to references/")

    for sub in BUNDLED:
        base = os.path.join(folder, sub)
        for dirpath, _, names in os.walk(base):
            for f in names:
                path = os.path.relpath(os.path.join(dirpath, f), folder).replace(os.sep, "/")
                if "__pycache__" in path:
                    continue
                if path not in text:
                    errors.append(f"{rel}/{path}: SKILL.md never names it, so the agent won't know it's there")
                if f.endswith(".py"):
                    try:
                        with open(os.path.join(dirpath, f), encoding="utf-8") as fh:
                            compile(fh.read(), path, "exec")
                    except (SyntaxError, ValueError) as e:
                        errors.append(f"{rel}/{path}: doesn't compile: {e}")
                    outside = sorted(imports(os.path.join(dirpath, f)) - set(sys.stdlib_module_names) - {"__future__"})
                    if outside:
                        errors.append(f"{rel}/{path}: imports outside the standard library: {', '.join(outside)}")
    for m in re.finditer(r"\b((?:scripts|references|assets)/[\w./-]*\w\.\w+)", text):
        parts = m.group(1).split("/")
        if len(parts) > 2 and not os.path.isdir(os.path.join(folder, *parts[:2])):
            continue  # a path in the project the skill works on, like scripts/editorial/packet.mjs
        if not os.path.exists(os.path.join(folder, *parts)):
            errors.append(f"{rel}/SKILL.md: names {m.group(1)}, which doesn't exist")


def check_index(skills):
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    listed = set(re.findall(r"^\|\s*\[([\w-]+)\]\(skills/([\w-]+)/SKILL\.md\)", readme, re.M))
    for label, target in listed:
        if label != target:
            errors.append(f"README.md: skills table row '{label}' links to skills/{target}")
    in_table = {t for _, t in listed}
    for s in sorted(skills - in_table):
        errors.append(f"README.md: skills table is missing {s}")
    for s in sorted(in_table - skills):
        errors.append(f"README.md: skills table lists {s}, which isn't in skills/")
    for s in sorted({m for m in re.findall(r"^\|\s*([\w-]+)\s*\|\s*[`\"/]", readme, re.M)} - skills):
        errors.append(f"README.md: options table names {s}, which isn't in skills/")
    with open(os.path.join(ROOT, "REFERENCES.md"), encoding="utf-8") as fh:
        sections = set(re.findall(r"^## ([\w-]+)\s*$", fh.read(), re.M))
    for s in sorted(sections - skills):
        errors.append(f"REFERENCES.md: section {s} has no skill in skills/")
    for s in sorted(skills - sections):
        warnings.append(f"REFERENCES.md: no section for {s}")


def main():
    skills_dir = os.path.join(ROOT, "skills")
    skills = {d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))}
    for name in sorted(skills):
        check_skill(name)
    check_index(skills)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"Checked {len(skills)} skills: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
