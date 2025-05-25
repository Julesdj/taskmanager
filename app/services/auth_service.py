from datetime import timedelta

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

    async def generate_tokens(self, user_id: str) -> dict:
        access_token = security.create_access_token({"sub": user_id})

        refresh_lifetime = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_data = security.create_refresh_token(user_id, refresh_lifetime)

        refresh_token = RefreshToken(
            user_id=user_id,
            jti=refresh_data["jti"],
            expires_at=refresh_data["exp"],
        )
        # Save the refresh token in DB (optional but recommended for revocation/rotation)
        await self.refresh_repo.save_token(refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_data["token"],
            "token_type": "bearer",
        }

    async def verify_and_rotate_refresh_token(self, token: str) -> dict:
        payload = security.decode_refresh_token(token)
        jti = payload["jti"]
        user_id = payload["sub"]

        token_obj = await self.refresh_repo.get_by_jti(jti)
        if not token_obj or token_obj.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Revoke old token
        await self.refresh_repo.revoke_token(jti)

        # Issue new tokens
        return await self.generate_tokens(user_id)

    async def logout(self, user_id: str) -> None:
        await self.refresh_repo.revoke_all_tokens_for_user(user_id)
