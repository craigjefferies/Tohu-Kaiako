from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    theme: str = Field(..., min_length=2)
    level: str = "ECE"
    keywords: Optional[str] = ""


class SemanticComponent(BaseModel):
    """Represents a single semantic element in the scene."""
    model_config = ConfigDict(extra='ignore')
    
    type: str  # agent, action, object, setting, attribute
    label: str  # e.g., "Boy", "Eat", "Apple", "Kitchen"
    nzsl_sign: str  # e.g., "BOY", "EAT", "APPLE", "KITCHEN"
    semantic_role: str  # e.g., "Who is doing the action", "What is happening"


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


class SceneImages(BaseModel):
    """Collection of generated imagery to scaffold scene-based storytelling."""
    model_config = ConfigDict(extra='ignore')
    
    object: str
    action: str
    setting: str
    scene: str


class GenerateResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    image_url: str
    nzsl_story_prompt: NZSLStoryPrompt
    activity_web: List[Activity]
    semantic_components: List[SemanticComponent] = []
    learning_prompts: List[str] = []
    scene_images: SceneImages
