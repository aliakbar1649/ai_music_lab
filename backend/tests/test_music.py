from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_music_generation_is_not_fake():
    response = client.post("/api/v1/music/generations")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "MUSIC_PROVIDER_NOT_CONFIGURED"
