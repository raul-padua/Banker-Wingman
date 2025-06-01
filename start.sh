#!/bin/bash
echo "🚀 Starting Banker Wingman API..."
echo "Working directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Port from environment: $PORT"
echo "Files in /app/api/:"
ls -la /app/api/

# Set Python path and determine port
export PYTHONPATH="/app:$PYTHONPATH"
cd /app

# Use App Runner's PORT environment variable, fallback to 8000
APP_PORT=${PORT:-8000}
echo "🔧 Starting uvicorn on port $APP_PORT..."
exec python3 -m uvicorn api.app:app --host 0.0.0.0 --port $APP_PORT 