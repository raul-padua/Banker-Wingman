#!/bin/bash
echo "🚀 Starting Banker Wingman API..."
echo "Working directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Files in /app/api/:"
ls -la /app/api/

# Set Python path and start uvicorn
export PYTHONPATH="/app:$PYTHONPATH"
cd /app
echo "🔧 Starting uvicorn..."
exec python3 -m uvicorn api.app:app --host 0.0.0.0 --port 8000 