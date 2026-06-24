import os
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from fastapi import FastAPI, Header, HTTPException, Request, status
from langchain_ollama import ChatOllama

from genai_service import __version__
from genai_service.assistant import AssistantError, LangChainSudokuAssistant
from genai_service.chat_client import ChatServiceClient, ChatServiceError
from genai_service.openai_model import OpenAICompatibleChatModel
from genai_service.schemas import GenerateChatAnswerRequest, GenerateChatAnswerResponse
from genai_service.settings import load_settings


def create_app(*, chat_model: Any | None = None) -> FastAPI:
    settings = load_settings()
    configured_chat_model = chat_model
    if configured_chat_model is None and settings.llm_provider == "ollama":
        configured_chat_model = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0,
        )
    if configured_chat_model is None and settings.llm_provider == "openai":
        configured_chat_model = OpenAICompatibleChatModel(
            settings.openai_base_url,
            settings.openai_api_key,
            settings.openai_model,
        )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.chat_client = ChatServiceClient(settings.chat_service_url)
        app.state.assistant = LangChainSudokuAssistant(
            settings,
            chat_model=configured_chat_model,
        )
        try:
            yield
        finally:
            await app.state.chat_client.aclose()

    app = FastAPI(title="GenAI Service", version=__version__, lifespan=lifespan)

    @app.get("/actuator/health", tags=["actuator"])
    async def health() -> dict[str, str]:
        return {"status": "UP"}

    @app.get("/actuator/info", tags=["actuator"])
    async def info() -> dict[str, dict[str, str]]:
        return {
            "build": {
                "version": __version__,
                "commit": os.getenv("GIT_COMMIT", "unknown"),
            }
        }

    @app.post(
        "/v1/chat/answer",
        response_model=GenerateChatAnswerResponse,
        tags=["chat"],
    )
    async def answer_chat(
        payload: GenerateChatAnswerRequest,
        request: Request,
        authorization: str | None = Header(default=None),
    ) -> GenerateChatAnswerResponse:
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required.",
            )

        token = authorization.removeprefix("Bearer ").strip()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required.",
            )

        chat_client = request.app.state.chat_client
        assistant = request.app.state.assistant

        try:
            chat = await chat_client.get_chat(payload.game_id, authorization)
        except ChatServiceError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

        try:
            assistant_response = await assistant.answer(payload, chat.messages)
        except AssistantError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

        try:
            await chat_client.create_message(
                payload.game_id,
                "user",
                payload.message,
                authorization,
            )
            await chat_client.create_message(
                payload.game_id,
                "assistant",
                assistant_response,
                authorization,
            )
        except ChatServiceError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

        return GenerateChatAnswerResponse(
            gameId=payload.game_id,
            message=payload.message,
            assistantResponse=assistant_response,
        )

    return app


app = create_app()
