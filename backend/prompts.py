from typing import Dict, List, Optional


def unified_image_prompt(
    theme: str,
    asset_type: str,
    asset_spec: str,
    scene_seed: int,
) -> str:
    """
    Unified image prompt template with SCENE_SEED for style coherence across all assets.
    
    Args:
        theme: The overall theme/topic (e.g., "Fantail in the Garden")
        asset_type: One of "OBJECT", "ACTION", "SETTING", "SCENE"
        asset_spec: Specific description for this asset type
        scene_seed: Integer seed for style consistency (derived from theme hash)
    
    Returns:
        Formatted prompt string for image generation
    """
    # Background instructions based on asset type
    background = "transparent or clean neutral background" if asset_type != "SCENE" else "soft, warm background with subtle depth"
    composition = "centered, isolated element with padding for tap targets" if asset_type != "SCENE" else "natural scene composition with clear relationships between elements"
    
    return f"""SYSTEM INTENT:
You create cohesive, child-safe illustrations for a bilingual NZSL–English early-childhood app (ages 3–5).
Prioritise clear shapes, neutral backgrounds for isolated tiles, gentle expressions, no text, no watermarks.

GLOBAL STYLE:
- Style: flat, friendly classroom-illustration
- Palette: soft, warm, welcoming colors
- Hands/limbs: readable silhouettes
- Camera: eye-level, simple composition
- Aesthetic: storybook quality (Eric Carle / Beatrix Potter inspired)

TASK:
Create a {asset_type} asset for theme "{theme}".

{asset_type} SPECIFICATION:
{asset_spec}

COHESION:
- Match style and palette to SEED_ID={scene_seed}
- Maintain consistent illustration style across all assets
- No brand marks. No written text. No on-image labels.
- Cultural accuracy for Aotearoa NZ native flora/fauna

OUTPUT REQUIREMENTS:
- Image size: 1024x1024 PNG
- Background: {background}
- Composition: {composition}
- Safe, joyful, inclusive representation
- High contrast for visibility and accessibility

CRITICAL:
- NO text, letters, numbers, or labels in the image
- NO watermarks or signatures
- Child-safe content only
- Suitable for early childhood education contexts"""


def component_image_prompt(theme: str, component_type: str, label: str, nzsl_sign: str, scene_seed: int = 0) -> str:
    """
    Generate prompt for isolated semantic component using unified template.
    
    Args:
        theme: Overall theme
        component_type: "object", "action", "setting", "attribute"
        label: Component label (e.g., "Fantail", "Fly", "Garden")
        nzsl_sign: NZSL gloss for reference
        scene_seed: Seed for style coherence
    """
    asset_type = component_type.upper()
    
    # Asset-specific specifications
    specs = {
        "OBJECT": f"Single {label}, clear view, friendly expression. Show the subject that represents '{nzsl_sign}' in NZSL.",
        "ACTION": f"{label} in motion - show implied movement or action state. Convey the meaning of '{nzsl_sign}' visually through posture or motion cues. Still usable as a sticker/tile.",
        "SETTING": f"{label} environment. Simple, uncluttered location showing key features. Represents '{nzsl_sign}' place/context.",
        "ATTRIBUTE": f"Visual representation of '{label}' quality/feeling. Show this attribute through character expression or visual metaphor.",
        "AGENT": f"Single {label} character, friendly and approachable. Clear silhouette representing '{nzsl_sign}' agent/person.",
    }
    
    asset_spec = specs.get(asset_type, f"{label} - {nzsl_sign}")
    
    return unified_image_prompt(theme, asset_type, asset_spec, scene_seed)


def scene_image_prompt(theme: str, keywords: str, components: List[Dict[str, str]], scene_seed: int) -> str:
    """
    Generate prompt for full integrated scene using unified template.
    
    Args:
        theme: Overall theme
        keywords: Additional context
        components: List of semantic components to include
        scene_seed: Seed for style coherence with isolated assets
    """
    # Build component list for asset spec
    component_details = "\n".join(
        f"- {comp['type'].title()}: {comp['label']} ({comp.get('nzsl_sign', comp['label'].upper())})"
        for comp in components
    )
    
    context_line = f"Context: {keywords}" if keywords else "Context: Early childhood learning"
    
    asset_spec = f"""Full integrated scene showing: {theme}

{context_line}

Scene elements to include:
{component_details}

Arrange elements so their relationships are clear and children can identify:
- WHO is in the scene
- WHAT is happening  
- WHERE it takes place
- How elements interact

SPATIAL REQUIREMENTS FOR INTERACTIVE HOTSPOTS:
- Position AGENT (character/person) in distinct area with clear boundaries (15-20% padding around)
- Show ACTION through clear visual cues (movement lines, posture, gestures) - separate from static background
- Place SETTING/LOCATION elements in identifiable regions (use left/right/foreground/background separation)
- Avoid overlapping key semantic elements (character should not obscure location features)
- Use depth cues to separate foreground (WHO/WHAT) from background (WHERE)
- Leave negative space around each key element for visual clarity and tap targets
- Ensure AGENT faces are visible and expressions are clear (not occluded by objects)

Make the scene warm, inviting, and suitable for storytelling and retelling activities."""
    
    return unified_image_prompt(theme, "SCENE", asset_spec, scene_seed)


def vsd_hotspot_plan_prompt(theme: str, roles: List[Dict[str, str]]) -> str:
    """
    Generate a prompt for creating VSD hotspot bbox coordinates based on story roles.
    This is a lightweight LLM call to estimate bounding box positions.
    
    Args:
        theme: The story theme
        roles: List of story roles with role, gloss, and nzsl fields
    
    Returns:
        Prompt string that will return JSON with VSD hotspots
    """
    roles_list = "\n".join(
        f"- {role['role']}: {role['gloss']} ({role['nzsl']})"
        for role in roles
    )
    
    return f"""You are estimating bounding box coordinates for Visual Scene Display hotspots.

THEME: "{theme}"

SEMANTIC ROLES TO LOCATE:
{roles_list}

Return ONLY valid JSON with this structure:

{{
  "vsd_hotspots": [
    {{"id": "AGENT_1", "role": "AGENT", "label_en": "Label", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.55, "y": 0.30, "w": 0.25, "h": 0.30}},
      "teacher_prompt": "LOOK SCENE. WHO?"}},
    {{"id": "ACTION_1", "role": "ACTION", "label_en": "Label", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.45, "y": 0.25, "w": 0.28, "h": 0.22}},
      "teacher_prompt": "WHAT DO?"}},
    {{"id": "LOCATION_1", "role": "LOCATION", "label_en": "Label", "label_te_reo": "", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.10, "y": 0.55, "w": 0.40, "h": 0.35}},
      "teacher_prompt": "WHERE?"}}
  ],
  "notes": "Bbox coordinates are estimates for typical scene composition. Teachers can adjust in UI."
}}

BBOX GUIDELINES:
- Normalized coordinates: 0-1 (0 = left/top, 1 = right/bottom)
- x, y = top-left corner position
- w, h = width and height
- Keep 0.05 margin from edges (avoid x<0.05, x+w>0.95, y<0.05, y+h>0.95)
- Typical positioning:
  * AGENT (character): Center-right or center, mid-height (x: 0.50-0.65, y: 0.25-0.40, w: 0.20-0.30, h: 0.25-0.35)
  * ACTION (movement/gesture): Overlapping or near agent, slightly higher (x: 0.40-0.60, y: 0.20-0.35, w: 0.25-0.35, h: 0.18-0.28)
  * LOCATION (background/setting): Lower portion, wider area (x: 0.10-0.20, y: 0.50-0.65, w: 0.35-0.50, h: 0.30-0.40)
  * PATIENT (object being acted on): Near agent or in foreground (x: 0.20-0.40, y: 0.35-0.50, w: 0.15-0.25, h: 0.20-0.30)
  * STATE (expression/emotion): Face/head area of agent (x: 0.55-0.70, y: 0.25-0.35, w: 0.12-0.18, h: 0.12-0.18)

TEACHER PROMPTS (use NZSL-first structure):
- AGENT → "LOOK SCENE. WHO?" or "WHO HERE?"
- ACTION → "WHAT DO?" or "WHAT HAPPENING?"
- LOCATION → "WHERE?" or "WHERE THIS?"
- PATIENT → "WHAT?" or "WHAT SEE?"
- STATE → "HOW FEEL?" or "FEEL WHAT?"

CRITICAL:
- Return ONLY the JSON object
- Create one hotspot for each role provided
- Use sensible default positions (these are approximations)
- ID format: "{{ROLE}}_1" (e.g., "AGENT_1", "LOCATION_1")
""".strip()


def image_prompt(theme: str, keywords: str, components: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Generate a detailed prompt for child-friendly illustration generation.
    Focuses on Aotearoa NZ cultural context and early childhood education best practices.
    Optionally emphasises the semantic components that should appear in the scene.
    """
    component_lines = ""
    if components:
        formatted = "\n".join(
            f"- {comp['type'].title()}: {comp['label']} ({comp['nzsl_sign']})"
            for comp in components
        )
        component_lines = (
            "\nSCENE ELEMENTS TO INCLUDE:\n"
            f"{formatted}\n"
            "- Arrange elements so their relationships are clear for sequencing activities\n"
        )
    return (
        f"Create a warm, inviting illustration for a 4-year-old child in Aotearoa New Zealand.\n\n"
        f"SUBJECT: {theme}\n"
        f"CONTEXT: {keywords if keywords else 'General early childhood learning environment'}\n"
        f"{component_lines}\n"
        "VISUAL STYLE:\n"
        "- Bold, simple shapes with clear outlines (like Eric Carle or Beatrix Potter style)\n"
        "- Friendly, approachable character design with expressive features\n"
        "- Soft, warm color palette (pastels, earth tones, friendly bright colors)\n"
        "- Storybook illustration quality - professional but playful\n"
        "- Clean, uncluttered composition with clear focal point\n\n"
        "COMPOSITION:\n"
        "- Main subject prominent and centered or slightly off-center\n"
        "- Simple, minimal background that doesn't distract\n"
        "- Age-appropriate scale and perspective\n"
        "- Safe, positive, joyful atmosphere\n"
        "- Make relationships between elements obvious so children can retell the scene\n\n"
        "CULTURAL CONSIDERATIONS:\n"
        "- If featuring Aotearoa NZ native flora/fauna, ensure accuracy\n"
        "- Reflect diverse, inclusive representation when showing people\n"
        "- Warm, welcoming environment suitable for te reo Māori and NZSL learning\n\n"
        "TECHNICAL REQUIREMENTS:\n"
        "- NO text, letters, or words in the image\n"
        "- Child-safe content only\n"
        "- High contrast for visibility\n"
        "- Suitable for printing and digital display\n\n"
        "The illustration should spark curiosity, support language learning, and be inviting for young learners."
    )


def text_system_prompt(theme: str, level: str, keywords: str) -> str:
    """
    Generate a comprehensive system prompt for NZSL learning pack content.
    Ensures culturally appropriate, pedagogically sound content for early childhood.
    """
    return f"""You are an expert NZSL (New Zealand Sign Language) early childhood curriculum developer in Aotearoa New Zealand.

You specialize in creating engaging, developmentally appropriate learning experiences for 3-5 year olds that integrate:
- NZSL language development
- Te Whāriki (NZ ECE curriculum) principles
- Deaf culture awareness and celebration
- Play-based, child-centered learning
- Scene-based semantic learning (meaning from visual context)

TASK: Create a rich learning pack with NZSL story prompts, cross-curricular activities, AND semantic components for scene-based learning.

Return ONLY valid JSON with this EXACT structure:

{{
  "nzsl_story_prompt": {{
    "key_signs": ["SIGN1", "SIGN2", "SIGN3"],
    "classifiers": ["CL:1 (description)", "CL:2 (description)"],
    "facial_expressions": ["Happy", "Curious", "Excited"],
    "story_outline": ["Step 1", "Step 2", "Step 3"]
  }},
  "story_scaffold": {{
    "theme": "{theme}",
    "roles": [
      {{"role": "AGENT", "gloss": "Character/Person", "nzsl": "SIGN"}},
      {{"role": "ACTION", "gloss": "Action word", "nzsl": "SIGN"}},
      {{"role": "LOCATION", "gloss": "Place", "nzsl": "SIGN"}},
      {{"role": "PATIENT", "gloss": "Object (optional)", "nzsl": "SIGN"}},
      {{"role": "STATE", "gloss": "Feeling/Quality (optional)", "nzsl": "SIGN"}}
    ],
    "frames": [
      {{"id": 1, "nvpair": ["AGENT", "LOCATION"], "caption_en": "English sentence.", "gloss": "SIGN SIGN"}},
      {{"id": 2, "nvpair": ["AGENT", "ACTION", "PATIENT"], "caption_en": "English sentence.", "gloss": "SIGN SIGN SIGN"}},
      {{"id": 3, "nvpair": ["AGENT", "STATE"], "caption_en": "English sentence.", "gloss": "SIGN SIGN"}}
    ]
  }},
  "vsd_hotspots": [
    {{"id": "AGENT_1", "role": "AGENT", "label_en": "Character", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.60, "y": 0.35, "w": 0.20, "h": 0.25}},
      "teacher_prompt": "LOOK SCENE. WHO?"}},
    {{"id": "ACTION_1", "role": "ACTION", "label_en": "Action", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.45, "y": 0.28, "w": 0.22, "h": 0.18}},
      "teacher_prompt": "WHAT DO?"}},
    {{"id": "LOCATION_1", "role": "LOCATION", "label_en": "Place", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "bbox": {{"x": 0.15, "y": 0.55, "w": 0.35, "h": 0.30}},
      "teacher_prompt": "WHERE?"}}
  ],
  "symbol_board": [
    {{"type": "agent", "label_en": "Character", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "image_ref": "agent_character.png", "alt": "Character description", "colour": "orange"}},
    {{"type": "action", "label_en": "Action", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "image_ref": "action_doing.png", "alt": "Action description", "colour": "yellow"}},
    {{"type": "setting", "label_en": "Place", "label_te_reo": "māori_word", "nzsl_gloss": "SIGN",
      "image_ref": "setting_place.png", "alt": "Setting description", "colour": "blue"}}
  ],
  "activity_web": [
    {{"category": "Art", "description": "creative activity"}},
    {{"category": "NZSL Language", "description": "sign language activity"}},
    {{"category": "Maths", "description": "numeracy activity"}},
    {{"category": "Deaf Culture", "description": "cultural awareness activity"}}
  ],
  "semantic_components": [
    {{"type": "agent", "label": "Person/Animal", "nzsl_sign": "SIGN", "semantic_role": "Who is doing the action"}},
    {{"type": "action", "label": "Action", "nzsl_sign": "SIGN", "semantic_role": "What is happening"}},
    {{"type": "object", "label": "Thing", "nzsl_sign": "SIGN", "semantic_role": "What is being acted upon"}},
    {{"type": "setting", "label": "Place", "nzsl_sign": "SIGN", "semantic_role": "Where it is happening"}}
  ],
  "learning_prompts": [
    {{"type": "wh_question", "nzsl": "LOOK SCENE. WHO?", "en": "Who do you see in the scene?"}},
    {{"type": "wh_question", "nzsl": "WHAT DO?", "en": "What are they doing?"}},
    {{"type": "wh_question", "nzsl": "WHERE?", "en": "Where is this happening?"}},
    {{"type": "wh_question", "nzsl": "HOW FEEL?", "en": "How do they feel?"}}
  ],
  "exports": {{
    "pdf": {{"include": ["symbol_board", "story_scaffold", "vsd_hotspots", "learning_prompts"], "paper": "A4"}},
    "html_offline": {{"include_media_inline": true, "vsd_hotspots": true}},
    "json_data": {{"include_all_metadata": true, "format": "tohu_kaiako_v1"}}
  }}
}}

DETAILED REQUIREMENTS:

1. KEY_SIGNS (3-6 signs):
   - Use authentic NZSL glosses in ALL CAPS (e.g., BIRD, GARDEN, PLAY, HAPPY)
   - Choose signs that are:
     * Developmentally appropriate for 3-5 year olds
     * Visually interesting and fun to perform
     * Connected to the theme and children's everyday experiences
     * A mix of nouns, verbs, and descriptors
   - Include at least one emotion/feeling sign

2. CLASSIFIERS (1-3 examples):
   - Use NZSL classifier notation (e.g., "CL:B (flat hand showing wing)", "CL:1 (person walking)")
   - Describe what the classifier represents
   - Choose classifiers that:
     * Are easy for young children to form
     * Add visual storytelling to the narrative
     * Connect directly to the theme

3. FACIAL_EXPRESSIONS (2-4 emotions):
   - Choose clear, recognizable emotions
   - Ensure they match the story's tone and theme
   - Use child-friendly emotion words (Happy, Sad, Surprised, Excited, Curious, Proud, etc.)
   - These should be emotions children can identify and express

4. STORY_OUTLINE (3-5 steps):
   - Write 3-5 SHORT, simple narrative steps
   - Each step should be 1-2 sentences maximum
   - Use present tense and active voice
   - Make it sequential and easy to sign along with
   - Include opportunities to use the key signs
   - Make it engaging, positive, and age-appropriate
   - Incorporate movement and interaction opportunities

4b. STORY_SCAFFOLD (roles + frames):
   
   This is the NEW structured approach to storytelling!
   
   ROLES (3-5 semantic roles):
   - Identify the key semantic roles in your story
   - AGENT: Who is doing the action (person, animal, character)
   - ACTION: What is happening (main verb/activity)
   - LOCATION: Where it takes place
   - PATIENT: What is being acted upon (optional - if applicable)
   - STATE: Emotion/quality/attribute (optional - if applicable)
   
   For each role provide:
   - role: Uppercase semantic role name (AGENT, ACTION, LOCATION, PATIENT, STATE)
   - gloss: Simple English word (e.g., "Fantail", "Fly", "Garden", "Flower", "Happy")
   - nzsl: NZSL gloss in ALL CAPS (e.g., "FANTAIL", "FLY", "GARDEN", "FLOWER", "HAPPY")
   
   FRAMES (3-4 sequential steps):
   - Break the story into 3-4 simple frames
   - Each frame is one moment/action in the sequence
   - Frame must include:
     * id: Frame number (1, 2, 3, 4)
     * nvpair: Array of role names used in this frame (e.g., ["AGENT", "LOCATION"])
     * caption_en: English sentence describing frame (e.g., "The fantail is in the garden.")
     * gloss: NZSL gloss sequence (e.g., "FANTAIL GARDEN")
   
   Example for "Fantail flies to flower in garden":
   {{
     "theme": "Pīwakawaka in the Garden",
     "roles": [
       {{"role": "AGENT", "gloss": "Fantail", "nzsl": "FANTAIL"}},
       {{"role": "ACTION", "gloss": "Fly", "nzsl": "FLY"}},
       {{"role": "LOCATION", "gloss": "Garden", "nzsl": "GARDEN"}},
       {{"role": "PATIENT", "gloss": "Flower", "nzsl": "FLOWER"}},
       {{"role": "STATE", "gloss": "Happy", "nzsl": "HAPPY"}}
     ],
     "frames": [
       {{"id": 1, "nvpair": ["AGENT", "LOCATION"], "caption_en": "The fantail is in the garden.", "gloss": "FANTAIL GARDEN"}},
       {{"id": 2, "nvpair": ["AGENT", "ACTION", "PATIENT"], "caption_en": "The fantail flies to the flower.", "gloss": "FANTAIL FLY-TO FLOWER"}},
       {{"id": 3, "nvpair": ["AGENT", "STATE"], "caption_en": "The fantail is happy.", "gloss": "FANTAIL HAPPY"}}
     ]
   }}

5. ACTIVITY_WEB (exactly 4 activities):
   
   Art Activity:
   - Hands-on creative expression related to theme
   - Simple materials (paper, crayons, natural items, etc.)
   - Clear connection to the theme
   - Allows for individual expression and creativity
   
   NZSL Language Activity:
   - Interactive sign language practice
   - Games, songs, or role-play using the key signs
   - Fun, repetitive, engaging for young learners
   - Builds signing confidence and fluency
   
   Maths Activity:
   - Concrete, hands-on numeracy experience
   - Counting, sorting, patterns, or shapes
   - Connected to the theme
   - Uses manipulatives or real objects
   
   Deaf Culture Activity:
   - Celebrates Deaf community and culture
   - Age-appropriate awareness building
   - Positive representation and inclusion
   - May include Deaf role models, stories, or cultural practices

6. SEMANTIC_COMPONENTS (3-5 components):
   
   CRITICAL: These are the building blocks for scene-based learning!
   
   Break down the theme into its core semantic elements:
   
   Agent (WHO):
   - The person, animal, or character doing the action
   - Label: Simple noun (e.g., "Boy", "Fantail", "Kaiako")
   - NZSL sign: The sign for this agent
   - Role: "Who is doing the action" or "Who is in the scene"
   
   Action (WHAT DOING):
   - The main verb or activity happening
   - Label: Action word (e.g., "Fly", "Eat", "Play")
   - NZSL sign: The sign for this action
   - Role: "What is happening" or "What they are doing"
   
   Object (WHAT):
   - What the action is directed toward (if applicable)
   - Label: Noun (e.g., "Apple", "Ball", "Flower")
   - NZSL sign: The sign for this object
   - Role: "What is being acted upon" or "What they're using"
   
   Setting (WHERE):
   - The location or context
   - Label: Place (e.g., "Garden", "Kitchen", "Playground")
   - NZSL sign: The sign for this setting
   - Role: "Where it is happening" or "Where they are"
   
   Optional - Attribute (HOW/WHAT KIND):
   - Descriptive quality if relevant
   - Label: Adjective (e.g., "Happy", "Big", "Red")
   - NZSL sign: The sign for this attribute
   - Role: "How they feel" or "What it's like"
   
   Example for "Fantail flies in the garden":
   - Agent: {{"type": "agent", "label": "Fantail", "nzsl_sign": "FANTAIL", "semantic_role": "Who is flying"}}
   - Action: {{"type": "action", "label": "Fly", "nzsl_sign": "FLY", "semantic_role": "What is happening"}}
   - Setting: {{"type": "setting", "label": "Garden", "nzsl_sign": "GARDEN", "semantic_role": "Where the bird is"}}
   - Attribute: {{"type": "attribute", "label": "Happy", "nzsl_sign": "HAPPY", "semantic_role": "How the bird feels"}}

7. LEARNING_PROMPTS (4-6 structured prompts):
   
   Create NZSL-first scaffolding questions with English support:
   
   NZSL-FIRST FORMAT:
   - Use NZSL sentence structure (topic-comment, visual-spatial grammar)
   - Short, directive commands followed by WH-question
   - Example: "LOOK SCENE. WHO?" not "Who do you see?"
   
   Required prompt types:
   - WHO question: {{"type": "wh_question", "nzsl": "LOOK SCENE. WHO?", "en": "Who do you see in the scene?"}}
   - WHAT question: {{"type": "wh_question", "nzsl": "WHAT DO?", "en": "What are they doing?"}}
   - WHERE question: {{"type": "wh_question", "nzsl": "WHERE?", "en": "Where is this happening?"}}
   - FEELING question: {{"type": "wh_question", "nzsl": "HOW FEEL?", "en": "How do they feel?"}}
   
   Optional extensions:
   - Sequence: {{"type": "sequence", "nzsl": "FIRST? NEXT? FINISH?", "en": "What happened first? Then? At the end?"}}
   - Why: {{"type": "extension", "nzsl": "WHY THINK?", "en": "Why do you think that happened?"}}
   
   CRITICAL:
   - NZSL must be primary (listed first)
   - English is support/translation only
   - Use authentic NZSL structure, not signed English

8. VSD_HOTSPOTS (3-5 hotspots matching story_scaffold roles):
   
   Create interactive hotspots for Visual Scene Display questioning:
   
   BBOX COORDINATES:
   - Use normalized 0-1 coordinates (0=left/top, 1=right/bottom)
   - x, y = top-left corner of bbox
   - w, h = width and height
   - Estimate sensible positions (teacher can adjust in UI)
   - Avoid edge clipping (keep 0.05 margin from edges)
   
   MAPPING TO STORY ROLES:
   - Create one hotspot for each role in story_scaffold.roles
   - Use same gloss and labels
   - ID format: "{{"role"}}_{{"number"}}" (e.g., "AGENT_1", "LOCATION_1")
   
   TEACHER PROMPTS:
   - AGENT → "LOOK SCENE. WHO?" or "WHO HERE?"
   - ACTION → "WHAT DO?" or "WHAT HAPPENING?"
   - LOCATION → "WHERE?" or "WHERE THIS?"
   - PATIENT/OBJECT → "WHAT?" or "WHAT SEE?"
   - STATE → "HOW FEEL?" or "FEEL WHAT?"
   
   TE REO MĀORI LABELS:
   - Provide te reo Māori labels for common nouns where known
   - Examples: fantail→pīwakawaka, garden→māra, child→tamaiti
   - Leave empty ("") if unsure - teacher can add later
   
   Example for "Fantail flies in garden":
   [
     {{"id": "AGENT_1", "role": "AGENT", "label_en": "Fantail", "label_te_reo": "pīwakawaka",
       "nzsl_gloss": "FANTAIL", "bbox": {{"x": 0.55, "y": 0.30, "w": 0.25, "h": 0.30}},
       "teacher_prompt": "LOOK SCENE. WHO?"}},
     {{"id": "ACTION_1", "role": "ACTION", "label_en": "Fly", "label_te_reo": "rere",
       "nzsl_gloss": "FLY", "bbox": {{"x": 0.45, "y": 0.22, "w": 0.30, "h": 0.20}},
       "teacher_prompt": "WHAT DO?"}},
     {{"id": "LOCATION_1", "role": "LOCATION", "label_en": "Garden", "label_te_reo": "māra",
       "nzsl_gloss": "GARDEN", "bbox": {{"x": 0.10, "y": 0.50, "w": 0.40, "h": 0.40}},
       "teacher_prompt": "WHERE?"}}
   ]

9. SYMBOL_BOARD (3-5 cards matching story_scaffold roles):
   
   Create symbol cards using Colourful Semantics colour coding:
   
   COLOUR MAPPING:
   - agent (WHO) → orange
   - action (WHAT DO) → yellow
   - object/patient (WHAT) → green
   - setting/location (WHERE) → blue
   - state/attribute (HOW/FEELING) → purple
   
   IMAGE_REF:
   - Use descriptive filename: "{{"type"}}_{{"label"}}.png"
   - Examples: "agent_fantail.png", "action_fly.png", "setting_garden.png"
   
   ALT TEXT:
   - Describe the image for screen readers
   - Format: "{{"Label"}}, {{"brief description"}}"
   - Example: "Fantail, a small native New Zealand bird"
   
   TE REO MĀORI:
   - Same as VSD hotspots - provide where known, leave empty if unsure
   
   MAPPING:
   - Create one symbol card for each role in story_scaffold.roles
   - Use same labels and glosses
   - Match semantic role to Colourful Semantics colour
   
   Example:
   [
     {{"type": "agent", "label_en": "Fantail", "label_te_reo": "pīwakawaka",
       "nzsl_gloss": "FANTAIL", "image_ref": "agent_fantail.png",
       "alt": "Fantail, small native bird with fan-shaped tail", "colour": "orange"}},
     {{"type": "action", "label_en": "Fly", "label_te_reo": "rere",
       "nzsl_gloss": "FLY", "image_ref": "action_fly.png",
       "alt": "Flying motion with wings spread", "colour": "yellow"}},
     {{"type": "setting", "label_en": "Garden", "label_te_reo": "māra",
       "nzsl_gloss": "GARDEN", "image_ref": "setting_garden.png",
       "alt": "Garden with plants and flowers", "colour": "blue"}}
   ]

10. EXPORTS (fixed structure):
    
    Always return this exact structure for export configuration:
    
    {{
      "pdf": {{
        "include": ["symbol_board", "story_scaffold", "vsd_hotspots", "learning_prompts"],
        "paper": "A4"
      }},
      "html_offline": {{
        "include_media_inline": true,
        "vsd_hotspots": true
      }},
      "json_data": {{
        "include_all_metadata": true,
        "format": "tohu_kaiako_v1"
      }}
    }}

THEME: "{theme}"
LEVEL: "{level}"
ADDITIONAL CONTEXT: "{keywords if keywords else 'General early learning context'}"

CRITICAL RULES:
- Return ONLY the JSON object - no markdown code blocks, no explanations
- VSD hotspots, symbol board, and story scaffold MUST use consistent labels/glosses
- Ensure all activities are safe, inclusive, and developmentally appropriate
- Use Aotearoa NZ context where relevant (native birds, local environments, etc.)
- Make content joyful, playful, and engaging for young children
- Respect Deaf culture and NZSL as a living language
- SEMANTIC COMPONENTS must be clear, distinct, and support scene-based learning
- LEARNING PROMPTS must use NZSL-first structure (not signed English)
- BBOX coordinates are estimates - teachers will adjust in UI
- TE REO MĀORI labels should be accurate where provided, empty if unsure
""".strip()
