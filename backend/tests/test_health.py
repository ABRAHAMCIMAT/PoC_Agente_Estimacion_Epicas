"""Smoke tests del endpoint /health: deben pasar con o sin modelos entrenados."""


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_payload_shape(client):
    response = client.get("/health")
    body = response.json()

    assert body["status"] == "healthy"
    assert isinstance(body["models_loaded"], bool)
    assert "timestamp" in body
