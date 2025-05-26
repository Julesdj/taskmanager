import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.db.deps import get_db
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository


class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db
        self.refresh_repo = RefreshTokenRepository(db)

    async def generate_tokens(
        self,
        user_id: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
        session_id: str | None = None,
    ) -> dict:
        session_id = session_id or str(uuid.uuid4())

        access_token = security.create_access_token({"sub": user_id, "sid": session_id})
        # access_token = security.create_access_token({"sub": user_id})

        refresh_lifetime = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_data = security.create_refresh_token(
            user_id, refresh_lifetime, session_id
        )

        refresh_token = RefreshToken(
            user_id=user_id,
            jti=refresh_data["jti"],
            expires_at=refresh_data["exp"],
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        # Save the refresh token in DB
        await self.refresh_repo.save_token(refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_data["token"],
            "token_type": "bearer",
        }

    async def verify_and_rotate_refresh_token(
        self,
        token: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        now = datetime.now(timezone.utc)

        payload = security.decode_refresh_token(token)
        jti = payload["jti"]
        user_id = payload["sub"]
        session_id = payload["sid"]

        token_obj = await self.refresh_repo.get_by_jti_for_update(jti)
        if not token_obj or token_obj.revoked or token_obj.expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Revoke old token
        await self.refresh_repo.revoke_token(jti, now)

        # Issue new tokens
        return await self.generate_tokens(
            user_id=user_id,
            user_agent=token_obj.user_agent or user_agent,
            ip_address=token_obj.ip_address or ip_address,
            session_id=session_id,
        )

    async def logout(self, user_id: str) -> None:
        now = datetime.now(timezone.utc)
        await self.refresh_repo.revoke_all_tokens_for_user(user_id, now)

    async def list_sessions(self, user_id: str):
        now = datetime.now(timezone.utc)
        return await self.refresh_repo.get_active_sessions_for_user(user_id, now)
