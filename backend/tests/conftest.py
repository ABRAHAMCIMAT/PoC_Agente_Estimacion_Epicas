"""Fixtures compartidos para los tests del backend."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Permite importar `app.main` igual que lo hace uvicorn al correr el servidor.
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    """Cliente de pruebas de FastAPI sobre la app real (sin levantar un servidor)."""
    with TestClient(app) as test_client:
        yield test_client
