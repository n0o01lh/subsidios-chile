from fastapi import APIRouter

from app.schemas.combiner import CombinationRequest, CombinationResponse
from app.schemas.eligibility import EligibilityRequest, EligibilityResponse
from app.services.eligibility_engine import EligibilityEngine
from app.services.subsidy_combiner import SubsidyCombiner

router = APIRouter(prefix='/eligibility')
engine = EligibilityEngine()
combiner = SubsidyCombiner()


@router.post('/check', response_model=EligibilityResponse)
async def check_eligibility(payload: EligibilityRequest) -> EligibilityResponse:
    return engine.check_eligibility(payload)


@router.post('/combine', response_model=CombinationResponse)
async def combine_subsidies(payload: CombinationRequest) -> CombinationResponse:
    return combiner.combine(payload.selected_subsidies)
