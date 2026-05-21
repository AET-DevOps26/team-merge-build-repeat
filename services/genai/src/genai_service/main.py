from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="GenAI Service", version="0.1.0")

    @app.get("/actuator/health", tags=["actuator"])
    async def health() -> dict[str, str]:
        return {"status": "UP"}

    return app


app = create_app()
