import httpx
import os
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
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Make a chat completion request to OpenRouter API
        """
        # Use longer timeout for complex requests
        timeout = httpx.Timeout(60.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            if max_tokens:
                payload["max_tokens"] = max_tokens
            
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.HTTPStatusError as e:
                raise Exception(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise Exception(f"Error calling OpenRouter API: {str(e)}")