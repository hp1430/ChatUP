from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


async def ensure_user(
    pool: AsyncConnectionPool,
    user_id: str,
    display_name: str,
) -> dict[str, Any]:
    """Create a user if it does not exist, then return the created or existing user."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                INSERT INTO chatup_users (user_id, display_name)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO NOTHING
                RETURNING user_id, display_name, created_at
                """,
                (user_id, display_name),
            )
            row = await cur.fetchone()
            if row is not None:
                return row

            await cur.execute(
                """
                SELECT user_id, display_name, created_at
                FROM chatup_users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            existing = await cur.fetchone()
            assert existing is not None
            return existing
