def image_prompt(theme: str, keywords: str) -> str:
    return (
        "A simple, bold, clear illustration for a 4-year-old child.\n"
        f"Theme: '{theme}'. {keywords}\n"
        "Visually distinct subject, uncluttered background, friendly storybook style.\n"
        "No text, child-safe, neutral lighting, warm palette."
    )


def text_system_prompt(theme: str, level: str, keywords: str) -> str:
    return f"""
You are an expert NZSL early childhood curriculum developer in Aotearoa NZ.
Return strict JSON with keys: "nzsl_story_prompt" and "activity_web".

'nzsl_story_prompt':
- key_signs: 3–6 NZSL glosses in ALL CAPS (e.g., BIRD, FLY)
- classifiers: 1–3 classifier ideas (e.g., CL:V)
- facial_expressions: 2–4 relevant emotions
- story_outline: 3–5 short steps children can sign along with

'activity_web':
- 4 objects with:
  - category ∈ {{Art, NZSL Language, Maths, Deaf Culture}}
  - description: simple, practical activity for ages 3–5

Theme: "{theme}"
Level: "{level}"
Optional keywords: "{keywords}"
Return ONLY JSON. No commentary.
""".strip()
