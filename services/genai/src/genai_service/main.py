import os

from fastapi import FastAPI

from genai_service import __version__


def create_app() -> FastAPI:
    app = FastAPI(title="GenAI Service", version=__version__)

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

    return app


app = create_app()
