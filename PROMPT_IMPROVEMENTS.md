# Prompt Improvements for Tohu-Kaiako

This document outlines the improvements made to both the image generation and text generation prompts.

## Image Generation Prompt Improvements

### Previous Prompt
Simple, basic description:
- "A simple, bold, clear illustration for a 4-year-old child"
- Basic theme and keywords
- Generic style guidance

### Improved Prompt
Comprehensive, detailed specification with:

**1. Enhanced Visual Style Guidance:**
- References to established children's book illustrators (Eric Carle, Beatrix Potter)
- Specific color palette direction (pastels, earth tones, friendly bright colors)
- Clear composition rules (clear focal point, uncluttered background)
- Professional but playful quality standards

**2. Composition Guidelines:**
- Subject placement specifics
- Background treatment
- Age-appropriate scale and perspective
- Emotional atmosphere (safe, positive, joyful)

**3. Cultural Considerations:**
- Aotearoa NZ context awareness
- Accuracy for native flora/fauna
- Diverse, inclusive representation
- Suitable for te reo Māori and NZSL learning environments

**4. Technical Requirements:**
- Explicit "no text" requirement
- Child-safe content emphasis
- High contrast for visibility
- Multi-format suitability (print and digital)

**5. Educational Purpose:**
- Sparks curiosity
- Supports language learning
- Inviting for young learners

### Expected Outcomes:
- More consistent, high-quality illustrations
- Better cultural appropriateness
- Clearer visual storytelling
- More suitable for educational contexts

---

## Text Generation Prompt Improvements

### Previous Prompt
Basic requirements with:
- Simple JSON structure example
- Minimal guidance on content
- Basic category requirements

### Improved Prompt
Comprehensive pedagogical framework with:

**1. Professional Context Setting:**
- Establishes expertise in NZSL ECE curriculum development
- References Te Whāriki (NZ early childhood curriculum)
- Integrates Deaf culture awareness
- Emphasizes play-based, child-centered learning

**2. Detailed Content Specifications:**

**Key Signs (3-6):**
- Must be developmentally appropriate
- Visually interesting and fun to perform
- Connected to everyday experiences
- Mix of nouns, verbs, descriptors
- Include at least one emotion/feeling

**Classifiers (1-3):**
- Proper NZSL notation with descriptions
- Easy for young children to form
- Add visual storytelling
- Connect directly to theme

**Facial Expressions (2-4):**
- Clear, recognizable emotions
- Match story tone
- Child-friendly emotion words
- Identifiable and expressible by children

**Story Outline (3-5 steps):**
- Short, simple narrative steps (1-2 sentences max)
- Present tense, active voice
- Sequential and signable
- Opportunities for key signs
- Engaging, positive, age-appropriate
- Movement and interaction opportunities

**3. Enhanced Activity Web Guidance:**

**Art Activity:**
- Hands-on creative expression
- Simple, accessible materials
- Theme connection
- Individual expression encouraged

**NZSL Language Activity:**
- Interactive sign practice
- Games, songs, or role-play
- Fun, repetitive, engaging
- Builds confidence and fluency

**Maths Activity:**
- Concrete, hands-on experience
- Counting, sorting, patterns, shapes
- Theme-connected
- Uses manipulatives/real objects

**Deaf Culture Activity:**
- Celebrates Deaf community
- Age-appropriate awareness
- Positive representation
- May include role models, stories, cultural practices

**4. Critical Rules:**
- Explicit JSON-only output requirement
- Safety and inclusion emphasis
- Aotearoa NZ contextualization
- Joyful, playful engagement
- Respect for Deaf culture and NZSL

### Expected Outcomes:
- Richer, more pedagogically sound content
- Better cultural appropriateness
- More engaging activities
- Clearer learning objectives
- More authentic NZSL integration
- Stronger Deaf culture representation

---

## Testing Recommendations

1. **Generate Multiple Packs** with different themes to test variety:
   - Nature themes (native birds, plants)
   - Community themes (family, friends, helpers)
   - Activity themes (play, sports, art)
   - Cultural themes (celebrations, traditions)

2. **Evaluate Quality:**
   - Image quality and appropriateness
   - NZSL sign authenticity
   - Activity feasibility and engagement
   - Cultural sensitivity
   - Age appropriateness

3. **Iterate Based on Feedback:**
   - Collect educator feedback
   - Test with children (if applicable)
   - Adjust prompts based on outcomes
   - Document learnings

---

## Maintenance Notes

**Image Prompt:**
- Located in `backend/prompts.py` → `image_prompt()`
- Adjust if image style needs refinement
- Can customize for different age groups
- May need regional/cultural variations

**Text Prompt:**
- Located in `backend/prompts.py` → `text_system_prompt()`
- Adjust for different curriculum frameworks
- Can expand activity categories
- May need different levels (toddlers, preschool, primary)

**Future Enhancements:**
- Template variations for different themes
- Level-specific prompt customization
- Multilingual prompt support (te reo Māori)
- Seasonal/cultural event variations
