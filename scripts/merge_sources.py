"""Merge work/sources-*.md rows into context/source-log.md without duplicates. Standard library only.

Usage:
  python -I scripts/merge_sources.py [PROJECT_ROOT]   (default ".")
  python -I scripts/merge_sources.py --self-test
A row is a table line starting with "|"; header, separator and "(none yet)" rows are skipped, and
the "(none yet)" row of the log is dropped once real rows are added. A row whose cell count differs from the
log header is skipped and printed to stderr. Exit 2 if the log is missing.
"""
import re
import sys
import tempfile
from pathlib import Path


def norm(line):
    return re.sub(r"\s+", " ", line.strip())


def is_separator(line):
    s = line.strip()
    return s.startswith("|") and set(s.replace("|", "")) <= set("-: ")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def width(lines):
    """Cell count of the first table header in lines, or None if there is no table."""
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            return len(cells(line))
    return None


def rows(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith("|") or is_separator(s) or "(none yet)" in s:
            continue
        if i + 1 < len(lines) and is_separator(lines[i + 1]):
            continue  # header row
        out.append(s)
    return out


def merge(root):
    root = Path(root)
    log = root / "context" / "source-log.md"
    if not log.is_file():
        raise FileNotFoundError(log)
    lines = log.read_text(encoding="utf-8").splitlines()
    seen = {norm(l) for l in lines}
    cols = width(lines)
    new = []
    for f in sorted((root / "work").glob("sources-*.md")):
        for r in rows(f):
            if cols and len(cells(r)) != cols:
                print(f"skipped {f.name}: {len(cells(r))} cells, the log has {cols}: {r[:80]}", file=sys.stderr)
            elif norm(r) not in seen:
                seen.add(norm(r))
                new.append(r)
    if new:
        lines = [l for l in lines if "(none yet)" not in l] + new
        log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(new)


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "context").mkdir()
        (root / "work").mkdir()
        head = "| Citation | Where |\n|---|---|\n"
        (root / "context" / "source-log.md").write_text("# Log\n\n" + head + "| (none yet) | |\n", encoding="utf-8")
        (root / "work" / "sources-a.md").write_text(head + "| A 2020 | url1 |\n| B 2021 | url2 |\n", encoding="utf-8")
        (root / "work" / "sources-b.md").write_text(head + "| B  2021 | url2 |\n| C 2022 | url3 |\n", encoding="utf-8")
        (root / "work" / "sources-c.md").write_text(head + "| D 2023 | url4 | extra |\n", encoding="utf-8")
        assert merge(root) == 3  # the 3-cell row is skipped
        assert merge(root) == 0
        text = (root / "context" / "source-log.md").read_text(encoding="utf-8")
        assert text.count("url2") == 1 and "(none yet)" not in text and "| C 2022 | url3 |" in text and "url4" not in text
    print("merge_sources self-test PASS")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        self_test()
    elif len(a) <= 1:
        try:
            print(f"added {merge(a[0] if a else '.')} rows")
        except FileNotFoundError as e:
            print(f"missing {e}")
            sys.exit(2)
    else:
        print(__doc__)
        sys.exit(2)
