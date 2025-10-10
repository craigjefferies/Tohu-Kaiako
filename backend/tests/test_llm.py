import json

import pytest
import respx
from httpx import Response

from backend import llm


@pytest.mark.asyncio
@respx.mock
async def test_generate_pack_makes_parallel_requests():
    text_route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "nzsl_story_prompt": {
                                        "key_signs": ["BIRD"],
                                        "classifiers": ["CL:V"],
                                        "facial_expressions": ["HAPPY"],
                                        "story_outline": ["Start", "End"],
                                    },
                                    "activity_web": [
                                        {"category": "Art", "description": "Paint"},
                                        {"category": "NZSL Language", "description": "Sign"},
                                        {"category": "Maths", "description": "Count"},
                                        {"category": "Deaf Culture", "description": "Discuss"},
                                    ],
                                }
                            )
                        }
                    }
                ]
            },
        )
    )

    image_route = respx.post("https://openrouter.ai/api/v1/images").mock(
        return_value=Response(200, json={"data": [{"url": "https://example.com/image.png"}]})
    )

    data, image_url = await llm.generate_pack("Birds", "ECE", "garden")

    assert text_route.called
    assert image_route.called
    assert image_url == "https://example.com/image.png"
    assert data["nzsl_story_prompt"]["key_signs"] == ["BIRD"]
