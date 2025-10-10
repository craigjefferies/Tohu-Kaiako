# Scene-Based Semantic Learning: Implementation Plan for Tohu-Kaiako

## 🌱 Core Concept

Scene-based learning constructs meaning through contextualized visual scenes rather than isolated vocabulary. This approach mirrors natural language acquisition - particularly effective for young children, Deaf learners, and multilingual contexts.

**Key Principle:** Meaning emerges from relationships between elements in a coherent visual and conceptual space where symbols, signs, and words coexist.

---

## 🎯 Current State vs. Vision

### Current Implementation (v1.0)
✅ Single unified scene image  
✅ NZSL story prompt with key signs  
✅ Activity web for cross-curricular learning  
✅ Storybook-style illustrations  

### Enhanced Vision (v2.0 - Scene-Based)
🔲 Individual semantic components (objects, actions, settings)  
🔲 Component-level sign/word/image mapping  
🔲 Scene composition workflow  
🔲 Semantic role scaffolding (agent, action, object, setting)  
🔲 Interactive element manipulation  
🔲 Progressive complexity (single → combined scenes)  

---

## 🧱 Implementation Architecture

### Phase 1: Semantic Components (Building Blocks)

**Data Structure:**
```json
{
  "theme": "Boy eats apple in kitchen",
  "semantic_components": [
    {
      "id": "component_1",
      "type": "agent",
      "label": "Boy",
      "nzsl_sign": "BOY",
      "image_url": "data:image/png;base64...",
      "semantic_role": "Who is doing the action"
    },
    {
      "id": "component_2", 
      "type": "action",
      "label": "Eat",
      "nzsl_sign": "EAT",
      "classifier": "CL:C (hand to mouth)",
      "image_url": "data:image/png;base64...",
      "semantic_role": "What is happening"
    },
    {
      "id": "component_3",
      "type": "object",
      "label": "Apple",
      "nzsl_sign": "APPLE",
      "image_url": "data:image/png;base64...",
      "semantic_role": "What is being acted upon"
    },
    {
      "id": "component_4",
      "type": "setting",
      "label": "Kitchen",
      "nzsl_sign": "KITCHEN",
      "image_url": "data:image/png;base64...",
      "semantic_role": "Where it is happening"
    }
  ],
  "combined_scene": {
    "image_url": "data:image/png;base64...",
    "description": "A boy eats an apple in the kitchen",
    "nzsl_sequence": ["BOY", "EAT", "APPLE", "KITCHEN"]
  }
}
```

**Prompt Engineering:**
- Generate 4 separate images (agent, action, object, setting)
- Each with isolated, clear background
- Consistent visual style for coherence
- Simple, bold representation suitable for manipulation

### Phase 2: Scene Composition Workflow

**Learning Sequence:**
1. **Introduce Components** → Show 3-4 isolated semantic elements
2. **Sign Mapping** → Match each with NZSL sign + English word
3. **Scene Building** → Combine into unified scene image
4. **Meaning Making** → Learner describes using available modes
5. **Semantic Expansion** → Modify one element, rebuild scene

**UI/UX Flow:**
```
[Component Cards Row]
[🖼️ Boy] [🖼️ Eat] [🖼️ Apple] [🖼️ Kitchen]
  ↓
[Build Scene Button]
  ↓
[Combined Scene Image]
  ↓
[Sign/Describe Prompt]
```

### Phase 3: Semantic Role Scaffolding

**Visual Indicators:**
- Color coding for semantic roles:
  - 🟦 Blue = Agent (Who)
  - 🟩 Green = Action (What doing)
  - 🟨 Yellow = Object (What)
  - 🟧 Orange = Setting (Where)

**Scaffolding Questions:**
- "WHO is in this scene?"
- "What are they DOING?"
- "What are they doing it TO?"
- "WHERE is this happening?"

---

## 🔧 Technical Implementation

### Backend Changes

**New Schema (schemas.py):**
```python
class SemanticComponent(BaseModel):
    id: str
    type: str  # agent, action, object, setting, attribute
    label: str
    nzsl_sign: str
    classifier: Optional[str] = None
    image_url: str
    semantic_role: str
    
class CombinedScene(BaseModel):
    image_url: str
    description: str
    nzsl_sequence: List[str]
    
class SceneBasedResponse(BaseModel):
    semantic_components: List[SemanticComponent]
    combined_scene: CombinedScene
    learning_prompts: List[str]
```

**New LLM Functions (llm.py):**
```python
async def generate_semantic_components(theme: str) -> List[Dict]:
    """Generate 4 isolated component descriptions for individual images"""
    
async def generate_combined_scene(components: List[Dict]) -> str:
    """Generate unified scene combining all components"""
```

**Prompt Updates (prompts.py):**
```python
def semantic_component_prompt(element: str, type: str) -> str:
    """Isolated element on white background, centered, clear"""
    
def combined_scene_prompt(components: List[Dict]) -> str:
    """All elements integrated into coherent scene"""
```

### Frontend Changes

**New Features:**
- Component card display
- Drag-and-drop scene builder (future)
- Semantic role highlighting
- Sequential reveal animation
- Sign/word overlay on hover

---

## 📚 Pedagogical Enhancements

### 1. Semantic Mapping Activities

**Activity Type: Visual Semantic Web**
```
Components:
- Create semantic web with theme at center
- Branches for agents, actions, objects, settings
- Students add NZSL signs to each node
```

**Activity Type: Story Sequencing**
```
Components:
- Provide 6-8 component cards
- Students arrange to tell a story
- Generate new combined scene from their sequence
```

### 2. Iterative Expansion Patterns

**Substitution:**
- "Boy eats apple" → "Girl eats apple"
- "Boy eats apple" → "Boy eats banana"

**Addition:**
- "Boy eats apple" → "Hungry boy eats apple"
- "Boy eats apple" → "Boy eats red apple"

**Transformation:**
- "Boy eats apple" → "Boy cuts apple"
- "Boy eats apple" → "Boy shares apple"

### 3. Cultural and Contextual Embedding

**NZ-Specific Scenes:**
- Marae contexts (greetings, kai preparation)
- Native environment (bush, beach, birds)
- Cultural practices (haka, waiata, kapa haka)
- Everyday NZ settings (dairy, playground, whānau gathering)

---

## 🎨 Visual Design Principles

### Component Images
- **Isolation:** White or minimal background
- **Clarity:** Single semantic unit, no distractions
- **Scale:** Consistent size for all components
- **Style:** Friendly, storybook quality
- **Modularity:** Can be digitally composed

### Combined Scene Images
- **Integration:** All components naturally positioned
- **Coherence:** Unified lighting, perspective, style
- **Narrative:** Clear action/relationship depicted
- **Cultural accuracy:** NZ context when relevant

---

## 🚀 Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Update schemas for semantic components
- [ ] Create component generation prompts
- [ ] Modify LLM functions for multi-image generation
- [ ] Test component + scene generation flow

### Phase 2: Frontend Integration (Week 3-4)
- [ ] Design component card UI
- [ ] Implement sequential reveal
- [ ] Add semantic role indicators
- [ ] Create scene builder interface

### Phase 3: Pedagogical Features (Week 5-6)
- [ ] Add scaffolding questions
- [ ] Implement substitution/expansion tools
- [ ] Create semantic web visualizer
- [ ] Add story sequencing activity

### Phase 4: Cultural Enhancement (Week 7-8)
- [ ] NZ-specific scene templates
- [ ] Māori cultural contexts
- [ ] Te reo Māori integration option
- [ ] NZSL cultural elements

### Phase 5: Testing & Iteration (Week 9-10)
- [ ] Educator feedback sessions
- [ ] Student usability testing
- [ ] Content quality review
- [ ] Performance optimization

---

## 🧪 Example Scenarios

### Scenario 1: Basic Scene Building
**Theme:** "Playing at the park"

**Components:**
1. Agent: "Child" (CHILD sign + image)
2. Action: "Play" (PLAY sign + image)
3. Object: "Ball" (BALL sign + image)
4. Setting: "Park" (PARK sign + image)

**Workflow:**
- Show 4 component cards
- Student matches signs
- Click "Build Scene"
- Generate combined image
- Student signs/describes scene

### Scenario 2: Cultural Context
**Theme:** "Kai time at the marae"

**Components:**
1. Agent: "Whānau" (FAMILY sign + image)
2. Action: "Share" (SHARE sign + image)
3. Object: "Kai" (FOOD sign + image)
4. Setting: "Marae" (MARAE sign + image)

**Cultural Learning:**
- Semantic role: sharing (cultural value)
- Setting: marae protocol
- Signs: NZSL + te reo Māori integration

### Scenario 3: Semantic Expansion
**Base:** "Bird flies in garden"

**Iterations:**
1. Substitute: "Bird → Fantail" (native bird specificity)
2. Add attribute: "Small bird flies"
3. Transform action: "Bird lands in garden"
4. Add emotional state: "Happy bird flies"

---

## 📊 Success Metrics

### Learning Outcomes
- Students can identify semantic roles (agent, action, object)
- Students match NZSL signs to visual components
- Students construct meaningful scenes from components
- Students generate novel sentences from modified scenes

### Engagement Indicators
- Time spent with component exploration
- Number of scene variations created
- Accuracy of sign-image matching
- Complexity of student-generated narratives

### Accessibility Impact
- Deaf learners demonstrate equivalent comprehension
- Visual learners show improved retention
- Second-language learners bridge meaning effectively
- Students with diverse needs access content equally

---

## 🔗 Integration with Existing Features

### Activity Web Enhancement
Each activity category can now include component-based tasks:

**Art:** 
- Draw your own components
- Create physical scene cards
- Build 3D scenes from components

**NZSL Language:**
- Sign each component in sequence
- Record video signing the scene
- Create new scenes with learned signs

**Maths:**
- Count components
- Sort by semantic role
- Create patterns with components

**Deaf Culture:**
- Identify Deaf cultural components
- Explore visual-spatial grammar
- Compare NZSL vs English structure

---

## 💡 Future Innovations

### Interactive Scene Builder (v3.0)
- Drag-and-drop component positioning
- Real-time scene generation
- Student-driven composition
- Save and share scenes

### AI-Powered Scaffolding (v4.0)
- Adaptive difficulty based on learner
- Automatic semantic role detection
- Personalized component suggestions
- Voice/sign recognition for feedback

### Multilingual Expansion (v5.0)
- Te reo Māori integration
- Pacific language support
- Multiple sign languages
- Cultural context switching

---

## 📖 Theoretical Foundation

### Supporting Research
- **Cognitive Load Theory:** Component isolation reduces cognitive load
- **Dual Coding Theory:** Visual + linguistic encoding strengthens memory
- **Zone of Proximal Development:** Scaffolded progression supports growth
- **Universal Design for Learning:** Multiple means of representation

### Language Acquisition Principles
- **Semantic priming** → Meaning before syntax
- **Contextual embedding** → Real-world relevance
- **Multimodal integration** → Visual-spatial-gestural-linguistic
- **Cultural grounding** → Authentic meaning-making

---

## ✨ Summary

Scene-based semantic learning transforms Tohu-Kaiako from a pack generator to a comprehensive language learning platform that:

1. **Builds meaning systematically** through semantic components
2. **Honors Deaf pedagogy** with visual-spatial primacy
3. **Supports bilingual development** (NZSL-English)
4. **Embeds cultural context** (Aotearoa NZ)
5. **Enables iterative expansion** for progressive complexity
6. **Provides inclusive access** across diverse learning needs

This approach positions Tohu-Kaiako as a pioneering tool in scene-based bilingual early childhood education.

---

**Next Step:** Shall we begin implementing Phase 1 (Core Infrastructure)?
