#!/usr/bin/env python3
"""Run the mechanical checks on agent skills. Read-only.

Finds every SKILL.md under the given paths (default: the current directory),
checks frontmatter, size, links, unreferenced files, eval prompts, and the
Codex invocation setting, collects each skill's git history, and compares
same-named files shared between skills. Prints JSON.

Usage: check_skills.py [PATH ...]
  PATH is a skill folder, a SKILL.md, or a folder to search for skills.
"""
import json
import os
import re
import subprocess
import sys

MAX_DESCRIPTION = 1024
MAX_NAME = 64
MAX_LINES = 500
LONG_REFERENCE = 100
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "evals"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIX_RE = re.compile(r"\b(fix(es|ed)?|bug|revert|regression|broken|wrong|stale)\b", re.I)
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE_PATH = re.compile(r"`((?:\.{1,2}/)?(?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|js|mjs|ts|json|yaml|yml|txt|ps1|dot|svg|png))`")
BACKSLASH_PATH = re.compile(r"\b(?:scripts|references|assets)\\[\w.\\-]+")
PERSON_RE = re.compile(r"^(i|we|you|my|our)\b", re.I)
SKILL_SUBDIRS = {"references", "scripts", "assets", "rules", "templates", "agents"}


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def git(args, cwd):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def parse_frontmatter(text):
    """Return (fields, line_of_each_field, body_start_line) or None if missing.

    Handles the subset of YAML skills use: plain, quoted, and block (> |) scalars.
    Nested maps such as metadata are kept as raw text.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    fields, where, i = {}, {}, 1
    while i < end:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value[:1] in "\"'" and value:
            close = value.find(value[0], 1)
            while value[0] == "'" and close != -1 and value[close + 1:close + 2] == "'":
                close = value.find("'", close + 2)  # '' is an escaped quote
            while value[0] == '"' and close != -1 and value[close - 1] == "\\":
                close = value.find('"', close + 1)
            if close != -1:
                value = value[:close + 1]  # drop a trailing comment after the closing quote
        else:
            value = re.sub(r"(^|\s+)#.*$", "", value).strip()
        where[key] = i + 1
        block = []
        j = i + 1
        while j < end and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
            block.append(lines[j].strip())
            j += 1
        if value in (">", ">-", ">+"):
            value = " ".join(b for b in block if b)
        elif value in ("|", "|-", "|+"):
            value = "\n".join(block).strip()
        elif not value and block:
            value = "\n".join(block).strip()
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            quote = value[0]
            value = value[1:-1]
            value = value.replace('\\"', '"') if quote == '"' else value.replace("''", "'")
        elif block:
            value = " ".join([value] + [b for b in block if b])  # plain scalar continued on indented lines
        fields[key] = value
        i = j
    return fields, where, end + 2


def is_true(value):
    return str(value).strip().lower() == "true"


def skill_files(skill_dir):
    out = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), skill_dir).replace(os.sep, "/"))
    return sorted(out)


def links_in(text):
    """Markdown links, and backticked paths that look like files (kind "code").

    Lines inside fenced code blocks are skipped: they hold examples, not links.
    """
    found = []
    in_fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in MD_LINK.finditer(line):
            found.append((n, m.group(1), "link"))
        for m in CODE_PATH.finditer(line):
            found.append((n, m.group(1), "code"))
    return found


def local_target(link):
    """Strip anchors and reject URLs; return a relative path or None."""
    if re.match(r"^[a-z]+:", link) or link.startswith(("#", "/", "~", "$", "<")):
        return None
    return link.split("#")[0] or None


def check_links(skill_dir, rel_file, text, issues, mentioned):
    base = os.path.dirname(os.path.join(skill_dir, rel_file))
    for line, link, kind in links_in(text):
        target = local_target(link)
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(base, target))
        if os.path.exists(resolved) and os.path.abspath(resolved).startswith(os.path.abspath(skill_dir) + os.sep):
            mentioned.add(os.path.relpath(resolved, skill_dir).replace(os.sep, "/"))
            continue
        if os.path.exists(os.path.join(skill_dir, target)):
            mentioned.add(target)  # written relative to the skill root, as most skills do
            continue
        # A backticked path usually names a file in the project the skill works on, so only
        # paths into the skill's own folders count as broken.
        if kind == "code" and target.split("/")[0] not in SKILL_SUBDIRS:
            continue
        if target.startswith("../"):
            issues.append(issue("warn", "link-outside-skill", f"{rel_file}:{line} points outside the skill folder ({link}); it breaks when the skill is copied on its own", rel_file, line))
        elif kind == "link":
            issues.append(issue("error", "broken-link", f"{rel_file}:{line} links to {link}, which doesn't exist", rel_file, line))
        else:
            issues.append(issue("warn", "missing-file", f"{rel_file}:{line} names {link}, which isn't in the skill folder (fine if it means a file in the user's project)", rel_file, line))


def issue(level, check, message, file=None, line=None):
    item = {"level": level, "check": check, "message": message}
    if file:
        item["file"] = file
    if line:
        item["line"] = line
    return item


def check_evals(skill_dir, name, model_invocable, issues):
    evals_dir = os.path.join(skill_dir, "evals")
    if not os.path.isdir(evals_dir):
        return 0
    cases = sorted(d for d in os.listdir(evals_dir) if os.path.isdir(os.path.join(evals_dir, d)))
    for case in cases:
        prompt_path = os.path.join(evals_dir, case, "prompt.md")
        if not os.path.isfile(prompt_path):
            issues.append(issue("warn", "eval-missing-prompt", f"evals/{case} has no prompt.md"))
            continue
        text = read(prompt_path)
        fm = parse_frontmatter(text)
        body = "\n".join(text.splitlines()[fm[2] - 1:]) if fm else text
        if not model_invocable and not body.strip().startswith(f"/{name}"):
            issues.append(issue("warn", "eval-prompt-no-slash", f"evals/{case}/prompt.md doesn't start with /{name}; the skill is manual-only, so the agent won't pick it up from plain English", f"evals/{case}/prompt.md"))
        if not os.path.isdir(os.path.join(evals_dir, case, "graders")):
            issues.append(issue("info", "eval-no-graders", f"evals/{case} has no graders/ folder"))
    return len(cases)


def git_history(skill_dir):
    log = git(["log", "--format=%h %s", "--", "."], skill_dir)
    if log is None:
        return None
    subjects = [l for l in log.splitlines() if l.strip()]
    fixes = [s for s in subjects if FIX_RE.search(s.split(" ", 1)[-1])]
    return {"commits": len(subjects), "fix_like": len(fixes), "recent": subjects[:8], "recent_fixes": fixes[:8]}


def check_skill(skill_md):
    skill_dir = os.path.dirname(os.path.abspath(skill_md))
    folder = os.path.basename(skill_dir)
    text = read(skill_md)
    lines = text.splitlines()
    issues = []
    result = {"path": skill_dir.replace(os.sep, "/"), "folder": folder, "lines": len(lines)}

    fm = parse_frontmatter(text)
    if fm is None:
        issues.append(issue("error", "frontmatter", "SKILL.md has no YAML frontmatter between --- lines", "SKILL.md", 1))
        fields, where = {}, {}
    else:
        fields, where, _ = fm

    name = fields.get("name", "")
    result["name"] = name or folder
    if not name:
        issues.append(issue("error", "name-missing", "frontmatter has no name", "SKILL.md", 1))
    else:
        if name != folder:
            issues.append(issue("error", "name-folder-mismatch", f"name '{name}' doesn't match folder '{folder}'", "SKILL.md", where.get("name")))
        if not NAME_RE.match(name) or len(name) > MAX_NAME:
            issues.append(issue("error", "name-format", f"name '{name}' must be lowercase letters, digits and single hyphens, at most {MAX_NAME} characters", "SKILL.md", where.get("name")))
        if re.search(r"anthropic|claude", name):
            issues.append(issue("warn", "name-reserved", f"name '{name}' uses a reserved word (anthropic, claude)", "SKILL.md", where.get("name")))

    desc = fields.get("description", "")
    result["description_chars"] = len(desc)
    if not desc:
        issues.append(issue("error", "description-missing", "frontmatter has no description", "SKILL.md", 1))
    else:
        if len(desc) > MAX_DESCRIPTION:
            issues.append(issue("error", "description-length", f"description is {len(desc)} characters; the limit is {MAX_DESCRIPTION}", "SKILL.md", where.get("description")))
        if re.search(r"<[A-Za-z/]", desc):
            issues.append(issue("warn", "description-xml", "description contains angle-bracket tags, which some loaders reject", "SKILL.md", where.get("description")))
        if PERSON_RE.match(desc):
            issues.append(issue("info", "description-person", "description opens in first or second person; third person reads better in a skill list", "SKILL.md", where.get("description")))

    model_invocable = not is_true(fields.get("disable-model-invocation", "false"))
    result["model_invocable"] = model_invocable
    codex = os.path.join(skill_dir, "agents", "openai.yaml")
    codex_implicit = None
    if os.path.isfile(codex):
        m = re.search(r"allow_implicit_invocation:\s*(true|false)", read(codex))
        codex_implicit = (m.group(1) == "true") if m else None
    result["codex_implicit"] = codex_implicit
    if not model_invocable and codex_implicit is not False:
        issues.append(issue("warn", "invocation-mismatch", "disable-model-invocation is true, but agents/openai.yaml doesn't set allow_implicit_invocation: false, so Codex can still fire it on its own"))
    if model_invocable and codex_implicit is False:
        issues.append(issue("warn", "invocation-mismatch", "agents/openai.yaml turns off implicit invocation, but Claude Code can still fire the skill on its own (no disable-model-invocation)"))

    if len(lines) > MAX_LINES:
        issues.append(issue("warn", "skill-length", f"SKILL.md is {len(lines)} lines; move reference material behind pointers to stay under ~{MAX_LINES}", "SKILL.md"))
    for n, line in enumerate(lines, 1):
        if BACKSLASH_PATH.search(line):
            issues.append(issue("warn", "backslash-path", f"SKILL.md:{n} uses a backslash path; use forward slashes", "SKILL.md", n))

    files = skill_files(skill_dir)
    mentioned = set()
    check_links(skill_dir, "SKILL.md", text, issues, mentioned)
    first_level = set(mentioned)
    for rel in sorted(first_level):
        if rel.endswith(".md") and rel != "SKILL.md":
            ref_text = read(os.path.join(skill_dir, rel))
            nested = set()
            check_links(skill_dir, rel, ref_text, issues, nested)
            for n in sorted(nested - first_level - {"SKILL.md"}):
                if n.endswith(".md"):
                    issues.append(issue("info", "nested-reference", f"{n} is reached only through {rel}; agents may preview a chained file partially, so link it from SKILL.md if it matters", rel))
            mentioned |= nested
            ref_lines = ref_text.count("\n") + 1
            head = "\n".join(ref_text.splitlines()[:20])
            if ref_lines > LONG_REFERENCE and not re.search(r"^[#*\s]*(table of )?contents\b", head, re.I | re.M):
                issues.append(issue("info", "reference-no-toc", f"{rel} is {ref_lines} lines with no contents list; a short list at the top lets the agent find its section", rel))
    names_mentioned = {os.path.basename(m) for m in mentioned} | {m for m in mentioned}
    for rel in files:
        top = rel.split("/")[0]
        base = os.path.basename(rel)
        if rel == "SKILL.md" or top in ("agents", "evals") or base.startswith(("test_", "conftest")) or "/" not in rel and base.upper().startswith(("LICENSE", "NOTICE", "README")):
            continue
        if rel not in names_mentioned and base not in text and base not in names_mentioned:
            issues.append(issue("info", "unreferenced-file", f"{rel} isn't mentioned by SKILL.md or the files it links, so the agent never loads it", rel))

    result["evals"] = check_evals(skill_dir, name or folder, model_invocable, issues)
    result["git"] = git_history(skill_dir)
    result["files"] = files
    result["issues"] = issues
    return result


def find_skills(paths):
    found, missing = [], []
    for p in paths:
        if not os.path.exists(p):
            missing.append(p)
            continue
        p = os.path.abspath(p)
        if os.path.isfile(p) and os.path.basename(p) == "SKILL.md":
            found.append(p)
            continue
        if os.path.isfile(os.path.join(p, "SKILL.md")):
            found.append(os.path.join(p, "SKILL.md"))
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if "SKILL.md" in files:
                found.append(os.path.join(root, "SKILL.md"))
                dirs[:] = []  # a skill's own subfolders hold no skills
    return sorted(set(found)), missing


def shared_files(results):
    """Same-named scripts and references in more than one skill, and whether they match."""
    groups = {}
    for r in results:
        for rel in r["files"]:
            if rel.split("/")[0] in ("scripts", "references") and not os.path.basename(rel).startswith("test_"):
                groups.setdefault(rel, []).append(r)
    out = []
    for rel, owners in sorted(groups.items()):
        if len(owners) < 2:
            continue
        contents = {}
        for r in owners:
            contents.setdefault(read(os.path.join(r["path"], rel)).replace("\r\n", "\n"), []).append(r["name"])
        out.append({"file": rel, "skills": [r["name"] for r in owners], "identical": len(contents) == 1,
                    "versions": list(contents.values()) if len(contents) > 1 else None})
    return out


def main():
    args = sys.argv[1:] or ["."]
    if any(a in ("-h", "--help") for a in args):
        print(__doc__)
        return 0
    skills, missing = find_skills(args)
    results = [check_skill(s) for s in skills]
    names = {}
    for r in results:
        names.setdefault(r["name"], []).append(r["path"])
    for name, paths in names.items():
        if len(paths) > 1:
            for r in results:
                if r["name"] == name:
                    r["issues"].append(issue("error", "duplicate-name", f"name '{name}' is used by {len(paths)} skills: {', '.join(paths)}"))
    shared = shared_files(results)
    counts = {"error": 0, "warn": 0, "info": 0}
    for r in results:
        for i in r["issues"]:
            counts[i["level"]] += 1
        del r["files"]
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    print(json.dumps({"skills_found": len(results), "missing_paths": missing, "counts": counts,
                      "skills": results, "shared_files": shared}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
