# VSD Hotspots & Symbol Board Integration

## Overview

This document describes the integration of **Visual Scene Display (VSD) hotspots** and **Colourful Semantics symbol boards** with the existing story scaffold structure.

## What's New

### 1. Visual Scene Display (VSD) Hotspots

Interactive hotspots overlaid on the scene image for teacher-guided questioning.

**Key Features:**
- **Normalized bbox coordinates** (0-1) for responsive positioning
- **Mapped to story_scaffold roles** (AGENT, ACTION, LOCATION, PATIENT, STATE)
- **NZSL-first teacher prompts** ("LOOK SCENE. WHO?", "WHAT DO?", "WHERE?")
- **Te reo Māori labels** (auto-populated where known)
- **Teacher-editable** (coordinates are LLM estimates, adjustable in UI)

**Example:**
```json
{
  "vsd_hotspots": [
    {
      "id": "AGENT_1",
      "role": "AGENT",
      "label_en": "Fantail",
      "label_te_reo": "pīwakawaka",
      "nzsl_gloss": "FANTAIL",
      "bbox": {"x": 0.60, "y": 0.35, "w": 0.20, "h": 0.25},
      "teacher_prompt": "LOOK SCENE. WHO?"
    }
  ]
}
```

### 2. Symbol Board (Colourful Semantics Cards)

Printable/digital symbol cards using established Colourful Semantics colour coding.

**Colour Mapping:**
- **Orange**: AGENT (WHO) - person, animal, character
- **Yellow**: ACTION (WHAT DO) - verb, activity
- **Green**: OBJECT/PATIENT (WHAT) - thing being acted upon
- **Blue**: SETTING/LOCATION (WHERE) - place, environment
- **Purple**: STATE/ATTRIBUTE (HOW) - emotion, quality, feeling

**Example:**
```json
{
  "symbol_board": [
    {
      "type": "agent",
      "label_en": "Fantail",
      "label_te_reo": "pīwakawaka",
      "nzsl_gloss": "FANTAIL",
      "image_ref": "agent_fantail.png",
      "alt": "Fantail, small native bird with fan-shaped tail",
      "colour": "orange"
    }
  ]
}
```

### 3. NZSL-First Learning Prompts

Structured prompts using authentic NZSL sentence structure (not signed English).

**Format:**
```json
{
  "learning_prompts": [
    {"type": "wh_question", "nzsl": "LOOK SCENE. WHO?", "en": "Who do you see?"},
    {"type": "wh_question", "nzsl": "WHAT DO?", "en": "What are they doing?"},
    {"type": "wh_question", "nzsl": "WHERE?", "en": "Where is this happening?"},
    {"type": "wh_question", "nzsl": "HOW FEEL?", "en": "How do they feel?"}
  ]
}
```

### 4. Export Configuration

Predefined export settings for PDF, HTML, and JSON outputs.

```json
{
  "exports": {
    "pdf": {
      "include": ["symbol_board", "story_scaffold", "vsd_hotspots", "learning_prompts"],
      "paper": "A4"
    },
    "html_offline": {
      "include_media_inline": true,
      "vsd_hotspots": true
    },
    "json_data": {
      "include_all_metadata": true,
      "format": "tohu_kaiako_v1"
    }
  }
}
```

## Integration with Story Scaffold

### Unified Semantic Model

All three components (story_scaffold, vsd_hotspots, symbol_board) share the same semantic roles:

**story_scaffold.roles** → Defines the semantic structure
```json
{
  "roles": [
    {"role": "AGENT", "gloss": "Fantail", "nzsl": "FANTAIL"},
    {"role": "ACTION", "gloss": "Fly", "nzsl": "FLY"},
    {"role": "LOCATION", "gloss": "Garden", "nzsl": "GARDEN"}
  ]
}
```

**vsd_hotspots** → Interactive questioning layer
- One hotspot per role
- Uses same `label_en`, `nzsl_gloss` as story role
- Adds `bbox` coordinates and `teacher_prompt`

**symbol_board** → Visual learning cards
- One card per role
- Uses same `label_en`, `nzsl_gloss` as story role
- Adds `image_ref`, `colour`, `alt` text

### Data Flow

1. **LLM generates story_scaffold** with 3-5 semantic roles
2. **LLM auto-creates vsd_hotspots** from roles (estimates bbox coordinates)
3. **LLM auto-creates symbol_board** from roles (assigns Colourful Semantics colours)
4. **Teacher can adjust** bbox coordinates in UI
5. **Export systems** use all three components for complete learning pack

## Technical Implementation

### New Schemas (backend/schemas.py)

```python
class BBox(BaseModel):
    x: float  # 0-1 normalized (left position)
    y: float  # 0-1 normalized (top position)
    w: float  # 0-1 normalized (width)
    h: float  # 0-1 normalized (height)

class VSDHotspot(BaseModel):
    id: str  # "AGENT_1", "ACTION_1", etc.
    role: str  # AGENT, ACTION, LOCATION, PATIENT, STATE
    label_en: str
    label_te_reo: str = ""
    nzsl_gloss: str
    bbox: BBox
    teacher_prompt: str  # NZSL-first question

class SymbolCard(BaseModel):
    type: str  # agent, action, object, setting, state
    label_en: str
    label_te_reo: str = ""
    nzsl_gloss: str
    image_ref: str  # Filename or data URI
    alt: str  # Accessibility description
    colour: str  # orange, yellow, green, blue, purple
```

### Enhanced Prompts (backend/prompts.py)

**text_system_prompt()**: Now generates vsd_hotspots, symbol_board, exports
**scene_image_prompt()**: Added spatial composition requirements for hotspot-friendly layouts
**vsd_hotspot_plan_prompt()**: NEW - Optional secondary LLM call for bbox refinement

### API Response (backend/app.py)

**GenerateResponse** now includes:
- `vsd_hotspots: List[VSDHotspot] = []`
- `symbol_board: List[SymbolCard] = []`
- `exports: Optional[ExportOptions] = None`

## Pedagogical Benefits

### For Teachers

1. **Guided Questioning**: VSD hotspots provide structured WH-questions in NZSL
2. **Visual Scaffolding**: Symbol cards support emergent literacy and AAC strategies
3. **Cultural Responsiveness**: Te reo Māori + NZSL + English trilingual support
4. **Print-Ready Materials**: Export to PDF for offline classroom use
5. **Differentiation**: Adjust hotspot positions for specific learner needs

### For Learners (Ages 3-5)

1. **Clear Visual Cues**: Colourful Semantics colours help identify sentence parts
2. **Interactive Engagement**: Hotspots encourage pointing, naming, signing
3. **Semantic Awareness**: WHO/WHAT/WHERE scaffolds language comprehension
4. **NZSL Development**: Exposure to authentic sign language structure
5. **Inclusive Design**: Supports Deaf, hard-of-hearing, and hearing learners

## BBox Coordinate Guidelines

### Typical Positioning

**AGENT (character/person)**
- Position: Center-right or center, mid-height
- Coordinates: x: 0.50-0.65, y: 0.25-0.40
- Size: w: 0.20-0.30, h: 0.25-0.35

**ACTION (movement/gesture)**
- Position: Overlapping or near agent, slightly higher
- Coordinates: x: 0.40-0.60, y: 0.20-0.35
- Size: w: 0.25-0.35, h: 0.18-0.28

**LOCATION (background/setting)**
- Position: Lower portion, wider area
- Coordinates: x: 0.10-0.20, y: 0.50-0.65
- Size: w: 0.35-0.50, h: 0.30-0.40

**PATIENT (object being acted on)**
- Position: Near agent or in foreground
- Coordinates: x: 0.20-0.40, y: 0.35-0.50
- Size: w: 0.15-0.25, h: 0.20-0.30

**STATE (expression/emotion)**
- Position: Face/head area of agent
- Coordinates: x: 0.55-0.70, y: 0.25-0.35
- Size: w: 0.12-0.18, h: 0.12-0.18

### Best Practices

- **Keep 0.05 margin from edges** (avoid x<0.05, y<0.05, x+w>0.95, y+h>0.95)
- **Avoid overlapping critical elements** (agent face, action gestures)
- **Use depth cues** (foreground WHO/WHAT, background WHERE)
- **Test on multiple screen sizes** (coordinates are responsive)

## Te Reo Māori Label Guidance

### Auto-Populated Examples

Common nouns with established te reo Māori translations:

- fantail → pīwakawaka
- garden → māra
- child → tamaiti / tamariki
- teacher → kaiako
- bird → manu
- fly → rere
- happy → koa
- play → tākaro

### When to Leave Empty

- **Complex phrases**: Multi-word concepts without single te reo equivalent
- **Uncertain translations**: Better empty than incorrect
- **Regional variations**: When multiple valid options exist
- **Teacher discretion**: Allow teachers to add culturally appropriate terms

## Next Steps

### Frontend UI (Future Work)

1. **Hotspot Overlay Component**
   - Render bbox rectangles on scene image
   - Click to highlight and show teacher_prompt
   - Drag-to-adjust bbox positions

2. **Symbol Card Display**
   - Grid layout (3x3 or 4x4)
   - Colourful Semantics colour borders
   - Print optimization (A4 layout)

3. **Learning Prompt Panel**
   - Toggle NZSL/English display
   - Audio support (text-to-speech for English)
   - Video links to NZSL Online dictionary

4. **Export Functionality**
   - PDF generation (symbol cards + hotspot reference)
   - HTML package (offline bundle with images)
   - JSON download (portable data format)

### Testing Recommendations

1. Generate packs with various themes (animals, activities, emotions)
2. Verify bbox coordinates don't overlap or clip edges
3. Check te reo Māori labels for accuracy
4. Test NZSL prompts with Deaf educators
5. Validate Colourful Semantics colour assignments

## References

- **Colourful Semantics**: Bryan (1997) - Visual-spatial grammar support for SEN learners
- **Visual Scene Display (VSD)**: Light & McNaughton (2013) - AAC strategy for context-based communication
- **NZSL Structure**: McKee (2015) - New Zealand Sign Language grammar and syntax
- **Te Whāriki**: NZ Ministry of Education - Early childhood curriculum framework

## License & Attribution

- NZSL glosses follow NZSL Online dictionary conventions
- Colourful Semantics used under educational fair use
- Te reo Māori labels sourced from Te Aka Māori Dictionary where applicable
- All generated content respects Deaf culture and NZSL as a living language
