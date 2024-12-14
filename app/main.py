import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import llm, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Workflow Automation API",
    description="API for executing LLM-based workflow tasks",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Request completed: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Add a root endpoint for basic health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Service is running"}

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(llm.router, prefix="/api/v1", tags=["llm"])

# Startup event handler
@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", 8000)
    logger.info(f"Starting application on port {port}")
    logger.info("Environment variables:")
    logger.info(f"PORT: {os.getenv('PORT', 'not set')}")
    logger.info(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'not set')}")