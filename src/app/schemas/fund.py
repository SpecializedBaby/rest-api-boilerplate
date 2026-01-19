from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from ..models.fund import FundOwnerType


class FundBase(BaseModel):
    currency: Annotated[str, Field(min_length=3, max_length=3, examples=["USD"], description="ISO 4217 currency code")]
    amount: Annotated[Decimal, Field(ge=0, decimal_places=4, examples=[100.0000], description="Fund amount")]


class FundCreate(FundBase):
    pass

class FundRead(BaseModel):
    id: int
    currency: Annotated[str, Field(min_length=3, max_length=3, examples=["USD"])]
    amount: Annotated[Decimal, Field(examples=[100.0000])]
    owner_type: FundOwnerType
    user_id: int | None = None
    insurance_id: int | None = None
    created_at: datetime


class FundTransactionResponse(BaseModel):
    currency: str
    amount: Annotated[Decimal, Field(examples=[100.0000])]

class FundCreateInternal(BaseModel):
    currency: str
    amount: Decimal
    owner_type: FundOwnerType
    user_id: int | None = None
    insurance_id: int | None = None
