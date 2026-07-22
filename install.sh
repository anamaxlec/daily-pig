#!/usr/bin/env bash
# Install hermes-daily-pig into Hermes skills dir (default profile).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
DEST="${HERMES_HOME}/skills/leisure/daily-pig"

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -R "$ROOT/skills/daily-pig/." "$DEST/"

echo "✅ Installed to: $DEST"
echo "Try:"
echo "  python3 \"$DEST/scripts/daily_pig.py\" today --user local"
echo "In Telegram / Hermes chat, say: 今日小猪"
echo "(reload skills / new session if the agent doesn't auto-pick it yet)"
