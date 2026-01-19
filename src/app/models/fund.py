from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .insurance import Insurance
    from .user import User


class FundOwnerType(str, Enum):
    USER = "USER"
    INSURANCE = "INSURANCE"
    CARRIER = "CARRIER"


class Fund(Base):
    __tablename__ = "fund"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, init=False)

    owner_type: Mapped[FundOwnerType] = mapped_column(String(20), index=True)

    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=4), nullable=False, default=Decimal("0.0000"))

    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True, default=None)
    insurance_id: Mapped[int | None] = mapped_column(
        ForeignKey("insurance.id", ondelete="CASCADE"), index=True, default=None
    )

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid7, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    # Relationships
    user: Mapped["User | None"] = relationship("User", back_populates="funds", init=False, default=None)
    insurance: Mapped["Insurance | None"] = relationship("Insurance", back_populates="funds", init=False, default=None)
