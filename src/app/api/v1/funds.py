from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request

from ...api.dependencies import get_current_user, get_fund_service
from ...models.fund import FundOwnerType
from ...schemas.fund import FundCreate, FundTransactionResponse
from ...services import FundService

router = APIRouter(prefix="/insurance", tags=["insurance"])

# TODO: Make configurable or get from path parameter for multiple providers
SHIPSURANCE_ID = 1


@router.patch(
    "/shipsurance/add_funds",
    response_model=FundTransactionResponse,
    dependencies=[Depends(get_current_user)],
    status_code=201,
)
async def add_insurance_funds(
    request: Request,
    fund_data: FundCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    fund_service: Annotated[FundService, Depends(get_fund_service)],
) -> dict[str, Any]:
    result = await fund_service.add_funds(
        owner_type=FundOwnerType.INSURANCE,
        owner_id=SHIPSURANCE_ID,
        currency=fund_data.currency,
        amount=fund_data.amount,
    )

    return result
