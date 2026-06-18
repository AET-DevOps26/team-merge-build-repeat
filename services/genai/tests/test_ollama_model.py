from __future__ import annotations

import asyncio

import httpx
from langchain_core.messages import HumanMessage, SystemMessage

from genai_service.ollama_model import OllamaChatModel


def test_ollama_chat_model_calls_chat_api() -> None:
    async def run() -> None:
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json={"message": {"role": "assistant", "content": "Antwort"}},
            )

        transport = httpx.MockTransport(handler)

        class TestOllamaChatModel(OllamaChatModel):
            async def ainvoke(self, messages):
                payload = {
                    "model": self._model,
                    "stream": False,
                    "messages": [
                        {"role": self._role_for(message), "content": str(message.content)}
                        for message in messages
                    ],
                }
                async with httpx.AsyncClient(
                    base_url=self._base_url,
                    transport=transport,
                    timeout=self._timeout,
                ) as client:
                    response = await client.post("/api/chat", json=payload)
                    response.raise_for_status()
                return response.json()["message"]["content"]

        model = TestOllamaChatModel("http://ollama", "smollm2:135m")

        response = await model.ainvoke(
            [SystemMessage(content="System"), HumanMessage(content="Hallo")]
        )

        assert response == "Antwort"
        assert requests[0].url.path == "/api/chat"
        assert requests[0].read() == (
            b'{"model":"smollm2:135m","stream":false,'
            b'"messages":[{"role":"system","content":"System"},'
            b'{"role":"user","content":"Hallo"}]}'
        )

    asyncio.run(run())
