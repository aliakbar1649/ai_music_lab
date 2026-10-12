from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_build_instrumental_prompt_uses_input():
    response = client.post("/api/v1/prompts/build", json={
        "mode": "instrumental",
        "idea": "A peaceful fantasy landscape that gradually becomes emotional",
        "genre": "cinematic orchestral",
        "mood": ["peaceful", "emotional"],
        "instruments": ["piano", "strings"],
        "tempo_bpm": 85,
        "structure": ["soft intro", "gradual build", "emotional climax", "gentle ending"]
    })
    assert response.status_code == 200
    body = response.json()
    assert body["enhancement_method"] == "rule_based"
    assert "85 BPM" in body["prompt"]
    assert "piano, strings" in body["prompt"]
    assert "peaceful fantasy landscape" in body["prompt"]

def test_invalid_tempo_is_rejected():
    response = client.post("/api/v1/prompts/build", json={
        "mode": "vocal", "idea": "A song idea", "tempo_bpm": 500
    })
    assert response.status_code == 422

def test_enhance_is_honest_about_fallback():
    response = client.post("/api/v1/prompts/enhance", json={"prompt": "  Warm piano   and strings "})
    assert response.status_code == 200
    assert response.json()["enhancement_method"] == "rule_based"
    assert "No external AI model" in response.json()["note"]
