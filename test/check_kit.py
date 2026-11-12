"""Placeholder test for project-kit. Standard library only.

Usage:
  python -I test/check_kit.py FOLDER       check one generated folder
  python -I test/check_kit.py --self-test  build one sample folder per type and check it,
                                           then confirm the bad fixtures fail
Exit code 0 = pass, 1 = failures, 2 = usage error.

Checks: the entry file has a read order and every file in it exists; no placeholder
in double braces is left (dependency, hidden and work/tests folders are skipped); every agent file has name, description and model; reviewer, evaluator and researcher exist when .claude/agents does.
Plugin check (--self-test): plugin.json and marketplace.json parse and have their keys,
every SKILL.md has frontmatter with name == folder name and a description, and every
templates/ path a skill mentions exists.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = ("research", "academic", "code", "general")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
STANDARDS = {"code": "code-standards.md"}
MARKER = "<!-- read-order -->"
SKIP_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".worktrees", ".git"}
AGENT_KEYS = ("name", "description", "model")
SETUP_AGENTS = ("reviewer.md", "evaluator.md", "researcher.md")


def read_order(entry):
    """Numbered backticked paths after the read-order marker (any language).

    Falls back to an English 'Read order' heading for folders made with version 0.1.
    """
    out, on = [], False
    for line in entry.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == MARKER or stripped.lower() == "## read order":
            on = True
            continue
        if on and stripped.startswith("## "):
            break
        m = re.match(r"\s*\d+\.\s+`([^`]+)`", line)
        if on and m:
            out.append(m.group(1))
    return out


def agent_errors(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
    if not m:
        return [f"agent without frontmatter: {path.name}"]
    keys = {l.split(":", 1)[0].strip() for l in m.group(1).splitlines() if ":" in l}
    return [f"agent {path.name} lacks {k}" for k in AGENT_KEYS if k not in keys]


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
    if not m:
        return None
    return {k.strip(): v.strip() for k, _, v in (l.partition(":") for l in m.group(1).splitlines()) if _}


def load_json(path, keys):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, [f"{path.name}: {e}"]
    return data, [f"{path.name} lacks {k}" for k in keys if not data.get(k)]


def plugin_errors(root):
    root, errors = Path(root), []
    meta = root / ".claude-plugin"
    plugin, errs = load_json(meta / "plugin.json", ("name", "version", "description"))
    errors += errs
    market, errs = load_json(meta / "marketplace.json", ("name", "description", "plugins"))
    errors += errs
    for entry in (market or {}).get("plugins") or []:
        errors += [f"marketplace plugin lacks {k}" for k in ("name", "source", "description") if not entry.get(k)]
        if plugin and entry.get("name") != plugin.get("name"):
            errors.append(f"marketplace plugin {entry.get('name')} != plugin.json name {plugin.get('name')}")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    for s in skills:
        text, fm = s.read_text(encoding="utf-8"), frontmatter(s.read_text(encoding="utf-8"))
        label = f"skill {s.parent.name}"
        if fm is None:
            errors.append(f"{label} has no frontmatter")
            continue
        if fm.get("name") != s.parent.name:
            errors.append(f"{label}: name {fm.get('name')!r} != folder")
        if not fm.get("description"):
            errors.append(f"{label} lacks description")
        for ref in sorted(set(re.findall(r"templates/[A-Za-z0-9_./-]+", text))):
            if not (root / ref.rstrip(".,")).exists():
                errors.append(f"{label} references missing {ref}")
    return errors


def check_folder(folder):
    folder, errors = Path(folder), []
    entry = folder / "CLAUDE.md"
    if not entry.is_file():
        return ["missing entry file CLAUDE.md"]
    order = read_order(entry)
    if not order:
        errors.append("entry file has no read order")
    errors += [f"read order file missing: {p}" for p in order if not (folder / p).is_file()]
    agents = folder / ".claude" / "agents"
    if agents.is_dir():
        errors += [f"mandatory agent missing: {a}" for a in SETUP_AGENTS if not (agents / a).is_file()]
        for a in sorted(agents.glob("*.md")):
            errors += agent_errors(a)
    for f in folder.rglob("*"):
        rel = f.relative_to(folder)
        if SKIP_DIRS & set(rel.parts) or rel.parts[:2] == ("work", "tests"):
            continue
        if any(p.startswith(".") and p != ".claude" for p in rel.parts[:-1]):
            continue
        if f.is_file() and f.suffix in {".md", ".txt", ".json", ""} and not f.name.startswith("_"):
            for m in PLACEHOLDER.findall(f.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"unfilled placeholder {m} in {f.relative_to(folder)}")
    return errors


def build_sample(kind, dest):
    t = ROOT / "templates"
    for layer in ("core", kind):
        if (t / layer).is_dir():
            shutil.copytree(t / layer, dest, dirs_exist_ok=True)
    (Path(dest) / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
    for a in SETUP_AGENTS:
        shutil.copy(t / "agents" / a, Path(dest) / ".claude" / "agents" / a)
    std = STANDARDS.get(kind, "writing-and-evidence-standards.md")
    for f in Path(dest).rglob("*"):
        if f.is_file():
            txt = f.read_text(encoding="utf-8").replace("{{STANDARDS_FILE}}", std)
            f.write_text(PLACEHOLDER.sub("sample", txt), encoding="utf-8")


def self_test():
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for kind in TYPES:
            dest = Path(tmp) / kind
            build_sample(kind, dest)
            for skipped in ("node_modules/p", "work/tests"):
                (dest / skipped).mkdir(parents=True)
                (dest / skipped / "x.md").write_text("{{SKIPPED}}\n", encoding="utf-8")
            errs = check_folder(dest)
            print(f"{kind}: {'PASS' if not errs else 'FAIL ' + '; '.join(errs)}")
            failed += bool(errs)
            if kind == "research":
                (dest / ".claude" / "agents" / "researcher.md").unlink()
                miss = check_folder(dest)
                print(f"missing mandatory agent: {'FAILS as expected' if miss else 'UNEXPECTEDLY PASSES'}")
                failed += not miss
    for a in sorted((ROOT / "templates" / "agents").glob("*.md")):
        errs = agent_errors(a)
        print(f"agent template {a.name}: {'PASS' if not errs else 'FAIL ' + '; '.join(errs)}")
        failed += bool(errs)
    errs = plugin_errors(ROOT)
    print(f"plugin: {'PASS' if not errs else 'FAIL ' + '; '.join(errs)}")
    failed += bool(errs)
    bad = plugin_errors(ROOT / "test" / "fixtures" / "bad_plugin")
    print(f"bad_plugin: {'FAILS as expected (' + str(len(bad)) + ' errors)' if bad else 'UNEXPECTEDLY PASSES'}")
    failed += not bad
    for fixture in ("bad_unfilled", "bad_agent"):
        bad = check_folder(ROOT / "test" / "fixtures" / fixture)
        print(f"{fixture}: {'FAILS as expected' if bad else 'UNEXPECTEDLY PASSES'}")
        failed += not bad
    return 1 if failed else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    errs = check_folder(sys.argv[1])
    print("\n".join(errs) or "PASS")
    sys.exit(1 if errs else 0)
