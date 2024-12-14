from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import llm

app = FastAPI(
    title="Workflow Automation API",
    description="API for executing LLM-based workflow tasks",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm.router, prefix="/api/v1")