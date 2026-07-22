#!/usr/bin/env bash
# Install daily-pig skill into a common agent skills directory.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/skills/daily-pig"

pick_dest() {
  if [[ -n "${DAILY_PIG_SKILL_DIR:-}" ]]; then
    echo "$DAILY_PIG_SKILL_DIR"
    return
  fi
  # Prefer existing agent skill roots; else ~/.agents/skills
  local candidates=(
    "$HOME/.agents/skills/daily-pig"
    "$HOME/.codex/skills/daily-pig"
    "$HOME/.claude/skills/daily-pig"
    "$HOME/.opencode/skills/daily-pig"
    "$HOME/.hermes/skills/leisure/daily-pig"
  )
  for c in "${candidates[@]}"; do
    parent="$(dirname "$c")"
    if [[ -d "$parent" ]]; then
      echo "$c"
      return
    fi
  done
  echo "$HOME/.agents/skills/daily-pig"
}

DEST="$(pick_dest)"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"

echo "✅ Installed to: $DEST"
echo "Try:"
echo "  python3 \"$DEST/scripts/daily_pig.py\" today --user local"
echo "Then tell your agent: 今日小猪"
echo "Override install path: DAILY_PIG_SKILL_DIR=/path/to/daily-pig bash install.sh"
