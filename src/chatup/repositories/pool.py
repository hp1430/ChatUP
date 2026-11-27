from __future__ import annotations

from psycopg_pool import AsyncConnectionPool

from chatup.config.settings import Settings, get_settings


def create_pool(settings: Settings | None = None) -> AsyncConnectionPool:
    """Create and configure an AsyncConnectionPool from application settings."""
    cfg = settings or get_settings()
    return AsyncConnectionPool(
        conninfo=cfg.database_url,
        min_size=cfg.postgres_pool_min_size,
        max_size=cfg.postgres_pool_max_size,
        open=cfg.postgres_pool_open,
    )
