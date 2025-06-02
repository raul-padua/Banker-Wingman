#!/usr/bin/env python3
"""
Absolute minimal FastAPI app for App Runner testing
"""
from fastapi import FastAPI
from datetime import datetime

print("🚀 INITIALIZING MINIMAL APP")

app = FastAPI(title="Minimal App Runner Test")

@app.get("/")
def root():
    return {
        "status": "SUCCESS",
        "message": "Minimal App Runner deployment working!",
        "timestamp": datetime.now().isoformat(),
        "port": 8080
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

print("✅ APP INITIALIZED - Ready for uvicorn") 