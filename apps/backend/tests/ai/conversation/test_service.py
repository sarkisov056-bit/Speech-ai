"""Unit tests for ``ConversationService``.

These tests exercise ``ConversationService`` as a plain Python object —
no FastAPI app, no HTTP server, and no real AI vendor SDK. ``MemoryService``
is used for real (its in-memory implementation is fast and
deterministic); ``AIProvider`` is replaced with ``FakeAIProvider``.
"""

from __future__ import annotations

from app.ai.conversation.service import ConversationService
from app.ai.memory.service import MemoryService
from tests.fakes import FakeAIProvider


def _make_service(response_text: str = "fake response") -> tuple[ConversationService, FakeAIProvider, MemoryService]:
    """Build a ``ConversationService`` wired up with test doubles/real memory."""
    ai_provider = FakeAIProvider(response_text=response_text)
    memory_service = MemoryService()
    service = ConversationService(ai_provider=ai_provider, memory_service=memory_service)
    return service, ai_provider, memory_service


async def test_chat_with_new_session_returns_ai_reply() -> None:
    """A brand-new session id should work without any prior setup."""
    service, _, _ = _make_service(response_text="hello there")

    reply = await service.chat(session_id="session-1", message="hi")

    assert reply == "hello there"


async def test_chat_with_existing_session_uses_prior_history() -> None:
    """A second call on the same session should include prior turns."""
    service, ai_provider, _ = _make_service(response_text="second reply")

    await service.chat(session_id="session-1", message="first message")
    await service.chat(session_id="session-1", message="second message")

    # The second request sent to the provider should include the first
    # user message and the first assistant reply (2 prior messages),
    # plus the new user message: 2 + 1 = 3 total.
    second_request = ai_provider.received_requests[1]
    assert len(second_request.messages) == 3
    assert second_request.messages[0].role == "user"
    assert second_request.messages[0].content == "first message"
    assert second_request.messages[1].role == "assistant"
    assert second_request.messages[-1].content == "second message"


async def test_chat_persists_history_in_memory_service() -> None:
    """After chatting, both user and assistant messages should be stored."""
    service, _, memory_service = _make_service(response_text="stored reply")

    await service.chat(session_id="session-1", message="remember this")

    history = await memory_service.get_history("session-1")
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].content == "remember this"
    assert history[1].role == "assistant"
    assert history[1].content == "stored reply"


async def test_chat_stores_ai_response_content_exactly() -> None:
    """The exact AI response text should be both returned and stored."""
    service, _, memory_service = _make_service(response_text="exact ai text")

    reply = await service.chat(session_id="session-2", message="question")

    history = await memory_service.get_history("session-2")
    assistant_messages = [m for m in history if m.role == "assistant"]
    assert reply == "exact ai text"
    assert assistant_messages[-1].content == "exact ai text"


async def test_chat_keeps_sessions_independent() -> None:
    """Two different session ids should not share history."""
    service, _, memory_service = _make_service()

    await service.chat(session_id="session-a", message="only in a")
    await service.chat(session_id="session-b", message="only in b")

    history_a = await memory_service.get_history("session-a")
    history_b = await memory_service.get_history("session-b")

    assert [m.content for m in history_a if m.role == "user"] == ["only in a"]
    assert [m.content for m in history_b if m.role == "user"] == ["only in b"]
