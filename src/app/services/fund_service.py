from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions.http_exceptions import BadRequestException
from ..crud.crud_fund import crud_funds
from ..models.fund import FundOwnerType
from ..schemas.fund import FundRead, FundCreateInternal


class FundService:

    def __init__(self, db: AsyncSession):
        self._db = db

    async def add_funds(
        self, owner_type: FundOwnerType, owner_id: int, currency: str, amount: Decimal
    ) -> dict[str, Any]:

        if amount <= 0:
            raise BadRequestException("Amount must be positive")

        currency = currency.upper()

        try:
            # Begin transaction
            existing_fund = False

            if existing_fund:
                # Update existing fund atomically
                current_balance = Decimal(str(existing_fund["amount"]))
                new_balance = current_balance + amount

                await crud_funds.update(
                    db=self._db,
                    id=existing_fund["id"],
                    object={"amount": new_balance},
                )
                fund_id = existing_fund["id"]
            else:
                # Create new fund record
                create_params = {"user_id": owner_id, "insurance_id": None}
                fund_internal = FundCreateInternal(
                    currency=currency,
                    amount=amount,
                    owner_type=owner_type,
                    **create_params,
                )

                created_fund = await crud_funds.create(
                    db=self._db, object=fund_internal, schema_to_select=FundRead
                )

                if created_fund is None:
                    raise BadRequestException("Failed to create fund record")

                fund_id = created_fund["id"]
                new_balance = amount

            await self._db.commit()

            return {
                "currency": currency,
                "amount": amount,
            }

        except Exception as e:
            await self._db.rollback()
            if isinstance(e, BadRequestException):
                raise
            raise BadRequestException(f"Transaction failed: {str(e)}") from e
