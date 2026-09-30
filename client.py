import json
import os
from urllib import request


class LLMError(Exception):
    pass


class LLMClient:
    """Tiny provider-independent chat client.

    Without CODEK_API_KEY it returns None. CodeK then uses its deterministic
    planner. No mock response is presented as a real model response.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None,
                 model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("CODEK_API_KEY")
        self.base_url = (base_url or os.getenv("CODEK_BASE_URL", "")).rstrip("/")
        self.model = model or os.getenv("CODEK_MODEL", "gpt-4o-mini")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key and self.base_url)

    def ask(self, prompt: str) -> str | None:
        if not self.enabled:
            return None

        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Return a concise plan for the coding task."},
                {"role": "user", "content": prompt},
            ],
        }).encode()

        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc
