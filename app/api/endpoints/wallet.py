from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import operate_wallet, get_wallet, create_wallet
from app.database import get_session
from app.api.endpoints.auth import get_current_user
from app.schemas.wallet import WalletResponse, OperationRequest

router = APIRouter(tags=["Взаимодействие с кошельком"])


@router.post(
    "/v1/wallets/{wallet_uuid}/operation",
    response_model=WalletResponse,
    dependencies=[Depends(get_current_user)],
)
async def wallet_operation(
    wallet_uuid: UUID,
    req: OperationRequest,
    session: AsyncSession = Depends(get_session),
):
    """Операция с кошельком."""
    try:
        wallet = await operate_wallet(
            session, wallet_uuid, req.operation_type, req.amount
        )
        return wallet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/v1/wallets/{wallet_uuid}",
    response_model=WalletResponse,
    dependencies=[Depends(get_current_user)],
)
async def get_wallet_by_uuid(
    wallet_uuid: UUID, session: AsyncSession = Depends(get_session)
):
    """Получение кошелька по UUID."""
    wallet = await get_wallet(session, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post(
    "/v1/wallets",
    response_model=WalletResponse,
    dependencies=[Depends(get_current_user)],
    summary="Создать новый кошелек"
)
async def create_wallet_endpoint(session: AsyncSession = Depends(get_session)):
    """Получение всех кошельков."""
    wallet = await create_wallet(session)
    return wallet
