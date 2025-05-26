from datetime import datetime
from typing import Sequence

from sqlalchemy import and_, delete, select, update
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

    async def get_by_jti_for_update(self, jti: str) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.jti == jti).with_for_update()
        )
        return result.scalar_one_or_none()

    async def save_token(self, token: RefreshToken):
        self.db.add(token)
        await self.db.commit()

    async def update_token_metadata(self, jti: str, ip: str, user_agent: str):
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.jti == jti)
            .values(ip_address=ip, user_agent=user_agent)
        )
        await self.db.commit()

    async def revoke_token(self, jti: str, now: datetime):
        token = await self.get_by_jti(jti)
        if token and not token.revoked:
            token.revoked = True
            token.revoked_at = now
            await self.db.commit()

    async def revoke_all_tokens_for_user(self, user_id: str, now: datetime):
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
            .values(
                revoked=True,
                revoked_at=now,
            )
        )
        await self.db.commit()

    async def get_active_sessions_for_user(
        self, user_id: str, now: datetime
    ) -> Sequence[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken)
            .where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.revoked.is_(False),
                    RefreshToken.expires_at > now,
                )
            )
            .order_by(RefreshToken.created_at.desc())
        )
        return result.scalars().all()

    # method to clean up expired + revoked tokens to keep the DB lean
    # Run this periodically via a background task or cron job.
    async def delete_expired_and_revoked(self, now: datetime):
        await self.db.execute(
            delete(RefreshToken).where(
                RefreshToken.revoked.is_(True),
                RefreshToken.expires_at < now,
            )
        )
        await self.db.commit()
