from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    theme: str = Field(..., min_length=2)
    level: str = "ECE"
    keywords: Optional[str] = ""


class NZSLStoryPrompt(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    key_signs: List[str]
    classifiers: List[str]
    facial_expressions: List[str]
    story_outline: List[str]


class Activity(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    category: str
    description: str


class GenerateResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    image_url: str
    nzsl_story_prompt: NZSLStoryPrompt
    activity_web: List[Activity]
