from fastapi.testclient import TestClient

from genai_service.main import app


def test_actuator_health_returns_up() -> None:
    client = TestClient(app)

    response = client.get("/actuator/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
