import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Wallet(Base):
    """Модель кошелька."""

    __tablename__ = "wallets"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(18, 2), nullable=False, default=0)
