#!/bin/bash
set -euo pipefail  # Exit on any error, undefined variables, or pipe failures

echo "🚀 === BANKER WINGMAN API STARTUP ==="
echo "Current working directory: $(pwd)"
echo "Current user: $(whoami)"
echo "Python version: $(python3 --version)"
echo ""

echo "📍 Environment Variables:"
echo "PORT: ${PORT:-'not set'}"
echo "PYTHONPATH: ${PYTHONPATH:-'not set'}"
echo ""

echo "📁 File Structure Check:"
echo "Contents of /app:"
ls -la /app/
echo ""
echo "Contents of /app/api/:"
ls -la /app/api/
echo ""

# Set Python path for imports
export PYTHONPATH="/app:${PYTHONPATH:-}"
echo "🐍 Updated PYTHONPATH: $PYTHONPATH"

# App Runner uses port 8080 by default
APP_PORT=8080
echo "🔧 Using port: $APP_PORT (App Runner standard)"

cd /app

echo "🧪 Testing Python import before startup..."
python3 -c "
import sys
print('✅ Python sys.path:', sys.path)
try:
    import api.simple_app
    print('✅ Simple app import successful')
except Exception as e:
    print('❌ Simple app import failed:', e)
try:
    import api.app
    print('✅ Full app import successful')
except Exception as e:
    print('❌ Full app import failed:', e)
    print('🔄 Falling back to simple app...')
"

echo ""
echo "🚀 Starting uvicorn server..."
echo "Command: python3 -m uvicorn api.simple_app:app --host 0.0.0.0 --port $APP_PORT"

# Start with simple app first to test
exec python3 -m uvicorn api.simple_app:app --host 0.0.0.0 --port $APP_PORT 