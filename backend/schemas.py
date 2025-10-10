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


class StoryRole(BaseModel):
    """Semantic role in the story (agent, action, location, patient, state)."""
    model_config = ConfigDict(extra='ignore')
    
    role: str  # AGENT, ACTION, LOCATION, PATIENT, STATE
    gloss: str  # English label (e.g., "Fantail", "Fly", "Garden")
    nzsl: str  # NZSL gloss (e.g., "FANTAIL", "FLY", "GARDEN")


class StoryFrame(BaseModel):
    """A single frame/step in the story sequence."""
    model_config = ConfigDict(extra='ignore')
    
    id: int  # Frame number (1, 2, 3...)
    nvpair: List[str]  # Role IDs used in this frame (e.g., ["AGENT", "LOCATION"])
    caption_en: str  # English caption (e.g., "The fantail is in the garden.")
    gloss: str  # NZSL gloss sequence (e.g., "FANTAIL GARDEN")


class StoryScaffold(BaseModel):
    """Complete story structure with roles and frames for sequencing."""
    model_config = ConfigDict(extra='ignore')
    
    theme: str  # Story theme
    roles: List[StoryRole]  # All semantic roles
    frames: List[StoryFrame]  # Sequential story frames


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
    story_scaffold: Optional[StoryScaffold] = None  # New frames-based story structure
