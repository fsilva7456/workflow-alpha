from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}