"""Lightweight wrapper around the OpenAI responses API with JSON output."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional, Sequence, cast

from openai import APIError, APITimeoutError, OpenAI, RateLimitError

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(
        self,
        model: str = "gpt-5-mini",
        max_retries: int = 2,
        retry_delay: float = 1.0,
        client: Optional[Any] = None,
    ):
        self._client = client or OpenAI()
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def complete_json(self, messages: Sequence[Dict[str, str]]) -> Dict[str, Any]:
        """Call the responses API and parse a JSON object."""
        attempt = 0
        while True:
            try:
                input_messages: List[Dict[str, str]] = list(messages)
                response = self._client.responses.create(
                    model=self.model,
                    input=cast(Any, input_messages),
                    text={"format": {"type": "json_object"}},
                )
                return self._extract_json(response)
            except (RateLimitError, APITimeoutError) as error:
                if attempt >= self.max_retries:
                    raise
                logger.warning(
                    "llm_retry",
                    extra={
                        "attempt": attempt + 1,
                        "error": type(error).__name__,
                        "delay_seconds": self.retry_delay,
                    },
                )
                time.sleep(self.retry_delay)
                attempt += 1
            except APIError:
                raise

    @staticmethod
    def _extract_json(response: Any) -> Dict[str, Any]:
        """Try to pull JSON text from a responses API object."""
        # Newer responses API objects often expose output_text directly.
        content_text = getattr(response, "output_text", None)
        if content_text:
            return json.loads(content_text)

        outputs: List[Any] = getattr(response, "output", [])
        if not outputs:
            raise ValueError("Empty response output")

        first_output = outputs[0]
        contents = getattr(first_output, "content", [])
        if not contents:
            raise ValueError("Empty response content")

        # Concatenate any text parts; typically there is exactly one.
        text_parts: List[str] = []
        for part in contents:
            text = getattr(part, "text", None)
            if text:
                text_parts.append(text)
        if not text_parts:
            raise ValueError("No text content in response")

        return json.loads("".join(text_parts))
