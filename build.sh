#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
  PIP=.venv/bin/pip
elif command -v python3 >/dev/null; then
  PY=python3
  PIP=pip3
else
  echo "python3 required" >&2
  exit 1
fi
if ! "$PY" -c "import markdown" 2>/dev/null; then
  "$PIP" install -r requirements.txt
fi
"$PY" build.py
