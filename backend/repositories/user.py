from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models import User, RevokedToken
from backend.security import hash_password


class UserRepository:
    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create_user(
        session: AsyncSession, email: str, password: str, is_admin: bool = False
    ):
        hashed_password = hash_password(password)
        new_user = User(email=email, password_hash=hashed_password, is_admin=is_admin)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_all_users(session: AsyncSession):
        result = await session.execute(select(User))
        return result.scalars().all()


class RevokedTokenRepository:
    @staticmethod
    async def revoke_token(session: AsyncSession, token: str, expires_at: datetime):
        revoked_token = RevokedToken(token=token, expires_at=expires_at)
        session.add(revoked_token)
        await session.commit()

    @staticmethod
    async def is_token_revoked(session: AsyncSession, token: str):
        result = await session.execute(
            select(RevokedToken).where(RevokedToken.token == token)
        )
        return result.scalars().first() is not None
