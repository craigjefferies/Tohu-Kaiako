import pytest
from backend import llm


@pytest.mark.asyncio
async def test_generate_pack_builds_scene_images(monkeypatch):
    async def fake_call_text(theme: str, level: str, keywords: str, subject: str = "language", activity=None):
        return {
            "nzsl_story_prompt": {
                "key_signs": ["BIRD", "FLY"],
                "classifiers": ["CL:V (bird flying)"],
                "facial_expressions": ["EXCITED"],
                "story_outline": ["Bird flaps", "Bird rests"],
            },
            "activity_web": [],
            "semantic_components": [
                {"type": "object", "label": "Nest", "nzsl_sign": "NEST", "semantic_role": "Where the bird rests"},
                {"type": "action", "label": "Fly", "nzsl_sign": "FLY", "semantic_role": "What the bird does"},
                {"type": "setting", "label": "Forest", "nzsl_sign": "FOREST", "semantic_role": "Where it happens"},
            ],
            "learning_prompts": ["Existing prompt"],
            "language_steps": ["Noun: Nest (NEST)", "Verb: Fly (FLY)", "Location: Forest (FOREST)"],
        }

    async def fake_generate_image(prompt: str, label: str):
        return f"image://{label}"

    monkeypatch.setattr(llm, "call_text", fake_call_text)
    monkeypatch.setattr(llm, "_generate_image", fake_generate_image)

    payload = await llm.generate_pack("Birds", "ECE", "garden")

    assert payload["scene_images"]["scene"] == "image://Birds scene"
    assert payload["scene_images"]["object"] == "image://Birds noun"
    assert payload["pack_content"][0]["phase"] == "Whole Scene"
    assert payload["pack_content"][1]["image_role"] == "noun"
    assert payload["pack_content"][-1]["image_data_url"] == "image://Birds scene"
    assert payload["teacher_tip"]
    assert payload["language_steps"][0].startswith("Noun:")
