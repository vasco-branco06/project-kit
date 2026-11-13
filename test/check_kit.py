"""Placeholder test for project-kit. Standard library only.

Usage:
  python -I test/check_kit.py FOLDER       check one generated folder
  python -I test/check_kit.py --self-test  build one sample folder per type and check it,
                                           then confirm the bad fixtures fail
Exit code 0 = pass, 1 = failures, 2 = usage error.

Checks: the entry file has a read order and every file in it exists; no placeholder
in double braces is left (dependency, hidden and work/tests folders are skipped); every agent file has name, description and model; .claude/agents exists and holds reviewer, evaluator and researcher.
Plugin check (--self-test): plugin.json and marketplace.json parse and have their keys,
every SKILL.md has frontmatter with name == folder name and a description, and every
templates/ path a skill mentions exists.
Project checks (--self-test, run last, each with a bad fixture under test/fixtures): placeholder
filler map, version alignment, changelog scenario record, vocabulary, bare templates/ paths,
agent schema, mandatory agent set. `--strict FOLDER` also flags "n/a until" in a generated folder.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "test" / "fixtures"
TYPES = ("research", "academic", "code", "general")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
STANDARDS = {"code": "code-standards.md"}
MARKER = "<!-- read-order -->"
SKIP_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".worktrees", ".git"}
AGENT_KEYS = ("name", "description", "model")

FILLERS = {}
for _skill, _names in {
    "new-project": "DATE MODEL_NAME PROJECT_NAME PROJECT_TYPE WORK_LANGUAGE CITATION_STYLE STYLE_GUIDE "
    "STANDARDS_FILE DECIDED_BY GOAL DONE_CHECKS SCOPE_IN SCOPE_OUT OWNER_RULES OWNER_TESTS PAGE_LIMIT "
    "TEACHER_GUIDE CURRENT_PHASE NEXT_STEPS FIRST_DECISION_TITLE DECISION_CONTEXT DECISION_OPTIONS "
    "DECISION_TAKEN DECISION_TRADEOFFS DECISION_SOURCES DECISION_EVIDENCE DECISION_REJECTED "
    "DECISION_INVALIDATION DECISION_REVERSIBILITY "
    "COMPONENTS_AND_ICONS LOOK_AND_TONE SPACING_AND_RADIUS TOKEN_NAME TOKEN_USE TOKEN_LIGHT TOKEN_DARK "
    "TYPOGRAPHY LAYOUT_PATTERNS",
    "run": "FRAMEWORK FRAMEWORK_REASON FRAMEWORK_VERSION HOSTING HOSTING_REASON HOSTING_VERSION LANGUAGE "
    "LANGUAGE_REASON LANGUAGE_VERSION LINTER LINTER_REASON LINTER_VERSION PACKAGE_MANAGER PACKAGE_REASON "
    "PACKAGE_VERSION TEST_TOOL TEST_REASON TEST_VERSION TEST_COMMAND BUILD_COMMAND CHECK_COMMAND "
    "LINT_COMMAND TYPES_COMMAND START_COMMAND STOP_COMMAND READY_SIGNAL ISOLATION INVARIANTS COMPONENTS "
    "DATA_FLOW CONSTRAINTS FIRST_UNIT_ID FIRST_UNIT_NAME FIRST_UNIT_DEPENDS "
    "FIRST_UNIT_CHECK UNIT_ID UNIT_NAME UNIT_GOAL UNIT_DESIGN UNIT_IMPLEMENTATION UNIT_DEPENDENCIES "
    "UNIT_VERIFY",
}.items():
    FILLERS.update({n: _skill for n in _names.split()})  # placeholder -> skill whose step fills it
MODEL_WORDS = re.compile(r"\b(haiku|sonnet|opus|fable)\b", re.I)
BLIND_WORDS = re.compile(r"\b(tests?|evals?|rubrics?|scores?|checklists?)\b", re.I)
BLIND_FILES = {"templates/agents/builder.md", "templates/agents/tester.md"}  # the builder and the visitor never see the evaluator's vocabulary
TOOLS_REQUIRED = {"reviewer", "researcher"}
VALID_MODELS = {"inherit", "opus", "sonnet", "haiku", "fable"}
MODEL_ID = re.compile(r"claude-[a-z0-9][a-z0-9.-]*")
CONSTANT_FILLERS = {"STANDARDS_FILE"}  # filled by a constant in new-project, not by a described step
BARE_TEMPLATES = re.compile(r"(?<!\$\{CLAUDE_PLUGIN_ROOT\}/)(?<![A-Za-z0-9_./-])templates/[A-Za-z0-9_./-]+")
RELEASE = re.compile(r"\|\s*(\d+\.\d+\.\d+):")  # the release field release.sh writes; Unreleased lines have none


def mandatory_names(root):
    """File names of the mandatory agents, read from the one place the kit names them: 'always the A, B and C, not counted' in templates/core/CLAUDE.md."""
    try:
        text = (Path(root) / "templates" / "core" / "CLAUDE.md").read_text(encoding="utf-8")
    except OSError:
        return []
    m = re.search(r"always the (.+?), not counted", text)
    return [f"{n}.md" for n in re.split(r",\s*|\s+and\s+", m.group(1))] if m else []


SETUP_AGENTS = tuple(mandatory_names(ROOT))


def read_order(entry):
    """Numbered backticked paths after the read-order marker (any language).

    Falls back to an English 'Read order' heading for folders made with version 0.1.
    """
    out, on = [], False
    for line in entry.read_text(encoding="utf-8-sig").splitlines():
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


def agent_errors(path, full=False):
    """Frontmatter keys; with full=True also the schema: name == file stem, valid model, tools, Status:."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return [f"agent {path.name} is not UTF-8 text"]
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return [f"agent without frontmatter: {path.name}"]
    fm = {k.strip(): v.strip() for k, _, v in (l.partition(":") for l in m.group(1).splitlines()) if _}
    errors = [f"agent {path.name} lacks {k}" for k in AGENT_KEYS if not fm.get(k)]
    if full:
        if fm.get("name") and fm["name"] != path.stem:
            errors.append(f"agent {path.name}: name {fm['name']!r} != file name")
        if fm.get("model") and fm["model"] not in VALID_MODELS and not MODEL_ID.fullmatch(fm["model"]):
            errors.append(f"agent {path.name}: model {fm['model']!r} not in {sorted(VALID_MODELS)}")
        if path.stem in TOOLS_REQUIRED and "tools" not in fm:
            errors.append(f"agent {path.name} lacks tools")
        report = re.split(r"^#*\s*report\b.*$", text[m.end():], maxsplit=1, flags=re.I | re.M)
        if len(report) < 2 or "Status:" not in report[1]:
            errors.append(f"agent {path.name}: report section lacks Status:")
    return errors


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


def mentions(text, rel):
    """True if text names the template file (path relative to its layer, or its file name) or a parent folder below the top."""
    parts = Path(rel).parts
    names = {rel, parts[-1]} | {"/".join(parts[:i]) + "/" for i in range(2, len(parts))}
    return any(n in text for n in names)


def placeholder_errors(root, fillers=FILLERS):
    """Every {{X}} in templates/ has a filler skill that exists and names X or the template file holding it."""
    root, errors, texts, unnamed = Path(root), [], {}, {}
    for f in sorted((root / "templates").rglob("*")):
        if f.is_file() and f.suffix in {".md", ".txt", ".json", ""}:
            rel = f.relative_to(root / "templates").as_posix()
            layer_rel = rel.split("/", 1)[1] if "/" in rel else rel
            for m in sorted(set(PLACEHOLDER.findall(f.read_text(encoding="utf-8", errors="ignore")))):
                name, skill = m[2:-2], fillers.get(m[2:-2])
                if skill is None:
                    errors.append(f"placeholder {m} in templates/{rel} has no filler")
                    continue
                if name in CONSTANT_FILLERS or not (root / "skills").is_dir():
                    continue
                path = root / "skills" / skill / "SKILL.md"
                if skill not in texts:
                    texts[skill] = path.read_text(encoding="utf-8") if path.is_file() else None
                if texts[skill] is None:
                    errors.append(f"placeholder {m}: filler skill {skill} not found")
                elif name not in texts[skill] and not mentions(texts[skill], layer_rel):
                    unnamed.setdefault((f"templates/{rel}", skill), []).append(m)
    errors += [f"{len(v)} placeholders in {k[0]} neither named nor is the file mentioned in skill {k[1]}: {' '.join(v)}"
               for k, v in sorted(unnamed.items())]
    return errors


def version_errors(root):
    """Version of the last CHANGELOG release line ('| X.Y.Z:', Unreleased lines skipped) == plugin.json (== marketplace.json if given)."""
    root, errors = Path(root), []
    try:
        lines = (root / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
        changelog = [m.group(1) for m in map(RELEASE.search, lines) if m][-1]
        plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    except (OSError, ValueError, KeyError, IndexError) as e:
        return [f"version check: {type(e).__name__} {e}"]
    if changelog != plugin:
        errors.append(f"CHANGELOG last version {changelog} != plugin.json {plugin}")
    try:
        market = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return errors
    for v in [market.get("version")] + [p.get("version") for p in market.get("plugins") or []]:
        if v and v != plugin:
            errors.append(f"marketplace.json version {v} != plugin.json {plugin}")
    return errors


def changelog_errors(root):
    """The CHANGELOG release line of the current version says scenarios were run or passed on an ISO date, not 'not run'."""
    root = Path(root)
    try:
        plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
        lines = (root / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError, KeyError) as e:
        return [f"changelog check: {type(e).__name__} {e}"]
    release = re.compile(rf"\|\s*{re.escape(plugin)}:")
    for l in lines:
        if (release.search(l) and re.search(r"scenarios?\b", l, re.I)
                and re.search(r"\b(run|passed|pass) on \d{4}-\d{2}-\d{2}\b", l, re.I)
                and not re.search(r"\bnot (yet )?run\b", l, re.I)):
            return []
    return [f"CHANGELOG has no release line for {plugin} saying scenarios were run or passed on an ISO date (and not 'not run')"]


def vocabulary_errors(root):
    """Model names only in skills/run/SKILL.md and the evaluator template's frontmatter; scanned: skills/ and templates/ *.md and
    test/scenarios.md (README, CONTRIBUTING and scripts are not). Blinding words flagged in builder.md and tester.md."""
    root, errors = Path(root), []
    for f in sorted(list((root / "skills").rglob("*.md")) + list((root / "templates").rglob("*.md"))):
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8", errors="ignore")
        if rel == "skills/run/SKILL.md":
            continue
        if rel == "templates/agents/evaluator.md":
            text = text.replace("\r\n", "\n").split("\n---", 1)[-1]
        for m in sorted(set(w.lower() for w in MODEL_WORDS.findall(text))):
            errors.append(f"model name {m!r} outside the allowed places: {rel}")
        if rel in BLIND_FILES:
            for w in sorted(set(w.lower() for w in BLIND_WORDS.findall(text))):
                errors.append(f"blinding word {w!r} in {rel}")
    scen = root / "test" / "scenarios.md"
    if scen.is_file():
        for part in re.split(r"(?m)^## (?=\d+\. )", scen.read_text(encoding="utf-8")):
            for m in sorted(set(w.lower() for w in MODEL_WORDS.findall(part))):
                errors.append(f"model name {m!r} outside the allowed places: test/scenarios.md {part.splitlines()[0][:30]!r}")
    return errors


def bare_path_errors(root):
    """A skill must write ${CLAUDE_PLUGIN_ROOT}/templates/..., never a bare templates/ path."""
    root, errors = Path(root), []
    for s in sorted((root / "skills").glob("*/SKILL.md")):
        for ref in sorted(set(BARE_TEMPLATES.findall(s.read_text(encoding="utf-8")))):
            errors.append(f"skill {s.parent.name}: bare path {ref}")
    return errors


def mandatory_errors(root=ROOT):
    """The mandatory agents named in templates/core/CLAUDE.md exist as templates."""
    names = mandatory_names(root)
    errors = [] if names else ["templates/core/CLAUDE.md names no mandatory agents"]
    errors += [f"template missing for mandatory agent {a}" for a in names
               if not (Path(root) / "templates" / "agents" / a).is_file()]
    return errors


def check_folder(folder, strict=False):
    folder, errors = Path(folder), []
    entry = folder / "CLAUDE.md"
    if not entry.is_file():
        return ["missing entry file CLAUDE.md"]
    try:
        order = read_order(entry)
    except UnicodeDecodeError:
        return ["entry file CLAUDE.md is not UTF-8 text"]
    if not order:
        errors.append("entry file has no read order")
    errors += [f"read order file missing: {p}" for p in order if not (folder / p).is_file()]
    agents = folder / ".claude" / "agents"
    if not agents.is_dir():
        errors.append(f"missing folder .claude/agents with the mandatory agents: {', '.join(SETUP_AGENTS)}")
    else:
        errors += [f"mandatory agent missing: {a}" for a in SETUP_AGENTS if not (agents / a).is_file()]
        known = {p.name for p in (ROOT / "templates" / "agents").glob("*.md")}
        for a in sorted(agents.glob("*.md")):
            errors += agent_errors(a, full=a.name in known)
    for f in folder.rglob("*"):
        rel = f.relative_to(folder)
        if SKIP_DIRS & set(rel.parts) or rel.parts[:2] == ("work", "tests") or rel.parts[0] == "inputs":
            continue
        if any(p.startswith(".") and p != ".claude" for p in rel.parts[:-1]):
            continue
        if f.is_file() and f.suffix in {".md", ".txt", ".json", ""} and not f.name.startswith("_"):
            for m in PLACEHOLDER.findall(f.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"unfilled placeholder {m} in {f.relative_to(folder)}")
            if strict and "n/a until" in f.read_text(encoding="utf-8", errors="ignore"):
                errors.append(f"strict: 'n/a until' left in {f.relative_to(folder)}")
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


def expect(name, errs, text):
    """A bad fixture must fail with exactly one error, and that error must contain text."""
    ok = len(errs) == 1 and text in errs[0]
    print(f"{name}: {'FAILS as expected' if ok else 'WRONG, got ' + (repr(errs) if errs else 'no error')}")
    return not ok


def fixture_errors(name, strict=False, agents=True):
    """check_folder on a copy of a fixture folder, with the mandatory agents added so the fixture holds one defect."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / name
        shutil.copytree(FIXTURES / name, dest)
        if agents:
            (dest / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
        for a in SETUP_AGENTS if agents else ():
            if not (dest / ".claude" / "agents" / a).exists():
                shutil.copy(ROOT / "templates" / "agents" / a, dest / ".claude" / "agents" / a)
        return check_folder(dest, strict=strict)


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
    for fixture, text in (("bad_plugin_json", "plugin.json lacks description"),
                          ("bad_marketplace_entry", "marketplace plugin lacks source"),
                          ("bad_marketplace_name", "marketplace plugin other != plugin.json name k"),
                          ("bad_skill_name", "skill x: name 'other' != folder"),
                          ("bad_skill_desc", "skill x lacks description"),
                          ("bad_skill_ref", "skill x references missing templates/missing/file.md")):
        failed += expect(fixture, plugin_errors(FIXTURES / fixture), text)
    for fixture, text in (("bad_unfilled", "unfilled placeholder {{OWNER_NAME}}"),
                          ("bad_readorder", "read order file missing: context/missing-file.md"),
                          ("bad_agent", "agent builder.md lacks model")):
        failed += expect(fixture, fixture_errors(fixture), text)
    failed += expect("bad_utf16", fixture_errors("bad_utf16"), "entry file CLAUDE.md is not UTF-8 text")
    failed += expect("bad_utf16_agent", agent_errors(FIXTURES / "bad_utf16_agent" / "builder.md", full=True),
                     "agent builder.md is not UTF-8 text")
    ok = agent_errors(FIXTURES / "ok_bom" / "builder.md", full=True)
    print(f"ok_bom (UTF-8 BOM agent): {'PASS' if not ok else 'FAIL ' + '; '.join(ok)}")
    failed += bool(ok)
    failed += expect("bad_noagents", fixture_errors("bad_noagents", agents=False), "missing folder .claude/agents")
    for script in ("freeze_tests.py", "merge_sources.py"):
        r = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / script), "--self-test"],
                           capture_output=True, text=True)
        print(f"{script} self-test: {'PASS' if r.returncode == 0 else 'FAIL ' + (r.stderr or r.stdout).strip()[-200:]}")
        failed += r.returncode != 0
    failed += project_checks()
    return 1 if failed else 0


def project_checks():
    """New checks, run last: each runs on the plugin (must pass) and on a bad fixture (must fail)."""
    fx, failed = FIXTURES, 0

    def report(name, errs, bad, text):
        nonlocal failed
        print(f"{name}: {'PASS' if not errs else 'FAIL ' + '; '.join(errs)}")
        failed += bool(errs) + expect(f"{name} bad fixture", bad, text)

    report("placeholder fillers", placeholder_errors(ROOT), placeholder_errors(fx / "bad_placeholder"),
           "placeholder {{NOT_A_REAL_FILLER}} in templates/core/CLAUDE.md has no filler")
    report("placeholder named in skill", [], placeholder_errors(fx / "bad_filler"),
           "1 placeholders in templates/core/CLAUDE.md neither named")
    report("version", version_errors(ROOT), version_errors(fx / "bad_version"),
           "CHANGELOG last version 0.2.0 != plugin.json 0.1.0")
    ok = version_errors(fx / "ok_unreleased")
    print(f"version, Unreleased line with a dotted number: {'PASS' if not ok else 'FAIL ' + '; '.join(ok)}")
    failed += bool(ok)
    failed += expect("marketplace version bad fixture", version_errors(fx / "bad_market_version"),
                     "marketplace.json version 0.3.0 != plugin.json 0.1.0")
    report("changelog scenarios", changelog_errors(ROOT), changelog_errors(fx / "bad_changelog"),
           "CHANGELOG has no release line for 0.2.0")
    for fixture in ("bad_changelog_date", "bad_changelog_notrun", "bad_changelog_version"):
        failed += expect(fixture, changelog_errors(fx / fixture), "CHANGELOG has no release line for 0.2.0")
    report("vocabulary", vocabulary_errors(ROOT), vocabulary_errors(fx / "bad_vocab"),
           "model name 'sonnet' outside the allowed places: skills/x/SKILL.md")
    for fixture, text in (("bad_blind", "blinding word 'rubric' in templates/agents/builder.md"),
                          ("bad_blind_tester", "blinding word 'checklists' in templates/agents/tester.md"),
                          ("bad_vocab_scenario", "model name 'haiku' outside the allowed places: test/scenarios.md"),
                          ("bad_vocab_evaluator", "model name 'opus' outside the allowed places: templates/agents/evaluator.md")):
        failed += expect(fixture, vocabulary_errors(fx / fixture), text)
    report("bare templates path", bare_path_errors(ROOT), bare_path_errors(fx / "bad_barepath"),
           "skill x: bare path templates/core/CLAUDE.md")
    schema = [e for a in sorted((ROOT / "templates" / "agents").glob("*.md")) for e in agent_errors(a, full=True)]
    report("agent schema", schema, agent_errors(fx / "bad_schema" / "builder.md", full=True),
           "agent builder.md: name 'wrongname' != file name")
    for fixture, text in (("bad_empty_model", "agent builder.md lacks model"),
                          ("bad_empty_description", "agent builder.md lacks description")):
        failed += expect(fixture, agent_errors(fx / fixture / "builder.md", full=True), text)
    failed += expect("agent status bad fixture", agent_errors(fx / "bad_status" / "builder.md", full=True),
                     "agent builder.md: report section lacks Status:")
    report("mandatory agents", mandatory_errors() + ([] if SETUP_AGENTS else ["no mandatory agents"]),
           mandatory_errors(fx / "bad_mandatory"), "template missing for mandatory agent builder.md")
    report("strict", fixture_errors("bad_strict"), fixture_errors("bad_strict", strict=True),
           "strict: 'n/a until' left in")
    return failed


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    strict = sys.argv[1:2] == ["--strict"]
    args = sys.argv[2:] if strict else sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    errs = check_folder(args[0], strict=strict)
    print("\n".join(errs) or "PASS")
    sys.exit(1 if errs else 0)
