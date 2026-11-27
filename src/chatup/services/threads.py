from typing import Any

from psycopg_pool import AsyncConnectionPool

from chatup.repositories import list_threads


async def get_threads_for_user(
    pool: AsyncConnectionPool,
    user_id: str,
) -> list[dict[str, Any]]:
    """Return all threads for the given user_id."""
    return await list_threads(pool, user_id=user_id)
