from __future__ import annotations

import asyncio

import httpx

from genai_service.main import app


def test_actuator_health_returns_up() -> None:
    async def run() -> None:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.get("/actuator/health")

        assert response.status_code == 200
        assert response.json() == {"status": "UP"}

    asyncio.run(run())


def test_actuator_info_returns_version() -> None:
    async def run() -> None:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            response = await client.get("/actuator/info")

        assert response.status_code == 200
        assert response.json()["build"]["version"] == "0.1.0"
        assert response.json()["build"]["commit"] == "unknown"

    asyncio.run(run())
