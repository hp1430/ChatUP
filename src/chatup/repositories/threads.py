from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


async def list_threads(
    pool: AsyncConnectionPool,
    user_id: str,
) -> list[dict[str, Any]]:
    """Return all threads belonging to the given user_id, ordered by most recently updated."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT thread_id, user_id, title, created_at, updated_at
                FROM chatup_threads
                WHERE user_id = %s
                ORDER BY updated_at DESC
                """,
                (user_id,),
            )
            return await cur.fetchall()


async def ensure_thread(
    pool: AsyncConnectionPool,
    thread_id: str,
    user_id: str,
    title: str | None = None,
) -> dict[str, Any]:
    """Create a thread if it does not exist, then return the created or existing thread."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                INSERT INTO chatup_threads (thread_id, user_id, title)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO NOTHING
                RETURNING thread_id, user_id, title, created_at, updated_at
                """,
                (thread_id, user_id, title),
            )
            row = await cur.fetchone()
            if row is not None:
                return row

            await cur.execute(
                """
                SELECT thread_id, user_id, title, created_at, updated_at
                FROM chatup_threads
                WHERE thread_id = %s
                """,
                (thread_id,),
            )
            existing = await cur.fetchone()
            assert existing is not None
            return existing


async def update_thread_title(
    pool: AsyncConnectionPool,
    thread_id: str,
    title: str,
) -> dict[str, Any] | None:
    """Update the title of a thread and return the updated row, or None if not found."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE chatup_threads
                SET title = %s,
                    updated_at = now()
                WHERE thread_id = %s
                RETURNING thread_id, user_id, title, created_at, updated_at
                """,
                (title, thread_id),
            )
            return await cur.fetchone()


async def touch_thread(
    pool: AsyncConnectionPool,
    thread_id: str,
) -> dict[str, Any] | None:
    """Update the updated_at timestamp of a thread to now() and return the updated row, or None if not found."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE chatup_threads
                SET updated_at = now()
                WHERE thread_id = %s
                RETURNING thread_id, user_id, title, created_at, updated_at
                """,
                (thread_id,),
            )
            return await cur.fetchone()
