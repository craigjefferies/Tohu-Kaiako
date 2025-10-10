from typing import List, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(..., min_length=2)
    level: str = "ECE"
    keywords: Optional[str] = ""


class NZSLStoryPrompt(BaseModel):
    key_signs: List[str]
    classifiers: List[str]
    facial_expressions: List[str]
    story_outline: List[str]


class Activity(BaseModel):
    category: str
    description: str


class GenerateResponse(BaseModel):
    image_url: str
    nzsl_story_prompt: NZSLStoryPrompt
    activity_web: List[Activity]
