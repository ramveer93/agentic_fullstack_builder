#!/bin/bash
echo "Starting FastAPI backend..."

# Kill any existing process on port 8001
lsof -t -i:8001 | xargs kill -9 2>/dev/null || true


# Run uvicorn from the root directory so backend module is found
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
