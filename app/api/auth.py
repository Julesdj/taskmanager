from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth_schema import LoginSchema, TokenSchema
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    auth_service = AuthService(db)

    user = await user_service.authenticate_user(data.email, data.password)

    tokens = await auth_service.generate_tokens(user_id=str(user.id))

    return TokenSchema(**tokens)  # includes access_token, refresh_token, token_type


@router.post("/auth/refresh", response_model=TokenSchema)
async def refresh_token(
    refresh_token: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    tokens = await auth_service.verify_and_rotate_refresh_token(refresh_token)
    return TokenSchema(**tokens)


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    auth_service = AuthService(db)
    await auth_service.logout(user_id=str(current_user.id))
