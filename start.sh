#!/bin/bash

echo "=== MINIMAL STARTUP TEST ==="
echo "Working directory: $(pwd)"
echo "User: $(whoami)"
echo "Date: $(date)"
echo "Python version: $(python3 --version)"

echo "=== DIRECTORY CONTENTS ==="
ls -la /app/

echo "=== PYTHON PATH TEST ==="
python3 -c "import sys; print('Python executable:', sys.executable); print('Python path:', sys.path)"

echo "=== STARTING MINIMAL FASTAPI ==="
cd /app
python3 -c "
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get('/')
def root():
    return {'status': 'alive', 'message': 'Minimal test successful'}

if __name__ == '__main__':
    print('Starting uvicorn...')
    uvicorn.run(app, host='0.0.0.0', port=8080)
" 