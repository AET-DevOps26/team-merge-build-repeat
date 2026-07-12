import os
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from fastapi import FastAPI, Header, HTTPException, Request, status
from prometheus_fastapi_instrumentator import Instrumentator
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from genai_service import __version__
from genai_service.assistant import AssistantError, LangChainSudokuAssistant
from genai_service.chat_client import ChatServiceClient, ChatServiceError
from genai_service.game_client import GameServiceClient, GameServiceError
from genai_service.schemas import GenerateChatAnswerRequest, GenerateChatAnswerResponse
from genai_service.settings import Settings, load_settings


logger = logging.getLogger("genai_service")


def _configure_logging(debug: bool) -> None:
    """Enable request-flow diagnostics without exposing request credentials."""
    if not debug:
        return

    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.propagate = False
    logger.debug("Detailed GenAI request logging is enabled.")


def _configure_chat_model(settings: Settings, chat_model: Any | None) -> Any | None:
    configured_chat_model = chat_model
    if configured_chat_model is None and settings.llm_provider == "ollama":
        configured_chat_model = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0,
        )
    if configured_chat_model is None and settings.llm_provider == "openai":
        configured_chat_model = ChatOpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )
    return configured_chat_model


def create_app(*, chat_model: Any | None = None) -> FastAPI:
    settings = load_settings()
    _configure_logging(settings.debug)
    configured_chat_model = _configure_chat_model(settings, chat_model)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.chat_client = ChatServiceClient(settings.chat_service_url)
        app.state.game_client = GameServiceClient(settings.game_service_url)
        app.state.assistant = LangChainSudokuAssistant(
            settings,
            chat_model=configured_chat_model,
        )
        try:
            yield
        finally:
            await app.state.chat_client.aclose()
            await app.state.game_client.aclose()

    app = FastAPI(
        title="GenAI Service",
        version=__version__,
        lifespan=lifespan,
        root_path=settings.root_path,
    )

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
        logger.debug("Received chat-answer request for game_id=%s.", payload.game_id)
        if authorization is None or not authorization.startswith("Bearer "):
            logger.debug(
                "Rejected chat-answer request for game_id=%s: missing or invalid bearer authorization.",
                payload.game_id,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required.",
            )

        token = authorization.removeprefix("Bearer ").strip()
        if not token:
            logger.debug(
                "Rejected chat-answer request for game_id=%s: empty bearer token.",
                payload.game_id,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required.",
            )

        chat_client = request.app.state.chat_client
        game_client = request.app.state.game_client
        assistant = request.app.state.assistant

        try:
            logger.debug("Loading chat history for game_id=%s.", payload.game_id)
            chat = await chat_client.get_chat(payload.game_id, authorization)
            logger.debug(
                "Loaded %d chat messages for game_id=%s.",
                len(chat.messages),
                payload.game_id,
            )
        except ChatServiceError as exc:
            logger.debug("Failed to load chat history for game_id=%s: %s", payload.game_id, exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

        try:
            logger.debug("Loading game data for game_id=%s.", payload.game_id)
            solution, template, board, candidates = await asyncio.gather(
                game_client.get_solution(payload.game_id, authorization),
                game_client.get_template(payload.game_id, authorization),
                game_client.get_state(payload.game_id, authorization),
                game_client.get_pencil_marks(payload.game_id, authorization),
            )
            logger.debug("Loaded game data for game_id=%s.", payload.game_id)
        except GameServiceError as exc:
            logger.debug("Failed to load game data for game_id=%s: %s", payload.game_id, exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

        try:
            logger.debug("Generating assistant answer for game_id=%s.", payload.game_id)
            assistant_response = await assistant.answer(
                payload,
                chat.messages,
                solution,
                template,
                board,
                candidates,
            )
            logger.debug("Generated assistant answer for game_id=%s.", payload.game_id)
        except AssistantError as exc:
            logger.debug("Failed to generate answer for game_id=%s: %s", payload.game_id, exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

        try:
            logger.debug("Persisting chat messages for game_id=%s.", payload.game_id)
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
            logger.debug("Persisted chat messages for game_id=%s.", payload.game_id)
        except ChatServiceError as exc:
            logger.debug("Failed to persist chat messages for game_id=%s: %s", payload.game_id, exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

        response = GenerateChatAnswerResponse(
            gameId=payload.game_id,
            message=payload.message,
            assistantResponse=assistant_response,
        )
        logger.debug("Completed chat-answer request for game_id=%s.", payload.game_id)
        return response

    return app


app = create_app()

Instrumentator().instrument(app).expose(app)
