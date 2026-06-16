from fastapi import APIRouter

from app.schemas.plan import PlanGenerationRequest, PlanGenerationResponse
from app.services.plan_generator import PlanGenerator

router = APIRouter(prefix='/plans')
plan_generator = PlanGenerator()


@router.post('/generate', response_model=PlanGenerationResponse)
async def generate_plans(payload: PlanGenerationRequest) -> PlanGenerationResponse:
    return plan_generator.generate(payload)
