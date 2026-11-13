"""Freeze and verify the evaluator's tests. Standard library only.

Usage:
  python -I scripts/freeze_tests.py --freeze [PROJECT_ROOT]   write work/tests/HASHES.txt
  python -I scripts/freeze_tests.py --verify [PROJECT_ROOT]   exit 1 listing changed, missing or added files
  python -I scripts/freeze_tests.py --self-test
PROJECT_ROOT defaults to ".". Files are read and hashed in binary, so CRLF cannot change a hash.
HASHES.txt lines: "<sha256>  <path relative to work/tests>"; the first line is "# frozen YYYY-MM-DD".
"""
import hashlib
import re
import sys
import tempfile
from datetime import date
from pathlib import Path


LINE = re.compile(r"([0-9a-fA-F]{64})\s+\*?(\S.*)")


def hashes(tests):
    return {f.relative_to(tests).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(tests.rglob("*")) if f.is_file() and f != tests / "HASHES.txt"}


def freeze(root):
    tests = Path(root) / "work" / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    lines = [f"# frozen {date.today().isoformat()}"] + [f"{h}  {n}" for n, h in hashes(tests).items()]
    (tests / "HASHES.txt").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    return len(lines) - 1


def verify(root):
    tests = Path(root) / "work" / "tests"
    try:
        text = (tests / "HASHES.txt").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ["HASHES.txt missing: run --freeze first"]
    frozen, bad = {}, []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        m = LINE.fullmatch(line.strip())
        if m:
            frozen[m.group(2)] = m.group(1).lower()
        else:
            bad.append(f"malformed: {line.strip()[:80]}")
    now = hashes(tests)
    return (bad + [f"missing: {n}" for n in frozen if n not in now]
            + [f"changed: {n}" for n in frozen if n in now and now[n] != frozen[n]]
            + [f"added: {n}" for n in now if n not in frozen])


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp) / "work" / "tests"
        t.mkdir(parents=True)
        (t / "a.txt").write_bytes(b"one\r\n")
        (t / "b.txt").write_bytes(b"two\n")
        assert freeze(tmp) == 2 and verify(tmp) == []
        (t / "a.txt").write_bytes(b"one\n")
        assert verify(tmp) == ["changed: a.txt"]
        (t / "a.txt").write_bytes(b"one\r\n")
        (t / "b.txt").unlink()
        assert verify(tmp) == ["missing: b.txt"]
        (t / "a.txt").write_bytes(b"one\r\n")
        (t / "b.txt").write_bytes(b"two\n")
        freeze(tmp)
        with open(t / "HASHES.txt", "a", encoding="utf-8") as f:
            f.write("a.txt abc\nnot a hash line\n")
        assert verify(tmp) == ["malformed: a.txt abc", "malformed: not a hash line"]
        (t / "HASHES.txt").unlink()
        freeze(tmp)
        (t / "c.txt").write_bytes(b"three\n")
        (t / "sub").mkdir()
        (t / "sub" / "HASHES.txt").write_bytes(b"nested\n")
        assert verify(tmp) == ["added: c.txt", "added: sub/HASHES.txt"]  # files added after the freeze
        (t / "HASHES.txt").unlink()
        assert verify(tmp) == ["HASHES.txt missing: run --freeze first"]
    print("freeze_tests self-test PASS")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        self_test()
    elif a[:1] in (["--freeze"], ["--verify"]) and len(a) <= 2:
        root = a[1] if len(a) == 2 else "."
        if a[0] == "--freeze":
            print(f"frozen {freeze(root)} files in {Path(root) / 'work' / 'tests' / 'HASHES.txt'}")
        else:
            errs = verify(root)
            print("\n".join(errs) or "PASS: tests match HASHES.txt")
            sys.exit(1 if errs else 0)
    else:
        print(__doc__)
        sys.exit(2)
