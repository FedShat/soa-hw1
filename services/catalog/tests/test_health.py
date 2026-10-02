from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    ("method", "path", "status"),
    [
        ("GET", "/", 404),
        ("GET", "/health/extra", 404),
        ("GET", "/products", 404),
        ("POST", "/health", 405),
    ],
)
def test_routes(client: TestClient, method: str, path: str, status: int) -> None:
    assert client.request(method, path).status_code == status
