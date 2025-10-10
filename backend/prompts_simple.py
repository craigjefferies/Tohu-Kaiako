from typing import Dict, List, Optional


def unified_image_prompt(
    theme: str,
    asset_type: str,
    asset_spec: str,
    scene_seed: int,
) -> str:
    """Simple unified image prompt for all asset types."""
    background = "clean neutral background" if asset_type != "SCENE" else "soft warm background"
    
    return f"""Create a child-safe illustration for ages 3-5.

Theme: {theme}
Type: {asset_type}
Details: {asset_spec}

Style: Flat, friendly, storybook quality (Eric Carle inspired)
Colors: Soft, warm, welcoming
Composition: {background}
Seed: {scene_seed} (for style consistency)

Requirements:
- NO text or labels in image
- Child-safe, joyful, inclusive
- Clear shapes, high contrast
- 1024x1024 PNG"""


def component_image_prompt(theme: str, component_type: str, label: str, nzsl_sign: str, scene_seed: int = 0) -> str:
    """Generate prompt for isolated component."""
    specs = {
        "OBJECT": f"Single {label}, clear view",
        "ACTION": f"{label} in motion",
        "SETTING": f"{label} environment, simple",
        "AGENT": f"Single {label} character, friendly",
        "ATTRIBUTE": f"{label} feeling/quality visual",
    }
    asset_spec = specs.get(component_type.upper(), f"{label}")
    return unified_image_prompt(theme, component_type.upper(), asset_spec, scene_seed)


def scene_image_prompt(theme: str, keywords: str, components: List[Dict[str, str]], scene_seed: int) -> str:
    """Generate prompt for full scene."""
    component_list = ", ".join([c['label'] for c in components])
    asset_spec = f"Scene with: {component_list}. Clear WHO/WHAT/WHERE. Warm, inviting."
    return unified_image_prompt(theme, "SCENE", asset_spec, scene_seed)


def text_system_prompt(theme: str, level: str, keywords: str) -> str:
    """Simplified system prompt for NZSL learning pack - MVP version."""
    return f"""You are an NZSL early childhood curriculum expert for ages 3-5 in Aotearoa NZ.

Create a learning pack for theme: "{theme}"

Return ONLY valid JSON (no markdown, no explanations):

{{
  "nzsl_story_prompt": {{
    "key_signs": ["SIGN1", "SIGN2", "SIGN3"],
    "classifiers": ["CL:B (description)"],
    "facial_expressions": ["Happy", "Curious"],
    "story_outline": ["Step 1", "Step 2", "Step 3"]
  }},
  "story_scaffold": {{
    "theme": "{theme}",
    "roles": [
      {{"role": "AGENT", "gloss": "Character", "nzsl": "SIGN"}},
      {{"role": "ACTION", "gloss": "Action", "nzsl": "SIGN"}},
      {{"role": "LOCATION", "gloss": "Place", "nzsl": "SIGN"}}
    ],
    "frames": [
      {{"id": 1, "nvpair": ["AGENT", "LOCATION"], "caption_en": "Sentence.", "gloss": "SIGN SIGN"}},
      {{"id": 2, "nvpair": ["AGENT", "ACTION"], "caption_en": "Sentence.", "gloss": "SIGN SIGN"}}
    ]
  }},
  "vsd_hotspots": [
    {{"id": "AGENT_1", "role": "AGENT", "label_en": "Character", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.60, "y": 0.35, "w": 0.20, "h": 0.25}}, "teacher_prompt": "WHO?"}},
    {{"id": "LOCATION_1", "role": "LOCATION", "label_en": "Place", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.15, "y": 0.55, "w": 0.35, "h": 0.30}}, "teacher_prompt": "WHERE?"}}
  ],
  "symbol_board": [
    {{"type": "agent", "label_en": "Character", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "image_ref": "agent.png", "alt": "Description", "colour": "orange"}},
    {{"type": "action", "label_en": "Action", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "image_ref": "action.png", "alt": "Description", "colour": "yellow"}}
  ],
  "activity_web": [
    {{"category": "Art", "description": "creative activity"}},
    {{"category": "NZSL Language", "description": "sign language activity"}},
    {{"category": "Maths", "description": "numeracy activity"}},
    {{"category": "Deaf Culture", "description": "cultural awareness activity"}}
  ],
  "semantic_components": [
    {{"type": "agent", "label": "Character", "nzsl_sign": "SIGN", "semantic_role": "Who"}},
    {{"type": "action", "label": "Action", "nzsl_sign": "SIGN", "semantic_role": "What"}},
    {{"type": "setting", "label": "Place", "nzsl_sign": "SIGN", "semantic_role": "Where"}}
  ],
  "learning_prompts": [
    {{"type": "wh_question", "nzsl": "WHO?", "en": "Who do you see?"}},
    {{"type": "wh_question", "nzsl": "WHAT DO?", "en": "What are they doing?"}},
    {{"type": "wh_question", "nzsl": "WHERE?", "en": "Where is this?"}}
  ]
}}

RULES:
- Use authentic NZSL glosses (ALL CAPS)
- 3-5 semantic roles (AGENT, ACTION, LOCATION, PATIENT, STATE)
- Bbox coordinates 0-1 normalized, estimate positions
- Colour coding: orange=agent, yellow=action, green=object, blue=setting, purple=state
- Te reo labels optional (leave "" if unsure)
- Keep it simple, joyful, age-appropriate (3-5 years)
- NZSL-first prompts (not signed English)

Theme: "{theme}"
Context: {keywords if keywords else "General ECE learning"}
""".strip()
