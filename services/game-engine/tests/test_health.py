import os

from fastapi.testclient import TestClient

import main


def test_actuator_health_returns_up() -> None:
    with TestClient(main.app) as client:
        response = client.get("/actuator/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_actuator_info_returns_build_metadata(monkeypatch) -> None:
    monkeypatch.setenv("APP_VERSION", "test-version")
    monkeypatch.setenv("GIT_COMMIT", "test-commit")

    with TestClient(main.app) as client:
        response = client.get("/actuator/info")

    assert response.status_code == 200
    assert response.json() == {
        "build": {
            "version": "test-version",
            "commit": "test-commit",
        }
    }
