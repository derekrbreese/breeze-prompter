import httpx
import os
import time
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/breese-prompter",
            "X-Title": "Breese Prompter"
        }

        # Model and timeout configuration via environment
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        timeout_read = float(os.getenv("OR_TIMEOUT_READ", "30"))
        timeout_connect = float(os.getenv("OR_TIMEOUT_CONNECT", "5"))

        # Reusable async client with HTTP/2 and connection pooling
        self._timeout = httpx.Timeout(timeout_read, connect=timeout_connect)
        self._limits = httpx.Limits(max_keepalive_connections=10, max_connections=100)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self._timeout,
            http2=True,
            limits=self._limits,
        )
        self._logger = logging.getLogger("openrouter")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Make a chat completion request to OpenRouter API
        """
        selected_model = model or self.model
        payload = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            start = time.perf_counter()
            response = await self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            elapsed_ms = (time.perf_counter() - start) * 1000
            if self._logger:
                self._logger.debug(
                    "openrouter.chat_completion model=%s max_tokens=%s duration_ms=%.1f status=%s",
                    selected_model,
                    payload.get("max_tokens"),
                    elapsed_ms,
                    response.status_code,
                )

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Error calling OpenRouter API: {str(e)}")

    async def aclose(self) -> None:
        try:
            await self._client.aclose()
        except Exception:
            pass