"""System prompt definitions.

This module holds the system prompt used to instruct the AI assistant on
its role, tone, and constraints. The current prompt is intentionally
minimal and generic — refining it (tone, sales-specific instructions,
guardrails, etc.) is left for later iterations. It exists as a single,
stable place ``ConversationService`` can depend on rather than hardcoding
prompt text itself.
"""

from __future__ import annotations

_DEFAULT_SYSTEM_PROMPT = (
    "You are the VoiceFlow AI assistant. Respond helpfully, clearly, and "
    "honestly to the user's messages."
)


def get_system_prompt() -> str:
    """Return the system prompt used to initialize the AI assistant.

    Returns:
        The system prompt text.
    """
    return _DEFAULT_SYSTEM_PROMPT
