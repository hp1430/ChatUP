from psycopg_pool import AsyncConnectionPool

from chatup.agents.runtime import AppRuntime
from chatup.repositories import touch_thread
from chatup.services.threads import verify_thread_ownership


async def chat_once(
    pool: AsyncConnectionPool,
    runtime: AppRuntime,
    thread_id: str,
    user_id: str,
    message: str,
) -> dict[str, str]:
    """Send a single message in a thread using the LangGraph checkpointer runtime."""
    if not await verify_thread_ownership(pool, thread_id=thread_id, user_id=user_id):
        raise PermissionError("Thread does not belong to user")

    reply, _ = runtime.chat(
        user_id=user_id,
        thread_id=thread_id,
        user_message=message,
    )
    await touch_thread(pool, thread_id=thread_id)
    return {"reply": reply, "thread_id": thread_id}
