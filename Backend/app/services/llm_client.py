from typing import Iterable, List, Dict
from app.core.config import settings

# OpenAI
from openai import OpenAI

# Google Gemini
import google.generativeai as genai

RoleMsg = Dict[str, str]  # {"role": "system|user|assistant", "content": "..."}

class LLMClient:
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY missing")
            self._openai = OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "google":
            if not settings.google_api_key:
                raise RuntimeError("GOOGLE_API_KEY missing")
            genai.configure(api_key=settings.google_api_key)
            self._gemini = genai.GenerativeModel(self.model)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate(self, messages: List[RoleMsg], temperature: float = 0.2, max_tokens: int | None = None) -> str:
        if self.provider == "openai":
            resp = self._openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
            )
            return resp.choices[0].message.content or ""
        else:
            contents = [{"role": m["role"], "parts": [m["content"]]} for m in messages]
            resp = self._gemini.generate_content(contents, generation_config={"temperature": temperature})
            return resp.text or ""

    def stream_generate(self, messages: List[RoleMsg], temperature: float = 0.2, max_tokens: int | None = None) -> Iterable[str]:
        if self.provider == "openai":
            stream = self._openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        else:
            contents = [{"role": m["role"], "parts": [m["content"]]} for m in messages]
            for ev in self._gemini.generate_content(contents, stream=True):
                if getattr(ev, "text", None):
                    yield ev.text
