from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional
import os

app = FastAPI()

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
    model: str = Field(..., description="Name of the LLM model to use")
    parameters: Optional[Dict] = Field(default={}, description="Optional model parameters")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a short story about a robot",
                "model": "claude",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            }
        }

class LLMResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/execute-llm", response_model=LLMResponse)
async def execute_llm(request: LLMRequest):
    try:
        # Validate model
        allowed_models = ["claude", "gpt-4", "gpt-3.5-turbo"]
        if request.model.lower() not in allowed_models:
            raise HTTPException(
                status_code=400,
                detail=f"Model must be one of: {', '.join(allowed_models)}"
            )

        # Mock response for now
        response = f"Mock response from {request.model}: Based on your prompt '{request.prompt}', here is a simulated response."
        
        return LLMResponse(response=response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
