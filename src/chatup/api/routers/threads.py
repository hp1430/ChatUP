from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from chatup.api.deps import PoolDep, UserIdDep
from chatup.schemas.api import ThreadCreate, ThreadResponse, ThreadUpdate
from chatup.services.threads import (
    create_thread_for_user,
    get_threads_for_user,
    rename_thread,
)

router = APIRouter(prefix="/api/threads", tags=["threads"])


def _timestamp(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


# todo: move it to a factory/adapter layer
def _to_response(row: dict) -> ThreadResponse:
    return ThreadResponse(
        thread_id=row["thread_id"],
        title=row["title"],
        created_at=_timestamp(row.get("created_at")),
        updated_at=_timestamp(row.get("updated_at")),
    )


@router.get("/", response_model=list[ThreadResponse])
async def list_threads(
    user_id: UserIdDep,
    pool: PoolDep,
) -> list[ThreadResponse]:
    threads = await get_threads_for_user(pool=pool, user_id=user_id)
    return [_to_response(row) for row in threads]


@router.post("/", response_model=ThreadResponse)
async def create_thread(
    body: ThreadCreate,
    user_id: UserIdDep,
    pool: PoolDep,
) -> ThreadResponse:
    thread = await create_thread_for_user(
        pool=pool,
        user_id=user_id,
        title=body.title.strip(),
    )
    return _to_response(thread)


@router.patch("/{thread_id}", response_model=ThreadResponse)
@router.put("/{thread_id}", response_model=ThreadResponse)
async def update_thread(
    thread_id: str,
    body: ThreadUpdate,
    user_id: UserIdDep,
    pool: PoolDep,
) -> ThreadResponse:
    thread = await rename_thread(
        pool=pool,
        thread_id=thread_id,
        user_id=user_id,
        title=body.title.strip(),
    )
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return _to_response(thread)