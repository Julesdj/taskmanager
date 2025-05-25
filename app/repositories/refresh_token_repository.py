from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_jti(self, jti: str) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.jti == jti)
        )
        return result.scalar_one_or_none()

    async def save_token(self, token: RefreshToken):
        self.db.add(token)
        await self.db.commit()

    async def revoke_token(self, jti: str):
        token = await self.get_by_jti(jti)
        if token and not token.revoked:
            token.revoked = True
            token.revoked_at = datetime.now(timezone.utc)
            await self.db.commit()
