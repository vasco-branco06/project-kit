#!/usr/bin/env bash
# Release helper for project-kit.
# Usage: scripts/release.sh X.Y.Z "what changed and why" MODEL_NAME
# Bumps plugin.json, adds the dated CHANGELOG line, restores model lines in the agent
# templates, runs the self-test, commits and tags. It never pushes: it prints the command.
# If the self-test or any step fails, the files it edited are restored.
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "usage: $0 X.Y.Z \"message\" MODEL_NAME" >&2
  exit 2
fi
VERSION="$1"; MSG="$2"; MODEL="$3"
case "$VERSION" in
  *[!0-9.]*|""|.*|*.|*..*) echo "version must look like X.Y.Z" >&2; exit 2 ;;
esac
[ "$(printf '%s' "$VERSION" | tr -cd . | wc -c)" -eq 2 ] || { echo "version must look like X.Y.Z" >&2; exit 2; }

cd "$(dirname "$0")/.."
PY=$(command -v python3 || command -v python) || { echo "python not found" >&2; exit 1; }
TAG="v$VERSION"

git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repository" >&2; exit 1; }
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  echo "tag $TAG already exists" >&2; exit 1
fi

# Files a release may include. Anything else changed or untracked stops the release.
EXPECTED=(skills templates test scripts .github .claude-plugin
  README.md CHANGELOG.md CREDITS.md CONTRIBUTING.md SECURITY.md LICENSE .gitattributes .gitignore)
STRAY=$(git status --porcelain --untracked-files=all | cut -c4- | while IFS= read -r f; do
  f=${f#\"}; f=${f%\"}; top=${f%%/*}
  ok=0; for e in "${EXPECTED[@]}"; do [ "$top" = "$e" ] && ok=1; done
  [ "$ok" -eq 1 ] || echo "$f"
done)
if [ -n "$STRAY" ]; then
  echo "files outside the expected set; move, commit or ignore them first:" >&2
  echo "$STRAY" >&2
  exit 1
fi

# Back up what the script edits; restore it if anything fails before the commit.
BACKUP=$(mktemp -d)
EDITED=(.claude-plugin/plugin.json CHANGELOG.md templates/agents/*.md)
for f in "${EDITED[@]}"; do mkdir -p "$BACKUP/$(dirname "$f")"; cp "$f" "$BACKUP/$f"; done
COMMITTED=0
restore() {
  rc=$?
  if [ "$rc" -ne 0 ] && [ "$COMMITTED" -eq 0 ]; then
    for f in "${EDITED[@]}"; do cp "$BACKUP/$f" "$f"; done
    echo "release failed; plugin.json, CHANGELOG.md and the agent templates were restored" >&2
  fi
  rm -rf "$BACKUP"
}
trap restore EXIT

# 1. plugin.json version, CHANGELOG line (newest at the bottom, skipped if already there)
# and the model lines the write hook may have removed (evaluator opus, the others inherit).
# One Python step, so it behaves the same on Linux, macOS and Windows.
"$PY" -I - "$VERSION" "$MSG" "$MODEL" <<'PYEOF'
import datetime, glob, re, sys
version, msg, model = sys.argv[1:4]


def rw(path, fn):
    text = open(path, encoding="utf-8", newline="").read()
    new = fn(text)
    if new != text:
        open(path, "w", encoding="utf-8", newline="").write(new)


def bump(text):
    new, n = re.subn(r'("version"\s*:\s*")[^"]*(")', lambda m: m.group(1) + version + m.group(2), text, count=1)
    if n != 1:
        sys.exit("no version key in plugin.json")
    return new


def log(text):
    if f"| {version}:" in text:
        return text
    if text and not text.endswith("\n"):
        text += "\n"
    return text + f"- {datetime.date.today().isoformat()} | {model} | {version}: {msg}\n"


def model_line(path):
    want = "opus" if path.replace("\\", "/").endswith("/evaluator.md") else "inherit"

    def fn(text):
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        if not m or re.search(r"^model:", m.group(1), re.M):
            return text
        lines = m.group(1).split("\n")
        at = next((i for i, l in enumerate(lines) if l.startswith("description:")), None)
        if at is None:
            at = next((i for i, l in enumerate(lines) if l.startswith("name:")), len(lines) - 1)
        lines.insert(at + 1, f"model: {want}")
        return "---\n" + "\n".join(lines) + text[m.end() - 4:]
    return fn


rw(".claude-plugin/plugin.json", bump)
rw("CHANGELOG.md", log)
for f in sorted(glob.glob("templates/agents/*.md")):
    rw(f, model_line(f))
PYEOF

# 2. self-test (a failure restores the edited files)
"$PY" -I test/check_kit.py --self-test

# 3. commit and tag
for e in "${EXPECTED[@]}"; do [ -e "$e" ] && git add -A -- "$e"; done
git commit -q -m "$VERSION: $MSG"
COMMITTED=1
git tag -a "$TAG" -m "$VERSION: $MSG"

echo
echo "Committed and tagged $TAG as: $(git log -1 --format='%an <%ae>')"
echo "Nothing was pushed. When you approve, run:"
echo "  git push origin \"$(git branch --show-current)\" $TAG"
