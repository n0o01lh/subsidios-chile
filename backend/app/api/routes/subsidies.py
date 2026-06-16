from fastapi import APIRouter, HTTPException

from app.schemas.subsidy import SubsidyResponse
from app.services.subsidy_catalog import SUBSIDY_RULES

router = APIRouter(prefix='/subsidies')


@router.get('', response_model=list[SubsidyResponse])
async def list_subsidies() -> list[SubsidyResponse]:
    return [
        SubsidyResponse(
            id=rule.id,
            name=rule.name,
            decree=rule.decree,
            target=rule.target,
            frs_min=rule.frs_min,
            frs_max=rule.frs_max,
            benefit_uf=rule.benefit_uf,
            required_savings_uf=rule.required_savings_uf,
            max_property_value_uf=rule.max_property_value_uf,
            mortgage_allowed=rule.mortgage_allowed,
            mortgage_required=rule.mortgage_required,
            modality=rule.modality,
            region_availability=list(rule.region_availability),
            postulation_periods=list(rule.postulation_periods),
            compatible_savings_instruments=list(rule.compatible_savings_instruments),
            compatible_with=list(rule.compatible_with),
        )
        for rule in SUBSIDY_RULES
    ]


@router.get('/{subsidy_id}', response_model=SubsidyResponse)
async def get_subsidy(subsidy_id: str) -> SubsidyResponse:
    for rule in SUBSIDY_RULES:
        if rule.id == subsidy_id:
            return SubsidyResponse(
                id=rule.id,
                name=rule.name,
                decree=rule.decree,
                target=rule.target,
                frs_min=rule.frs_min,
                frs_max=rule.frs_max,
                benefit_uf=rule.benefit_uf,
                required_savings_uf=rule.required_savings_uf,
                max_property_value_uf=rule.max_property_value_uf,
                mortgage_allowed=rule.mortgage_allowed,
                mortgage_required=rule.mortgage_required,
                modality=rule.modality,
                region_availability=list(rule.region_availability),
                postulation_periods=list(rule.postulation_periods),
                compatible_savings_instruments=list(rule.compatible_savings_instruments),
                compatible_with=list(rule.compatible_with),
            )
    raise HTTPException(status_code=404, detail='Subsidy not found')
