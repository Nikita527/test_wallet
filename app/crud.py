from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet


async def get_wallet(db: AsyncSession, wallet_uuid):
    """Получение кошелька по UUID."""
    result = await db.execute(
        select(Wallet).filter(Wallet.uuid == wallet_uuid)
    )
    return result.scalars().first()


async def operate_wallet(
    db: AsyncSession, wallet_uuid, operation_type, amount
):
    """Операция с кошельком."""
    result = await db.execute(
        select(Wallet).where(Wallet.uuid == wallet_uuid).with_for_update()
    )
    wallet = result.scalars().first()
    if not wallet:
        raise ValueError("Wallet not found")
    if operation_type == "DEPOSIT":
        wallet.balance += amount
    elif operation_type == "WITHDRAW":
        if wallet.balance < amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= amount
    else:
        raise ValueError("Invalid operation type")
    await db.commit()
    await db.refresh(wallet)
    return wallet


async def create_wallet(db: AsyncSession):
    """Создание кошелька."""
    wallet = Wallet()
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet
