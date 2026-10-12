from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "AI Music Lab"}

def test_frontend_compat_health():
    response = client.get("/api/health")
    assert response.status_code == 200
