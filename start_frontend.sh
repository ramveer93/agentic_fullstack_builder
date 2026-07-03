#!/bin/bash
echo "Starting React frontend..."

# Kill any existing process on port 5173
lsof -t -i:5173 | xargs kill -9 2>/dev/null || true


cd frontend
npm run dev
