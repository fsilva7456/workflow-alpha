from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

@router.get("/health-check", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")