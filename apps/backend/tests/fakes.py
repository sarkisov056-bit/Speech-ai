"""Test doubles for the AI Core.

Contains ``FakeAIProvider``, an in-memory ``AIProvider`` implementation
used by unit tests so that ``ConversationService`` can be tested without
any real AI vendor SDK or network access.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from app.ai.providers.interfaces import AIProvider, GenerationRequest, GenerationResponse


class FakeAIProvider(AIProvider):
    """In-memory ``AIProvider`` test double.

    ``FakeAIProvider`` returns a deterministic, canned response instead of
    calling any real AI vendor, and records every ``GenerationRequest`` it
    receives so tests can assert on what ``ConversationService`` sent it
    (e.g. that conversation history was passed through correctly).
    """

    def __init__(self, response_text: str = "fake response") -> None:
        """Initialize the fake provider.

        Args:
            response_text: The text that ``generate_response`` will
                return for every call.
        """
        self._response_text = response_text
        self.received_requests: list[GenerationRequest] = []

    async def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """Record the request and return a canned ``GenerationResponse``.

        Args:
            request: The generation request sent by the caller.

        Returns:
            A ``GenerationResponse`` containing the configured canned
            text and placeholder usage/model values.
        """
        self.received_requests.append(request)
        return GenerationResponse(
            text=self._response_text,
            usage_prompt_tokens=0,
            usage_completion_tokens=0,
            model="fake-model",
        )

    async def stream_response(self, request: GenerationRequest) -> AsyncIterator[str]:
        """Record the request and yield the canned response as one chunk.

        Args:
            request: The generation request sent by the caller.

        Yields:
            The configured canned response text as a single chunk.
        """
        self.received_requests.append(request)
        yield self._response_text
