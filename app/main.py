import os
from fastapi import FastAPI

app = FastAPI()

# Log startup information
@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", "8080")
    print(f"Starting application on port: {port}")
    print(f"Environment variables:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}