from typing import Any, Dict

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_generate_validation() -> None:
    response = client.post("/api/generate_pack", json={"theme": ""})
    assert response.status_code == 422


def test_generate_success(monkeypatch) -> None:
    async def fake_generate_pack(theme: str, level: str, keywords: str):
        return (
            {
                "nzsl_story_prompt": {
                    "key_signs": ["BIRD"],
                    "classifiers": ["CL:V"],
                    "facial_expressions": ["HAPPY"],
                    "story_outline": ["Step 1", "Step 2"],
                },
                "activity_web": [
                    {"category": "Art", "description": "Draw"},
                    {"category": "NZSL Language", "description": "Sign"},
                    {"category": "Maths", "description": "Count"},
                    {"category": "Deaf Culture", "description": "Discuss"},
                ],
                "semantic_components": [
                    {"type": "object", "label": "Nest", "nzsl_sign": "NEST", "semantic_role": "Where the bird rests"},
                    {"type": "action", "label": "Fly", "nzsl_sign": "FLY", "semantic_role": "What the bird does"},
                    {"type": "setting", "label": "Forest", "nzsl_sign": "FOREST", "semantic_role": "Where it happens"},
                ],
            },
            {
                "object": "https://example.com/object.png",
                "action": "https://example.com/action.png",
                "setting": "https://example.com/setting.png",
                "scene": "https://example.com/scene.png",
            },
        )

    monkeypatch.setattr("backend.app.generate_pack", fake_generate_pack)

    payload: Dict[str, Any] = {"theme": "Birds", "level": "ECE", "keywords": ""}
    response = client.post("/api/generate_pack", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["image_url"] == "https://example.com/scene.png"
    assert data["scene_images"]["object"] == "https://example.com/object.png"
    assert len(data["activity_web"]) == 4
    assert data["nzsl_story_prompt"]["key_signs"] == ["BIRD"]
