from typing import Any

from psycopg_pool import AsyncConnectionPool

from chatup.repositories import ensure_thread, ensure_user


async def login_user(
    pool: AsyncConnectionPool,
    user_id: str,
    display_name: str,
) -> dict[str, Any]:
    """Ensure the user and their default main thread exist, returning both."""
    user = await ensure_user(pool, user_id=user_id, display_name=display_name)
    default_thread_id = f"{user_id}:main"
    default_thread = await ensure_thread(
        pool,
        thread_id=default_thread_id,
        user_id=user_id,
        title="Main",
    )
    return {
        "user": user,
        "default_thread": default_thread,
    }
