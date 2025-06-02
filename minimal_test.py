#!/usr/bin/env python3
"""
Minimal test for App Runner deployment
"""
import sys
import os
from datetime import datetime

print("=== MINIMAL PYTHON TEST ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Timestamp: {datetime.now()}")

# Test FastAPI import
try:
    from fastapi import FastAPI
    print("✅ FastAPI import successful")
    
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {
            "status": "alive",
            "message": "Minimal App Runner test successful",
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version
        }
    
    print("✅ FastAPI app created successfully")
    
    # Start uvicorn
    import uvicorn
    print("🚀 Starting uvicorn on port 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 