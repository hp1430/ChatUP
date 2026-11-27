from __future__ import annotations

from fastapi import APIRouter

from chatup.api.deps import PoolDep
from chatup.schemas.api import LoginRequest, UserResponse
from chatup.services.users import login_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, pool: PoolDep) -> UserResponse:
    result = await login_user(
        pool=pool,
        user_id=body.user_id.strip(),
        display_name=body.display_name.strip(),
    )
    user = result["user"]
    return UserResponse(
        user_id=user["user_id"],
        display_name=user["display_name"],
    )