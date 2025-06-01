#!/usr/bin/env python3
"""
Minimal FastAPI app for testing App Runner deployment
"""
from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI(title="Test Banker Wingman API")

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Test Banker Wingman API",
        "timestamp": datetime.utcnow().isoformat(),
        "port": os.getenv("PORT", "unknown"),
        "message": "Minimal test app running successfully!"
    }

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 