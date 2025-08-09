#!/usr/bin/env sh
set -e

export PYTHONPATH=/app/src
cd /app
exec uvicorn src.main:app --host 0.0.0.0 --port 8000

