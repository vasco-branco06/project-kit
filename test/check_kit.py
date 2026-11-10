"""Placeholder test for project-kit. Standard library only.

Usage:
  python -I test/check_kit.py FOLDER     check one generated folder
  python -I test/check_kit.py --self-test  build one sample folder per type and check it,
                                           then confirm the bad fixture fails
Exit code 0 = pass, 1 = failures, 2 = usage error.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = ("research", "academic", "code", "general")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
STANDARDS = {"code": "code-standards.md"}


def read_order(entry):
    """Paths listed under the 'Read order' heading, one backticked path per line."""
    out, on = [], False
    for line in entry.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            on = line.strip().lower() == "## read order"
            continue
        m = re.match(r"\s*\d+\.\s+`([^`]+)`", line)
        if on and m:
            out.append(m.group(1))
    return out


def check_folder(folder):
    folder, errors = Path(folder), []
    entry = folder / "CLAUDE.md"
    if not entry.is_file():
        return ["missing entry file CLAUDE.md"]
    order = read_order(entry)
    if not order:
        errors.append("entry file has no read order")
    errors += [f"read order file missing: {p}" for p in order if not (folder / p).is_file()]
    for f in folder.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".txt", ".json", ""} and ".git" not in f.parts:
            for m in PLACEHOLDER.findall(f.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"unfilled placeholder {m} in {f.relative_to(folder)}")
    return errors


def build_sample(kind, dest):
    t = ROOT / "templates"
    for layer in ("core", kind):
        if (t / layer).is_dir():
            shutil.copytree(t / layer, dest, dirs_exist_ok=True)
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
            errs = check_folder(dest)
            print(f"{kind}: {'PASS' if not errs else 'FAIL ' + '; '.join(errs)}")
            failed += bool(errs)
    bad = check_folder(ROOT / "test" / "fixtures" / "bad_unfilled")
    print(f"bad fixture: {'FAILS as expected' if bad else 'UNEXPECTEDLY PASSES'}")
    return 1 if failed or not bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    errs = check_folder(sys.argv[1])
    print("\n".join(errs) or "PASS")
    sys.exit(1 if errs else 0)
