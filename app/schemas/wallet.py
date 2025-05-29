from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OperationRequest(BaseModel):
    """Запрос на операцию с кошельком."""

    operation_type: str  # "DEPOSIT" or "WITHDRAW"
    amount: Decimal


class WalletResponse(BaseModel):
    """Ответ с кошельком."""

    uuid: UUID
    balance: Decimal


class WalletCreation(BaseModel):
    """Запрос на создание кошелька."""

    balance: Decimal
