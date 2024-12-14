from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
import logging
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)
router = APIRouter()
llm_service = LLMService()

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for the LLM", min_length=1)
    model: str = Field(..., description="Name of the LLM model to use")
    parameters: Optional[Dict] = Field(default={}, description="Optional model parameters")

    @validator('model')
    def validate_model(cls, v):
        allowed_models = ["claude", "gpt-4", "gpt-3.5-turbo"]
        if v.lower() not in allowed_models:
            raise ValueError(f"Model must be one of: {', '.join(allowed_models)}")
        return v.lower()

class LLMResponse(BaseModel):
    response: str = Field(..., description="Response from the LLM")

@router.post("/execute-llm", response_model=LLMResponse)
async def execute_llm(request: LLMRequest):
    """
    Execute an LLM task with the given prompt and parameters
    """
    logger.info(f"Executing LLM request for model: {request.model}")
    try:
        response = await llm_service.execute(
            prompt=request.prompt,
            model=request.model,
            parameters=request.parameters
        )
        logger.info("LLM request completed successfully")
        return LLMResponse(response=response)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")