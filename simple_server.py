#!/usr/bin/env python3
"""
Ultra minimal FastAPI server for App Runner testing
"""
print("=== STARTING SIMPLE SERVER ===")

from fastapi import FastAPI
import uvicorn
import os

print("✅ Imports successful")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "running"}

@app.get("/test")
def test():
    return {"test": "success", "port": os.getenv("PORT", 8080)}

if __name__ == "__main__":
    print("🚀 Starting uvicorn directly...")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
else:
    print("✅ App object created for uvicorn command") 