from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    theme: str = Field(..., min_length=2)
    level: str = "ECE"
    keywords: Optional[str] = ""
    subject: str = "language"
    activity: Optional[str] = None


class PackContentItem(BaseModel):
    """Single phase in the Whole–Part–Whole sequence."""
    model_config = ConfigDict(extra='ignore')
    
    phase: str
    image_role: str
    pedagogical_purpose: str
    language_focus: str
    image_description: str
    image_data_url: Optional[str] = None
    order: int = 0


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


class BBox(BaseModel):
    """Bounding box with normalized coordinates (0-1) for hotspot positioning."""
    model_config = ConfigDict(extra='ignore')
    
    x: float  # Left position (0-1)
    y: float  # Top position (0-1)
    w: float  # Width (0-1)
    h: float  # Height (0-1)


class VSDHotspot(BaseModel):
    """Visual Scene Display hotspot for interactive questioning."""
    model_config = ConfigDict(extra='ignore')
    
    id: str  # Unique ID (e.g., "AGENT_1", "ACTION_1")
    role: str  # Semantic role: AGENT, ACTION, LOCATION, PATIENT, STATE
    label_en: str  # English label (e.g., "Fantail")
    label_te_reo: str = ""  # Te reo Māori label (e.g., "Pīwakawaka")
    nzsl_gloss: str  # NZSL gloss (e.g., "FANTAIL")
    bbox: BBox  # Bounding box coordinates
    teacher_prompt: str  # Scaffolding question (e.g., "WHO is here?")


class SymbolCard(BaseModel):
    """Symbol card for Colourful Semantics-based learning."""
    model_config = ConfigDict(extra='ignore')
    
    type: str  # agent, action, object, setting, state
    label_en: str  # English label
    label_te_reo: str = ""  # Te reo Māori label
    nzsl_gloss: str  # NZSL gloss
    image_ref: str  # Reference to component image (filename or data URI)
    alt: str  # Alt text for accessibility
    colour: str  # Colourful Semantics color: orange, yellow, green, blue, purple


class ExportOptions(BaseModel):
    """Export configuration for PDF and HTML outputs."""
    model_config = ConfigDict(extra='ignore')
    
    pdf: Optional[dict] = None  # PDF export settings
    html_offline: Optional[dict] = None  # HTML export settings
    json_data: Optional[dict] = None  # JSON data export settings


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
    
    pack_id: str
    generated_at: str
    theme: str
    language_steps: List[str] = []
    sentence_nzsl: str
    sentence_en: str
    teacher_tip: str
    pack_content: List[PackContentItem]
    scene_images: Optional[SceneImages] = None
    pdf_base64: Optional[str] = None
