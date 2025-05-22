from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.deps import get_db
from app.schemas.auth_schema import LoginSchema, TokenSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post("/auth/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def Login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.authenticate_user(data.email, data.password)

    access_token = create_access_token({"sub": str(user.id)})

    return TokenSchema(access_token=access_token, token_type="bearer")
