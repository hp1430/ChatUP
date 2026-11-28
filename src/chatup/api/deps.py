from __future__ import annotations
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from psycopg_pool import AsyncConnectionPool

from chatup.agents.runtime import AppRuntime, create_app_runtime
from chatup.config import get_settings
from chatup.repositories import create_pool


@lru_cache
def get_app_runtime() -> AppRuntime:
    return create_app_runtime(get_settings())

def require_user_id(
        x_user_id: str | None = Header(None, alias="X-User-Id"),
) -> str:
    if x_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="X-User_Id header required"
        )
    user_id = x_user_id.strip()
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="X-User-Id header required"
        )
    return user_id

@lru_cache
def _get_cached_pool() -> AsyncConnectionPool:
    return create_pool()


async def get_db_pool() -> AsyncConnectionPool:
    pool = _get_cached_pool()
    if pool._closed:
        await pool.open()
    return pool


def shutdown_runtime() -> None:
    return None

UserIdDep = Annotated[str, Depends(require_user_id)]
PoolDep = Annotated[AsyncConnectionPool, Depends(get_db_pool)]
AppRuntimeDep = Annotated[AppRuntime, Depends(get_app_runtime)]
