"""Conversation memory service.

This module defines ``MemoryService``, responsible for storing and
retrieving the message history of a conversation, scoped by session.

The current implementation stores history in a plain Python dictionary
kept in process memory. This is intentionally a temporary storage
strategy — it does not survive process restarts and is not shared across
multiple processes/workers. It exists to unblock ``ConversationService``
now; a persistent backend (e.g. Redis) is expected to replace it later
without requiring changes to ``MemoryService``'s public interface.
"""

from __future__ import annotations

from app.ai.conversation.models import ConversationMessage


class MemoryService:
    """Manages conversation history, keyed by session.

    ``MemoryService`` abstracts away *how* and *where* conversation
    history is persisted from the rest of the AI Core. Consumers (such as
    ``ConversationService``) depend only on this public interface, not on
    the storage mechanism, which keeps the storage backend free to change
    later (e.g. to Redis) without affecting callers.

    Each ``MemoryService`` instance owns and manages its own internal
    state — a ``dict[str, list[ConversationMessage]]`` mapping a session
    id to its ordered message history. There is no global or singleton
    state: the dictionary lives on the instance, created fresh in
    ``__init__``, so multiple independent ``MemoryService`` instances
    never share history.
    """

    def __init__(self) -> None:
        """Initialize an empty, in-memory history store."""
        self._sessions: dict[str, list[ConversationMessage]] = {}

    async def get_history(self, session_id: str) -> list[ConversationMessage]:
        """Return the message history for a session.

        Args:
            session_id: The unique identifier of the conversation
                session.

        Returns:
            A list of ``ConversationMessage`` instances in chronological
            order. Returns an empty list for a session that has no
            history yet (this does not create an entry for the session).
        """
        return list(self._sessions.get(session_id, []))

    async def add_message(self, session_id: str, message: ConversationMessage) -> None:
        """Append a message to a session's history.

        If the session does not yet exist, it is created implicitly.

        Args:
            session_id: The unique identifier of the conversation
                session.
            message: The message to append to the session's history.
        """
        self._sessions.setdefault(session_id, []).append(message)

    async def clear(self, session_id: str) -> None:
        """Remove all stored history for a session.

        Args:
            session_id: The unique identifier of the conversation
                session to clear. Clearing a session that has no stored
                history is a no-op.
        """
        self._sessions.pop(session_id, None)
