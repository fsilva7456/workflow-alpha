from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal
from openai import OpenAI
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Startup event to verify OpenAI connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify OpenAI API key on startup
    try:
        # Test API connection with a simple completion
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("Successfully connected to OpenAI API")
    except Exception as e:
        print(f"Error connecting to OpenAI API: {str(e)}")
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM", min_length=1)
    model: Literal["gpt-4", "gpt-3.5-turbo"] = Field(
        default="gpt-3.5-turbo",
        description="Name of the OpenAI model to use"
    )
    parameters: Optional[Dict] = Field(
        default={
            "temperature": 0.7,
            "max_tokens": 1000
        },
        description="Optional model parameters"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a short story about a robot",
                "model": "gpt-3.5-turbo",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            }
        }

class LLMResponse(BaseModel):
    response: str

def verify_api_key():
    if not os.getenv('OPENAI_API_KEY'):
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured"
        )
    return True

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}

@app.post("/execute-llm", response_model=LLMResponse)
async def execute_llm(request: LLMRequest, api_key_valid: bool = Depends(verify_api_key)):
    try:
        print(f"Received request for model: {request.model}")
        # Create chat completion
        completion = client.chat.completions.create(
            model=request.model,
            messages=[{
                "role": "user",
                "content": request.prompt
            }],
            temperature=request.parameters.get("temperature", 0.7),
            max_tokens=request.parameters.get("max_tokens", 1000)
        )
        
        # Extract the response
        response = completion.choices[0].message.content
        print(f"Generated response with length: {len(response)}")
        
        return LLMResponse(response=response)

    except Exception as e:
        print(f"Error in execute_llm: {str(e)}")
        if 'api_key' in str(e).lower():
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error calling OpenAI API: {str(e)}"
        )