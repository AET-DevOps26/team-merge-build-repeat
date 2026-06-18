from __future__ import annotations

import asyncio

import httpx
from langchain_core.messages import HumanMessage, SystemMessage

from genai_service.openai_model import OpenAICompatibleChatModel


def test_openai_compatible_chat_model_calls_chat_completions_api() -> None:
    async def run() -> None:
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {"message": {"role": "assistant", "content": "Antwort"}}
                    ]
                },
            )

        transport = httpx.MockTransport(handler)

        class TestOpenAICompatibleChatModel(OpenAICompatibleChatModel):
            async def ainvoke(self, messages):
                payload = {
                    "model": self._model,
                    "messages": [
                        {"role": self._role_for(message), "content": str(message.content)}
                        for message in messages
                    ],
                }
                headers = {"Authorization": f"Bearer {self._api_key}"}
                async with httpx.AsyncClient(
                    base_url=self._base_url,
                    transport=transport,
                    timeout=self._timeout,
                ) as client:
                    response = await client.post(
                        "/chat/completions",
                        json=payload,
                        headers=headers,
                    )
                    response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

        model = TestOpenAICompatibleChatModel(
            "https://logos.aet.cit.tum.de:8080/v1",
            "lg-test",
            "openai/gpt-oss-120b",
        )

        response = await model.ainvoke(
            [SystemMessage(content="System"), HumanMessage(content="Hallo")]
        )

        assert response == "Antwort"
        assert requests[0].url.path == "/v1/chat/completions"
        assert requests[0].headers["authorization"] == "Bearer lg-test"
        assert requests[0].read() == (
            b'{"model":"openai/gpt-oss-120b",'
            b'"messages":[{"role":"system","content":"System"},'
            b'{"role":"user","content":"Hallo"}]}'
        )

    asyncio.run(run())
