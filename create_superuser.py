import asyncio
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy.future import select

from app.database import async_session_maker
from app.models.users import User

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user():
    """Создание суперпользователя."""
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    hashed_password = pwd_context.hash(password)  # type: ignore

    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            print(f"Пользователь {email} уже существует.")
            return

        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        print(f"Пользователь {email} успешно создан.")


if __name__ == "__main__":
    asyncio.run(create_user())
