from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from psycopg_pool import AsyncConnectionPool

from chatup.config.settings import get_settings
from chatup.repositories import touch_thread
from chatup.services.threads import verify_thread_ownership

_MEM: dict[tuple[str, str], list[BaseMessage]] = {}

SYSTEM_PROMPT = "You are ChatUp, a helpful assistant."


async def chat_once(
    pool: AsyncConnectionPool,
    thread_id: str,
    user_id: str,
    message: str,
) -> dict[str, str]:
    """Send a single message in a thread, maintaining in-memory history in _MEM."""
    if not await verify_thread_ownership(pool, thread_id=thread_id, user_id=user_id):
        raise PermissionError("Thread does not belong to user")

    history = _MEM.setdefault((thread_id, user_id), [SystemMessage(content=SYSTEM_PROMPT)])
    history.append(HumanMessage(content=message))

    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.chat_model,
        api_key=settings.openai_api_key,
    )
    response = await llm.ainvoke(history)
    reply = str(response.content)

    history.append(AIMessage(content=reply))
    await touch_thread(pool, thread_id=thread_id)   
    return {"reply": reply, "thread_id": thread_id}
