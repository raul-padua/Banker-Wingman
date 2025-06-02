#!/usr/bin/env python3
"""
Direct Python execution for App Runner with a minimal web server.
"""
import sys
import os
from datetime import datetime

# This should be the first thing that runs
print(f"--- PYTHON SCRIPT {__file__} STARTED ---")
print(f"Timestamp: {datetime.now().isoformat()}")
sys.stdout.flush() # Explicit flush

try:
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PYTHONPATH: {os.getenv('PYTHONPATH', 'not set')}")
    print(f"PORT (from env): {os.getenv('PORT', 'not set by App Runner')}") # App Runner sets PORT
    print(f"PYTHONUNBUFFERED: {os.getenv('PYTHONUNBUFFERED', 'not set')}")
    sys.stdout.flush()

    print("Attempting to import FastAPI and Uvicorn...")
    from fastapi import FastAPI
    import uvicorn
    print("✅ FastAPI and Uvicorn imported successfully.")
    sys.stdout.flush()

    app = FastAPI(title="Minimal App Runner Test Server")

    @app.get("/")
    def read_root():
        print("GET / requested by health checker or user")
        sys.stdout.flush()
        return {
            "status": "healthy_and_running",
            "message": "Minimal App Runner Python server is alive!",
            "timestamp": datetime.now().isoformat()
        }

    @app.get("/health") # Explicit health check endpoint
    def health_check():
        print("GET /health requested")
        sys.stdout.flush()
        return {"status": "healthy_from_/health"}

    # Use port 8080 as App Runner expects, but allow override if PORT is somehow set differently
    # App Runner typically injects PORT=8080 when no custom port is set in App Runner console.
    # If apprunner.yaml does not specify network.port, App Runner defaults to 8080 and sets the PORT env var.
    # Our apprunner.yaml does not set network.port, so PORT should be 8080.
    server_port = int(os.getenv("PORT", 8080))

    print(f"✅ FastAPI app created. Attempting to start Uvicorn on host 0.0.0.0 port {server_port}...")
    sys.stdout.flush()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=server_port,
        log_level="info" # Uvicorn's own logging
    )
    # This line below will not be reached if uvicorn starts successfully, as uvicorn.run() is blocking.
    # print("--- UVICORN EXITED (UNEXPECTED) ---") # Should not happen in normal operation

except Exception as e:
    # Ensure any catastrophic error during setup is printed
    print(f"!!!!!!!!!! PYTHON SCRIPT CRITICAL ERROR !!!!!!!!!!")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Details: {str(e)}")
    import traceback
    print("Traceback:")
    traceback.print_exc(file=sys.stdout) # Print traceback to stdout
    sys.stdout.flush()
    sys.stderr.flush() # Also flush stderr
    print(f"!!!!!!!!!! END PYTHON SCRIPT CRITICAL ERROR !!!!!!!!!!")
    sys.exit(1) # Exit with error code

# Fallback print, should not be reached if uvicorn starts and runs indefinitely
# print("--- PYTHON SCRIPT REACHED UNEXPECTED END ---")
# sys.stdout.flush() 