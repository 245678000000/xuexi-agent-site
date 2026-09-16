#!/usr/bin/env bash
# Sync an unpacked Obsidian vault folder into content/, then rebuild.
# Usage: scripts/sync-from-vault.sh /path/to/学习agent
#    or: scripts/sync-from-vault.sh /path/to/vault-root  (auto-detects 学习agent/)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-}"
if [[ -z "$SRC" ]]; then
  echo "Usage: $0 /path/to/unpacked-vault-or-学习agent" >&2
  exit 1
fi
if [[ ! -d "$SRC" ]]; then
  echo "Not a directory: $SRC" >&2
  exit 1
fi
# Prefer nested 学习agent/ if present
if [[ -d "$SRC/学习agent" ]]; then
  SRC="$SRC/学习agent"
elif [[ -f "$SRC/欢迎.md" ]] || [[ -d "$SRC/00-地图" ]]; then
  : # already the content root
elif [[ -d "$SRC/content" ]] && [[ -f "$SRC/content/欢迎.md" ]]; then
  SRC="$SRC/content"
fi
echo "Syncing from: $SRC"
rm -rf "$ROOT/content"
mkdir -p "$ROOT/content"
# Copy, skip AppleDouble / DS_Store
( cd "$SRC" && tar cf - --exclude='._*' --exclude='.DS_Store' --exclude='.obsidian' --exclude='.trash' . ) \
  | tar xf - -C "$ROOT/content"
echo "Content files: $(find "$ROOT/content" -name '*.md' | wc -l)"
"$ROOT/build.sh"
echo "Done. Output in $ROOT/dist"
