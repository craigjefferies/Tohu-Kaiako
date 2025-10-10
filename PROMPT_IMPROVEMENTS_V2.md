# Prompt & Structure Improvements V2

**Date:** October 10, 2025  
**Implemented:** Unified Image Prompts + Story Frames Structure

---

## Summary

This update implements two major improvements to Tohu-Kaiako based on expert feedback:

1. **Unified Image Prompt Template** - Consistent style across all 4 images using SCENE_SEED
2. **Story Scaffold with Frames** - Structured storytelling with semantic roles and sequential frames

---

## 1. Unified Image Prompt Template

### Problem Solved
Previously, each of the 4 images (object, action, setting, scene) used different prompts, resulting in visual inconsistency. Images could have different art styles, color palettes, and aesthetic approaches.

### Solution Implemented
Created a single `unified_image_prompt()` function with:
- **SCENE_SEED** parameter for style coherence (derived from `hash(theme) % 100000`)
- **Asset type slotting** (OBJECT, ACTION, SETTING, SCENE)
- **Asset-specific specifications** dynamically generated
- **Global style guidelines** consistently applied

### New Prompt Structure
```python
def unified_image_prompt(theme, asset_type, asset_spec, scene_seed):
    """
    SYSTEM INTENT:
    - Cohesive, child-safe illustrations
    - Ages 3-5, bilingual NZSL-English
    
    GLOBAL STYLE:
    - Flat, friendly classroom-illustration
    - Soft, warm palette
    - Readable silhouettes
    - Eye-level composition
    
    TASK:
    Create {asset_type} for theme "{theme}"
    {asset_spec}
    
    COHESION:
    - Match style to SEED_ID={scene_seed}
    - Consistent across all assets
    
    OUTPUT:
    - 1024x1024 PNG
    - Appropriate background (transparent/soft)
    - Child-safe, inclusive
    """
```

### Benefits
✅ **Visual coherence** - All 4 images share same art style  
✅ **Predictable outputs** - Consistent dimensions, format  
✅ **DRY principle** - Single template, easier maintenance  
✅ **Clear specifications** - Explicit requirements reduce ambiguity  

---

## 2. Story Scaffold with Frames

### Problem Solved
Previously, stories were simple linear outlines (Step 1, Step 2, Step 3) without explicit semantic structure. Teachers couldn't easily create sequencing activities or map NZSL glosses to narrative moments.

### Solution Implemented
Added structured story scaffold with:
- **Semantic roles** (AGENT, ACTION, LOCATION, PATIENT, STATE)
- **Sequential frames** with English/NZSL pairs
- **Role references** (nvpair) showing which roles appear in each frame

### New Data Models

#### StoryRole
```python
class StoryRole(BaseModel):
    role: str        # AGENT, ACTION, LOCATION, PATIENT, STATE
    gloss: str       # English label (e.g., "Fantail")
    nzsl: str        # NZSL gloss (e.g., "FANTAIL")
```

#### StoryFrame
```python
class StoryFrame(BaseModel):
    id: int                 # Frame number
    nvpair: List[str]       # Roles used ["AGENT", "LOCATION"]
    caption_en: str         # English sentence
    gloss: str             # NZSL gloss sequence
```

#### StoryScaffold
```python
class StoryScaffold(BaseModel):
    theme: str
    roles: List[StoryRole]
    frames: List[StoryFrame]
```

### Example Output
```json
{
  "story_scaffold": {
    "theme": "Pīwakawaka in the Garden",
    "roles": [
      {"role": "AGENT", "gloss": "Fantail", "nzsl": "FANTAIL"},
      {"role": "ACTION", "gloss": "Fly", "nzsl": "FLY"},
      {"role": "LOCATION", "gloss": "Garden", "nzsl": "GARDEN"},
      {"role": "PATIENT", "gloss": "Flower", "nzsl": "FLOWER"},
      {"role": "STATE", "gloss": "Happy", "nzsl": "HAPPY"}
    ],
    "frames": [
      {
        "id": 1,
        "nvpair": ["AGENT", "LOCATION"],
        "caption_en": "The fantail is in the garden.",
        "gloss": "FANTAIL GARDEN"
      },
      {
        "id": 2,
        "nvpair": ["AGENT", "ACTION", "PATIENT"],
        "caption_en": "The fantail flies to the flower.",
        "gloss": "FANTAIL FLY-TO FLOWER"
      },
      {
        "id": 3,
        "nvpair": ["AGENT", "STATE"],
        "caption_en": "The fantail is happy.",
        "gloss": "FANTAIL HAPPY"
      }
    ]
  }
}
```

### Benefits
✅ **Explicit semantic structure** - Clear WHO/WHAT/WHERE/WHAT TO/HOW  
✅ **Sequencing activities** - Frames can be printed and rearranged  
✅ **Bilingual alignment** - English and NZSL side-by-side  
✅ **Auto-generation** - Easy to create activity cards from frames  
✅ **Progressive complexity** - Frames build on each other  

---

## 3. Frontend Display Enhancements

### Story Frames Section
Added new UI component showing:

1. **Semantic Roles Reference**
   - Color-coded role badges
   - English label + NZSL gloss pairs
   - Quick reference for teachers

2. **Sequential Frame Cards**
   - Numbered frames (1, 2, 3...)
   - English caption prominently displayed
   - NZSL gloss in monospace font
   - Role tags showing semantic structure
   - Hover effects for interactivity

### Visual Design
- Blue color scheme for language/literacy focus
- Clear hierarchy (frame number → English → NZSL → roles)
- Print-friendly layout for physical sequencing cards
- Accessible contrast and typography

---

## 4. Technical Implementation

### Files Modified

**backend/prompts.py**
- Added `unified_image_prompt()` base template
- Refactored `component_image_prompt()` to use unified template
- Added `scene_image_prompt()` for full scene generation
- Updated `text_system_prompt()` with story_scaffold requirements
- Added detailed FRAMES and ROLES documentation

**backend/schemas.py**
- Added `StoryRole` model
- Added `StoryFrame` model  
- Added `StoryScaffold` model
- Updated `GenerateResponse` to include optional `story_scaffold`

**backend/llm.py**
- Added `scene_seed` generation from theme hash
- Updated all image prompts to include `scene_seed` parameter
- Changed import from `image_prompt` to `scene_image_prompt`

**backend/app.py**
- Added `StoryScaffold` import
- Added parsing for `story_scaffold` from LLM response
- Included `story_scaffold` in response payload

**frontend/templates/index.html**
- Added Story Frames section with roles reference
- Added frame card display with bilingual captions
- Added role usage badges (nvpair display)

---

## 5. Backward Compatibility

✅ **Fully backward compatible**
- `story_scaffold` is optional (can be None)
- Existing `story_outline` still generated and displayed
- If `story_scaffold` is present, shows new frames UI
- No breaking changes to existing API contracts

---

## 6. Testing & Validation

### Server Status
✅ Server reloaded successfully after changes  
✅ No compilation errors  
✅ All imports resolved correctly  

### Next Steps for Testing
1. Generate a learning pack with theme "Fantail in the Garden"
2. Verify all 4 images share consistent style
3. Verify story_scaffold is generated with proper roles and frames
4. Check frontend displays story frames correctly
5. Validate English/NZSL gloss pairs are accurate

---

## 7. Future Enhancements (Still To Do)

### High Priority
- [ ] **NZSL video clip resolver** - Link glosses to actual nzsl.nz videos
- [ ] **Curated NZSL map** - 50+ common ECE signs with video URLs
- [ ] **Missing clip warnings** - Show ⚠️ when video unavailable

### Medium Priority
- [ ] **Portable data model** - Save packs as JSON files
- [ ] **Export functionality** - Download as PDF or JSON
- [ ] **Pack versioning** - Iterate and improve packs over time

### Low Priority
- [ ] **Drag-and-drop sequencing** - Interactive frame rearrangement
- [ ] **Multi-seed generation** - Try different visual styles
- [ ] **Custom frame creation** - Teachers add their own frames

---

## 8. Impact Assessment

### For Teachers
✅ Better visual quality - Images look like they belong together  
✅ Sequencing activities - Can print frames for physical manipulation  
✅ Clearer progression - See how story builds frame by frame  
✅ Bilingual support - English and NZSL explicitly paired  

### For Learners
✅ Consistent visual experience - Less cognitive load  
✅ Clear semantic roles - Understand WHO/WHAT/WHERE structure  
✅ Progressive complexity - Frames build understanding step-by-step  
✅ Multiple entry points - Can engage with English or NZSL  

### For Deaf Learners
✅ Explicit NZSL structure - Gloss sequences shown clearly  
✅ Visual-first design - Images and signs prioritized  
✅ Semantic framing - Aligns with visual-spatial language structure  
⚠️ **Still needs video clips** - Text glosses are insufficient  

---

## 9. Alignment with Pedagogical Goals

### Scene-Based Semantic Learning ✅
- Frames explicitly break down semantic components
- WHO/WHAT/WHERE/TO WHAT/HOW structure preserved
- Progressive revelation supports meaning-making

### Te Whāriki Principles ✅
- Holistic development (language + literacy + culture)
- Family and community (shareable frames)
- Contribution (learner agency in sequencing)
- Communication (bilingual expression)

### Deaf Pedagogy ⚠️
- Visual-spatial structure: ✅ Frames support spatial sequencing
- NZSL primacy: ⚠️ Need video clips, not just glosses
- Deaf culture: ✅ NZSL treated as full language, not supplement

---

## 10. Conclusion

**Successfully implemented 2 of 4 suggested improvements:**
1. ✅ Unified image prompt template with SCENE_SEED
2. ⚠️ NZSL clip linking (not yet implemented - critical next step)
3. ✅ Story scaffold with roles and frames
4. ⚠️ Portable data model (not yet implemented)

**Next Critical Step:** Implement NZSL video clip resolver with curated map of common signs.

Without actual sign language videos, the app remains incomplete for its core purpose of bilingual NZSL-English learning. The text glosses (e.g., "FANTAIL") are useful for teachers who know NZSL, but not sufficient for learners to actually acquire the language.

**Recommendation:** Prioritize NZSL clip linking before any other features.

---

## Appendix: Code Snippets

### Unified Image Prompt Usage
```python
# Generate scene seed for visual coherence
scene_seed = abs(hash(theme)) % 100000

# All images share same scene_seed
object_prompt = component_image_prompt(theme, "object", "Fantail", "FANTAIL", scene_seed)
action_prompt = component_image_prompt(theme, "action", "Fly", "FLY", scene_seed)
setting_prompt = component_image_prompt(theme, "setting", "Garden", "GARDEN", scene_seed)
scene_prompt = scene_image_prompt(theme, keywords, component_list, scene_seed)
```

### Story Frame Generation
```python
# LLM generates this structure
{
  "story_scaffold": {
    "roles": [...],
    "frames": [
      {"id": 1, "nvpair": ["AGENT", "LOCATION"], ...},
      {"id": 2, "nvpair": ["AGENT", "ACTION", "PATIENT"], ...}
    ]
  }
}

# Backend parses and validates
story_scaffold = StoryScaffold(**text_json["story_scaffold"])
```

### Frontend Display
```html
<!-- Story Frames display -->
<template x-for="frame in result.story_scaffold.frames">
  <div class="frame-card">
    <div class="frame-number" x-text="frame.id"></div>
    <p class="caption-en" x-text="frame.caption_en"></p>
    <p class="gloss-nzsl" x-text="frame.gloss"></p>
    <div class="role-tags">
      <template x-for="role_id in frame.nvpair">
        <span x-text="role_id"></span>
      </template>
    </div>
  </div>
</template>
```

---

**End of Document**
