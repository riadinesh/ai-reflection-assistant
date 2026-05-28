#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
"$SCRIPT_DIR/venv/bin/python" -m app.summarize >> /tmp/reflections.log 2>> /tmp/reflections-error.log
