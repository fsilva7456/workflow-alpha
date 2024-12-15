from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="LLM API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM")
    model: Literal["gpt-4", "gpt-3.5-turbo"] = "gpt-3.5-turbo"
    parameters: Dict = Field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 1000
    })

class LLMResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}

@app.get("/health-check")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest):
    logger.info(f"Generate endpoint called with model: {request.model}")
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Call OpenAI API
        completion = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            temperature=request.parameters.get("temperature", 0.7),
            max_tokens=request.parameters.get("max_tokens", 1000)
        )
        
        response = completion.choices[0].message.content
        logger.info("Successfully generated response")
        return LLMResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error in generate_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
