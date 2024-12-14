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

# Initialize FastAPI app
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

# Request logging middleware
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

# Root endpoint for basic health check
@app.get("/")
async def root():
    """Root endpoint for basic health check"""
    return {"status": "ok", "message": "Service is running"}

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(llm.router, prefix="/api/v1", tags=["llm"])

# Startup event
@app.on_event("startup")
async def startup_event():
    # Get environment variables
    port = os.getenv("PORT", "8000")
    environment = os.getenv("ENVIRONMENT", "development")
    
    # Log startup information
    logger.info("Starting application...")
    logger.info(f"Environment: {environment}")
    logger.info(f"Port: {port}")
    logger.info(f"Python path: {os.getenv('PYTHONPATH', 'not set')}")
    
    # Log all environment variables for debugging
    logger.info("Environment variables:")
    for key, value in os.environ.items():
        logger.info(f"{key}: {value if 'SECRET' not in key.upper() else '[REDACTED]'}")
