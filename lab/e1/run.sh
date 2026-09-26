#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
E1_PYTHON="${E1_PYTHON:-./.venv/bin/python}"
exec "$E1_PYTHON" server.py "$@"
