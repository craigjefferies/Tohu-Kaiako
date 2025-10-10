from typing import Dict, List, Optional


def component_image_prompt(theme: str, component_type: str, label: str, nzsl_sign: str) -> str:
    """
    Prompt for generating an isolated illustration that highlights a single semantic component.
    """
    return (
        "Create an isolated illustration to support scene-based NZSL storytelling for 3-5 year olds.\n\n"
        f"THEME: {theme}\n"
        f"FOCUS TYPE: {component_type.upper()}\n"
        f"FOCUS LABEL: {label}\n"
        f"NZSL SIGN (for reference only, no text in image): {nzsl_sign}\n\n"
        "REQUIREMENTS:\n"
        "- Show only the focus element with a clean, neutral background\n"
        "- Use clear shapes and colour contrast so tamariki can identify the element quickly\n"
        "- Convey the meaning of the NZSL sign visually (e.g., motion cues, character posture)\n"
        "- Keep composition simple; the element should sit centrally and be easy to cut out\n"
        "- Avoid written text or fingerspelling in the illustration\n\n"
        "STYLE: Warm, inclusive, Aotearoa NZ inspired storybook aesthetic."
    )


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
    "WHO question",
    "WHAT question", 
    "WHERE question",
    "Extension question"
  ]
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

7. LEARNING_PROMPTS (3-5 scaffolding questions):
   
   Create questions that help learners identify semantic roles:
   
   - WHO question: "WHO do you see in this scene?" or "WHO is doing something?"
   - WHAT question: "WHAT are they doing?" or "WHAT is happening?"
   - WHERE question: "WHERE is this happening?" or "WHERE are they?"
   - OBJECT question (if applicable): "WHAT are they using/doing it to?"
   - FEELING question (if applicable): "HOW do they feel?"
   
   Example prompts:
   - "WHO is flying in the garden?"
   - "WHAT is the fantail doing?"
   - "WHERE is the bird flying?"
   - "HOW does the fantail feel?"

THEME: "{theme}"
LEVEL: "{level}"
ADDITIONAL CONTEXT: "{keywords if keywords else 'General early learning context'}"

CRITICAL RULES:
- Return ONLY the JSON object - no markdown code blocks, no explanations
- Ensure all activities are safe, inclusive, and developmentally appropriate
- Use Aotearoa NZ context where relevant (native birds, local environments, etc.)
- Make content joyful, playful, and engaging for young children
- Respect Deaf culture and NZSL as a living language
- SEMANTIC COMPONENTS must be clear, distinct, and support scene-based learning
- LEARNING PROMPTS should scaffold semantic role awareness (WHO, WHAT, WHERE)
""".strip()
