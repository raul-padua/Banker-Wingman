#!/usr/bin/env python3
"""
Direct Python execution for App Runner
"""
import sys
import os
from datetime import datetime

print("=== APP RUNNER DIRECT EXECUTION ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Environment PORT: {os.getenv('PORT', 'not set')}")

try:
    from fastapi import FastAPI
    print("✅ FastAPI import successful")
    
    import uvicorn
    print("✅ Uvicorn import successful")
    
    # Create app
    app = FastAPI(title="Direct App Runner Test")
    
    @app.get("/")
    def root():
        return {
            "status": "RUNNING",
            "message": "Direct Python execution successful!",
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version
        }
    
    @app.get("/health")
    def health():
        return {"status": "healthy", "method": "direct_python"}
    
    print("✅ FastAPI app created")
    
    # Start server
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting server on port {port}...")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 