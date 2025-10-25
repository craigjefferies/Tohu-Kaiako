from typing import Dict, List, Optional

def unified_image_prompt(theme: str, role: str, detail: str, seed: int) -> str:
    """
    Unified prompt prioritising semantic clarity for NZSL learning assets.
    """
    role_upper = role.upper()
    
    base = (
        "Make the meaning obvious for tamariki aged 3–5. "
        "Keep the style calm, inclusive, and storybook-simple. No text. "
        "Ground everything in everyday Aotearoa New Zealand experiences (local flora/fauna, classrooms, whānau life) so it feels familiar."
    )
    # Additional style/consistency cues
    style_closure = (
        "Use large, friendly characters or objects, bold yet soft outlines, warm daylight lighting, "
        "bright but gentle colour palette, minimal background clutter. "
        "Ensure the same character/object style is used across related images."
    )

    semantic_guidance = {
        "OBJECT":    "Show the main thing we are naming by itself so learners can clearly see what it is.",
        "AGENT":     "Show the main person/character by themselves so learners can clearly see who it is.",
        "ACTION":    "Show the same subject performing the action so learners understand what it does.",
        "SETTING":   "Show where it happens without changing who the character is.",
        "LOCATION":  "Show where it happens without changing who the character is.",
        "SCENE":     "Bring the subject, action, and place together in one picture that tells a short story.",
    }
    granular_control = {
        "OBJECT":    "Single isolated subject, neutral/simple background, clear shapes, child-friendly proportions and recognisable features.",
        "AGENT":     "Single isolated subject, neutral/simple background, clear shapes, child-friendly proportions and recognisable features.",
        "ACTION":    "Same subject in motion, clean neutral background, freeze a mid-action pose that reads instantly, child-friendly view.",
        "SETTING":   "Environment cues only, soft warm background with depth, include identifiable Aotearoa NZ details (e.g., pōhutukawa, flax, backyard, beach).",
        "LOCATION":  "Environment cues only, soft warm background with depth, include identifiable Aotearoa NZ details (e.g., pōhutukawa, flax, backyard, beach).",
        "SCENE":     "Combine subject + action + place. Keep characters/objects consistent, interactions clear, scene simple and readable for young children.",
    }
    
    semantic_text = semantic_guidance.get(role_upper, semantic_guidance["OBJECT"])
    control_text  = granular_control.get(role_upper, granular_control["OBJECT"])
    
    prompt = (
        f"{base} {style_closure}\n"
        f"Theme: {theme}\n"
        f"Role: {role_upper}\n"
        f"Semantic clarity: {semantic_text}\n"
        f"Instructions: {control_text} {detail}\n"
        f"Image format: 1024×1024 PNG (transparent background if needed)\n"
        f"Seed: {seed}"
    )
    return prompt

def component_image_prompt(theme: str, component_type: str, label: str, nzsl_sign: str, scene_seed: int = 0) -> str:
    """Generate prompt for isolated component (noun/agent/action/setting)."""
    specs = {
        "OBJECT":   f"{label} (NZSL: {nzsl_sign}) clearly visible",
        "ACTION":   f"{label} action showing motion (NZSL: {nzsl_sign})",
        "SETTING":  f"{label} location cues for {label} (NZSL: {nzsl_sign})",
        "LOCATION": f"{label} location cues for {label} (NZSL: {nzsl_sign})",
        "AGENT":    f"{label} character, warm expression (NZSL: {nzsl_sign})",
        "ATTRIBUTE":f"{label} feeling or quality (NZSL: {nzsl_sign})",
    }
    role   = component_type.upper()
    detail = specs.get(role, f"{label} (NZSL: {nzsl_sign})")
    return unified_image_prompt(theme, role, detail, scene_seed)

def scene_image_prompt(theme: str, keywords: str, components: List[Dict[str, str]], scene_seed: int) -> str:
    """Generate prompt for full scene (noun+verb+where)."""
    component_list = ", ".join([c['label'] for c in components])
    detail = f"Include: {component_list}. Keep WHO/WHAT/WHERE clear and welcoming."
    if keywords:
        detail += f" Context keywords: {keywords}."
    return unified_image_prompt(theme, "SCENE", detail, scene_seed)

def text_system_prompt(theme: str, level: str, keywords: str, subject: str = "language", activity: Optional[str] = None) -> str:
    """Simplified system prompt for NZSL learning pack – MVP version."""
    
    if subject == "math" and activity == "name_the_number":
        return f"""You are an NZSL early childhood mathematics curriculum expert for ages 3-5 in Aotearoa NZ.

Create a mathematics learning pack for theme: "{theme}" with activity: "Name the number"

Return ONLY valid JSON (no markdown, no explanations):

{{
  "nzsl_story_prompt": {{
    "key_signs": ["NUMBER", "THEME_SIGN", "COUNT"],
    "classifiers": ["CL:B (group of objects)"],
    "facial_expressions": ["Excited", "Focused"],
    "story_outline": ["Show the number", "Name the objects", "Count together"]
  }},
  "story_scaffold": {{
    "theme": "{theme}",
    "roles": [
      {{"role": "NUMBER",   "gloss": "Number", "nzsl": "NUMBER_SIGN"}},
      {{"role": "OBJECT",   "gloss": "{theme}", "nzsl": "THEME_SIGN"}},
      {{"role": "SETTING",  "gloss": "Place",  "nzsl": "PLACE"}}
    ],
    "frames": [
      {{"id": 1, "nvpair": ["NUMBER","OBJECT"], "caption_en": "There are X {theme}.", "gloss": "NUMBER THEME_SIGN"}},
      {{"id": 2, "nvpair": ["OBJECT","SETTING"], "caption_en": "The {theme} are in the place.", "gloss": "THEME_SIGN PLACE"}}
    ]
  }},
  "vsd_hotspots": [
    {{"id": "NUMBER_1",  "role": "NUMBER", "label_en": "Number", "label_te_reo": "", "nzsl_gloss": "NUMBER",
      "bbox": {{"x": 0.10, "y": 0.10, "w": 0.20, "h": 0.20}}, "teacher_prompt": "WHAT NUMBER?"}},
    {{"id": "OBJECT_1",  "role": "OBJECT", "label_en": "{theme}", "label_te_reo": "", "nzsl_gloss": "THEME_SIGN",
      "bbox": {{"x": 0.40, "y": 0.40, "w": 0.30, "h": 0.30}}, "teacher_prompt": "WHAT OBJECTS?"}}
  ],
  "symbol_board": [
    {{"type": "number", "label_en": "Number", "label_te_reo": "", "nzsl_gloss": "NUMBER",
      "image_ref": "number.png", "alt": "Number symbol", "colour": "blue"}},
    {{"type": "object", "label_en": "{theme}", "label_te_reo": "", "nzsl_gloss": "THEME_SIGN",
      "image_ref": "object.png", "alt": "Object symbol", "colour": "green"}}
  ],
  "activity_web": [
    {{"category": "Maths",          "description": "counting activity with {theme}"}},
    {{"category": "NZSL Language",  "description": "number signs practice"}},
    {{"category": "Art",            "description": "draw and count {theme}"}},
    {{"category": "Deaf Culture",   "description": "cultural number stories"}}
  ],
  "semantic_components": [
    {{"type": "number", "label": "Number", "nzsl_sign": "NUMBER_SIGN", "semantic_role": "How many"}},
    {{"type": "object", "label": "{theme}", "nzsl_sign": "THEME_SIGN", "semantic_role": "What"}},
    {{"type": "setting", "label": "Place", "nzsl_sign": "PLACE", "semantic_role": "Where"}}
  ],
  "language_steps": [
    "Number: SHOW the quantity (use NUMBER)",
    "Object: NAME what is being counted (use OBJECT)",
    "Count: DEMONSTRATE counting the {theme}"
  ],
  "learning_prompts": [
    "Show the number first.",
    "Name the objects next.",
    "Count them together."
  ],
  "math_details": {{
    "number": 3,
    "operation": "counting",
    "focus": "number identification"
  }}
}}

RULES:
- Choose a number between 1-10 appropriate for {level} level (ECE: 1-5, Junior Primary: 1-10)
- Use authentic NZSL number signs (e.g., ONE, TWO, THREE...)
- semantic_components must include number, object, setting
- language_steps must be exactly 3 strings focused on number identification
- Bbox coordinates are normalized 0-1, estimate positions visually
- Colour coding: blue=number, green=object, purple=setting
- Keep it simple, joyful, age-appropriate (ages 3-5)
- NZSL-first prompts for numbers and counting

Theme: "{theme}"
Context: {keywords if keywords else "Mathematics counting activity"}
Subject: {subject}
Activity: {activity}
""".strip()
    
    # Default language prompt
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
      {{"role": "AGENT",    "gloss": "Character", "nzsl": "SIGN"}},
      {{"role": "ACTION",   "gloss": "Action",    "nzsl": "SIGN"}},
      {{"role": "LOCATION", "gloss": "Place",     "nzsl": "SIGN"}}
    ],
    "frames": [
      {{"id": 1, "nvpair": ["AGENT","LOCATION"], "caption_en": "Sentence.", "gloss": "SIGN SIGN"}},
      {{"id": 2, "nvpair": ["AGENT","ACTION"],   "caption_en": "Sentence.", "gloss": "SIGN SIGN"}}
    ]
  }},
  "vsd_hotspots": [
    {{"id": "AGENT_1",   "role": "AGENT",    "label_en": "Character", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.60, "y": 0.35, "w": 0.20, "h": 0.25}}, "teacher_prompt": "WHO?"}},
    {{"id": "LOCATION_1","role": "LOCATION", "label_en": "Place",     "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.15, "y": 0.55, "w": 0.35, "h": 0.30}}, "teacher_prompt": "WHERE?"}}
  ],
  "symbol_board": [
    {{"type": "agent",  "label_en": "Character", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "image_ref": "agent.png",      "alt": "Description", "colour": "orange"}},
    {{"type": "action", "label_en": "Action",    "label_te_reo": "", "nzsl_gloss": "SIGN",
      "image_ref": "action.png",     "alt": "Description", "colour": "yellow"}}
  ],
  "activity_web": [
    {{"category": "Art",            "description": "creative activity"}},
    {{"category": "NZSL Language",  "description": "sign-language activity"}},
    {{"category": "Maths",          "description": "numeracy activity"}},
    {{"category": "Deaf Culture",   "description": "cultural awareness activity"}}
  ],
  "semantic_components": [
    {{"type": "agent",   "label": "Character", "nzsl_sign": "SIGN", "semantic_role": "Who"}},
    {{"type": "action",  "label": "Action",    "nzsl_sign": "SIGN", "semantic_role": "What"}},
    {{"type": "setting", "label": "Place",     "nzsl_sign": "SIGN", "semantic_role": "Where"}}
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
- 3-5 semantic roles (AGENT, ACTION, LOCATION, PATIENT, STATE) exactly
- language_steps must be exactly 3 strings ordered: Noun, Verb, Location (each include theme-specific words)
- Bbox coordinates are normalized 0-1, estimate positions visually
- Colour coding: orange=agent, yellow=action, green=object, blue=setting, purple=state
- Te reo labels optional (leave "" if unsure)
- Keep it simple, joyful, age-appropriate (ages 3-5)
- NZSL-first prompts (not Signed English)
- Style & consistency cues: same character/object style across all images, bold outlines, warm daylight, bright but soft palette

Theme: "{theme}"
Context: {keywords if keywords else "General ECE learning"}
Subject: {subject}
Activity: {activity if activity else "General"}
""".strip()

