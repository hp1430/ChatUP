from __future__ import annotations

from fastapi import APIRouter, HTTPException

from chatup.api.deps import AppRuntimeDep, PoolDep, UserIdDep
from chatup.schemas.api import ChatRequest, ChatResponse, MessageResponse
from chatup.services.chat import chat_once

router = APIRouter(prefix="/api/threads", tags=["chat"])

@router.get("/{thread_id}/messages", response_model=MessageResponse)
def list_thread_messages(
    thread_id: str,
    _user_id: UserIdDep,
) -> MessageResponse:
    return MessageResponse(thread_id=thread_id, messages=[])


@router.post("/{thread_id}/chat", response_model=ChatResponse)
async def send_message(
    thread_id: str,
    body: ChatRequest,
    user_id: UserIdDep,
    pool: PoolDep,
    runtime: AppRuntimeDep,
) -> ChatResponse:
    try:
        result = await chat_once(
            pool=pool,
            runtime=runtime,
            thread_id=thread_id,
            user_id=user_id,
            message=body.message.strip(),
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    return ChatResponse(
        reply=result["reply"],
        thread_id=result["thread_id"],
    )