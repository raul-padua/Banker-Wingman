#!/bin/bash
set -e  # Exit on any error

echo "🚀 === BANKER WINGMAN API STARTUP DIAGNOSTICS ==="
echo "Current working directory: $(pwd)"
echo "Current user: $(whoami)"
echo "Python version: $(python3 --version)"
echo "Environment variables:"
env | grep -E "(PORT|PYTHON|PATH)" | sort
echo ""

echo "📁 Checking files and permissions:"
echo "Contents of /app:"
ls -la /app/
echo ""
echo "Contents of /app/api/:"
ls -la /app/api/
echo ""
echo "start.sh permissions:"
ls -la /app/start.sh
echo ""

# Set Python path
export PYTHONPATH="/app:$PYTHONPATH"
echo "🐍 Python path set to: $PYTHONPATH"

# Test if simple app can be imported
echo "🧪 Testing simple app import..."
cd /app
python3 -c "
import sys
print('Python sys.path:', sys.path)
try:
    from api.simple_app import app as simple_app
    print('✅ Successfully imported simple FastAPI app')
except Exception as e:
    print('❌ Failed to import simple app:', e)
    import traceback
    traceback.print_exc()
"

# Test Python import of main app
echo "🧪 Testing main app import..."
python3 -c "
try:
    from api.app import app
    print('✅ Successfully imported main FastAPI app')
except Exception as e:
    print('❌ Failed to import main app:', e)
    print('Will try with simple app instead')
    import traceback
    traceback.print_exc()
"

# Determine port - App Runner uses PORT environment variable
if [ -z "$PORT" ]; then
    echo "⚠️  PORT environment variable not set, using default 8080"
    APP_PORT=8080
else
    APP_PORT=$PORT
    echo "✅ Using PORT from environment: $APP_PORT"
fi

echo "🔧 Starting uvicorn on port $APP_PORT..."

# Try to start with the main app, fall back to simple app if it fails
echo "Attempting to start main app..."
if python3 -c "from api.app import app" 2>/dev/null; then
    echo "✅ Main app imports successfully, starting main app"
    echo "Command: python3 -m uvicorn api.app:app --host 0.0.0.0 --port $APP_PORT --log-level info"
    exec python3 -m uvicorn api.app:app --host 0.0.0.0 --port $APP_PORT --log-level info
else
    echo "⚠️  Main app failed to import, starting simple test app"
    echo "Command: python3 -m uvicorn api.simple_app:app --host 0.0.0.0 --port $APP_PORT --log-level info"
    exec python3 -m uvicorn api.simple_app:app --host 0.0.0.0 --port $APP_PORT --log-level info
fi 