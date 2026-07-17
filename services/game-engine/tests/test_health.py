from fastapi.testclient import TestClient
import pytest

import main
from sudoku_solver import map_difficulty_to_level


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


def test_map_difficulty_to_level_rejects_unsupported_values() -> None:
    assert map_difficulty_to_level("easy") == 0.4
    assert map_difficulty_to_level("medium") == 0.5
    assert map_difficulty_to_level("hard") == 0.6

    with pytest.raises(ValueError, match="Unsupported difficulty"):
        map_difficulty_to_level("expert")


def test_sudoku_rejects_unsupported_difficulty() -> None:
    with TestClient(main.app) as client:
        response = client.get("/sudoku?difficulty=expert")

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported difficulty. Choose easy, medium, or hard."
