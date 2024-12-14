from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM")
    model: str = Field(..., description="Name of the LLM model to use")
    parameters: Optional[Dict] = Field(default={}, description="Optional model parameters")

class LLMResponse(BaseModel):
    response: str = Field(..., description="Response from the LLM")

@router.post("/execute-llm", response_model=LLMResponse)
async def execute_llm(request: LLMRequest):
    try:
        response = await llm_service.execute(
            prompt=request.prompt,
            model=request.model,
            parameters=request.parameters
        )
        return LLMResponse(response=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")