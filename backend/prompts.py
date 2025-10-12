from typing import Dict, List, Optional


def unified_image_prompt(theme: str, role: str, detail: str, seed: int) -> str:
    """
    Unified prompt prioritising semantic clarity for NZSL learning assets.
    """
    role_upper = role.upper()
    
    base = (
        "Make the meaning obvious for tamariki aged 3–5. "
        "Keep the style calm, inclusive, and storybook simple. No text. "
        "Ground everything in everyday Aotearoa New Zealand experiences (local flora/fauna, classrooms, whānau life) so it feels familiar."
    )
    
    semantic_guidance = {
        "OBJECT": "Show the main thing we are naming by itself so learners can clearly see what it is.",
        "AGENT": "Show the main person/character by themselves so learners can clearly see who it is.",
        "ACTION": "Show the same subject performing the action so learners understand what it does.",
        "SETTING": "Show where it happens without changing who the character is.",
        "LOCATION": "Show where it happens without changing who the character is.",
        "SCENE": "Bring the subject, action, and place together in one picture that tells a short story.",
    }
    
    granular_control = {
        "OBJECT": "Single isolated subject, neutral background, clear shapes. Keep proportions child-friendly and recognisable.",
        "AGENT": "Single isolated subject, neutral background, clear shapes. Keep proportions child-friendly and recognisable.",
        "ACTION": "Same subject in motion, clean neutral background. Freeze a mid-action pose that reads instantly.",
        "SETTING": "Environment cues, soft warm background with depth. Use real Aotearoa details (e.g., pōhutukawa, kiwiana).",
        "LOCATION": "Environment cues, soft warm background with depth. Use real Aotearoa details (e.g., pōhutukawa, kiwiana).",
        "SCENE": "Combine subject, action, and place. Keep characters consistent and interactions clear.",
    }
    
    semantic_text = semantic_guidance.get(role_upper, semantic_guidance["OBJECT"])
    control_text = granular_control.get(role_upper, granular_control["OBJECT"])
    
    return (
        f"{base}\n"
        f"Theme: {theme}\n"
        f"Role: {role_upper}\n"
        f"Semantic clarity: {semantic_text}\n"
        f"Instructions: {control_text} {detail}\n"
        f"Image format: 1024x1024 PNG\n"
        f"Seed: {seed}"
    )


def component_image_prompt(theme: str, component_type: str, label: str, nzsl_sign: str, scene_seed: int = 0) -> str:
    """Generate prompt for isolated component."""
    specs = {
        "OBJECT": f"{label} (NZSL: {nzsl_sign}) clearly visible",
        "ACTION": f"{label} action showing motion (NZSL: {nzsl_sign})",
        "SETTING": f"{label} location cues (NZSL: {nzsl_sign})",
        "AGENT": f"{label} character, warm expression (NZSL: {nzsl_sign})",
        "ATTRIBUTE": f"{label} feeling or quality (NZSL: {nzsl_sign})",
    }
    role = component_type.upper()
    detail = specs.get(role, f"{label} (NZSL: {nzsl_sign})")
    return unified_image_prompt(theme, role, detail, scene_seed)


def scene_image_prompt(theme: str, keywords: str, components: List[Dict[str, str]], scene_seed: int) -> str:
    """Generate prompt for full scene."""
    component_list = ", ".join([c['label'] for c in components])
    detail = f"Include: {component_list}. Keep WHO/WHAT/WHERE clear and welcoming."
    if keywords:
        detail += f" Context keywords: {keywords}."
    return unified_image_prompt(theme, "SCENE", detail, scene_seed)


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
  "language_steps": [
    "Noun: NAME the key person or object (use AGENT/OBJECT)",
    "Verb: TELL the action that happens (use ACTION)",
    "Location: SHOW where it happens (use LOCATION/SETTING)"
  ],
  "learning_prompts": [
    "Name the noun first.",
    "Add the verb next.",
    "Finish with where it happens."
  ]
}}

RULES:
- Use authentic NZSL glosses (ALL CAPS)
- 3-5 semantic roles (AGENT, ACTION, LOCATION, PATIENT, STATE)
- language_steps must be exactly 3 strings ordered: Noun, Verb, Location (each include theme-specific words)
- Bbox coordinates 0-1 normalized, estimate positions
- Colour coding: orange=agent, yellow=action, green=object, blue=setting, purple=state
- Te reo labels optional (leave "" if unsure)
- Keep it simple, joyful, age-appropriate (3-5 years)
- NZSL-first prompts (not signed English)

Theme: "{theme}"
Context: {keywords if keywords else "General ECE learning"}
""".strip()
