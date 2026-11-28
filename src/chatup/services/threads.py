from typing import Any
from uuid import uuid4

from psycopg_pool import AsyncConnectionPool

from chatup.repositories import (
    ensure_thread,
    list_threads,
    thread_belongs_to_user,
    update_thread_title,
)


async def get_threads_for_user(
    pool: AsyncConnectionPool,
    user_id: str,
) -> list[dict[str, Any]]:
    """Return all threads for the given user_id."""
    return await list_threads(pool, user_id=user_id)


async def create_thread_for_user(
    pool: AsyncConnectionPool,
    user_id: str,
    title: str = "New Thread",
) -> dict[str, Any]:
    """Create a new thread for the given user_id."""
    thread_id = f"{user_id}:{uuid4().hex}"
    return await ensure_thread(pool, thread_id=thread_id, user_id=user_id, title=title)


async def rename_thread(
    pool: AsyncConnectionPool,
    thread_id: str,
    user_id: str,
    title: str,
) -> dict[str, Any] | None:
    """Update the title of a thread if it belongs to user_id."""
    if not await thread_belongs_to_user(pool, thread_id=thread_id, user_id=user_id):
        return None
    return await update_thread_title(pool, thread_id=thread_id, title=title)


async def verify_thread_ownership(
    pool: AsyncConnectionPool,
    thread_id: str,
    user_id: str,
) -> bool:
    """Return True if thread_id belongs to user_id."""
    return await thread_belongs_to_user(pool, thread_id=thread_id, user_id=user_id)
