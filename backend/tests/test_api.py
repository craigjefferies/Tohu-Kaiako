from typing import Dict

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_generate_validation() -> None:
    response = client.post("/api/generate_pack", json={"theme": ""})
    assert response.status_code == 422


def test_generate_success(monkeypatch) -> None:
    async def fake_generate_pack(theme: str, level: str, keywords: str, subject: str = "language", activity=None):
        return {
            "pack_id": "pack-test-123",
            "generated_at": "2024-01-01T00:00:00+00:00",
            "theme": theme,
            "language_steps": ["Noun: Nest (NEST)", "Verb: Fly (FLY)", "Location: Forest (FOREST)"],
            "sentence_nzsl": "NEST FLY FOREST",
            "sentence_en": "The Nest flies in the Forest.",
            "teacher_tip": "Show the full scene first so tamariki can anchor WHO, WHAT, and WHERE visually.",
            "pack_content": [
                {
                    "order": 1,
                    "phase": "Whole Scene",
                    "image_role": "scene_intro",
                    "pedagogical_purpose": "Build shared meaning before introducing the target language.",
                    "language_focus": "Ask tamariki what they notice happening in the scene.",
                    "image_description": "Scene prompt",
                    "image_data_url": "https://example.com/scene.png",
                },
                {
                    "order": 2,
                    "phase": "Noun",
                    "image_role": "noun",
                    "pedagogical_purpose": "Isolate the key person or object for clear naming.",
                    "language_focus": "Model NEST.",
                    "image_description": "Noun prompt",
                    "image_data_url": "https://example.com/object.png",
                },
                {
                    "order": 3,
                    "phase": "Verb",
                    "image_role": "verb",
                    "pedagogical_purpose": "Show the action to link meaning, movement, and language.",
                    "language_focus": "Model FLY.",
                    "image_description": "Verb prompt",
                    "image_data_url": "https://example.com/action.png",
                },
                {
                    "order": 4,
                    "phase": "Location",
                    "image_role": "location",
                    "pedagogical_purpose": "Ground the language in place.",
                    "language_focus": "Model FOREST.",
                    "image_description": "Location prompt",
                    "image_data_url": "https://example.com/setting.png",
                },
                {
                    "order": 5,
                    "phase": "Whole Again",
                    "image_role": "scene_review",
                    "pedagogical_purpose": "Recombine WHO, WHAT, WHERE.",
                    "language_focus": "Sign the full sentence together.",
                    "image_description": "Scene prompt",
                    "image_data_url": "https://example.com/scene.png",
                },
            ],
            "scene_images": {
                "object": "https://example.com/object.png",
                "action": "https://example.com/action.png",
                "setting": "https://example.com/setting.png",
                "scene": "https://example.com/scene.png",
            },
        }

    monkeypatch.setattr("backend.app.generate_pack", fake_generate_pack)

    payload: Dict[str, str] = {"theme": "Birds", "level": "ECE", "keywords": ""}
    response = client.post("/api/generate_pack", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["pack_id"] == "pack-test-123"
    assert data["scene_images"]["scene"] == "https://example.com/scene.png"
    assert len(data["pack_content"]) == 5
    assert data["pdf_base64"]  # pdf injected by route
    assert data["sentence_nzsl"] == "NEST FLY FOREST"
