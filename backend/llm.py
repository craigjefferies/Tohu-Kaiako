import asyncio
import json
import logging
import base64
from typing import Any, Dict, List, Tuple

import google.generativeai as genai

from .prompts import component_image_prompt, scene_image_prompt, text_system_prompt
from .settings import settings

logger = logging.getLogger("tohu-kaiako")

# Configure Google Generative AI
genai.configure(api_key=settings.google_api_key)


async def call_text(theme: str, level: str, keywords: str) -> Dict[str, Any]:
    """Call Google Gemini API for text generation."""
    try:
        model = genai.GenerativeModel(settings.text_model)
        prompt = text_system_prompt(theme, level, keywords)
        
        logger.info(f"Calling Google Gemini with model: {settings.text_model}")
        logger.info(f"API Key present: {bool(settings.google_api_key)}")
        
        # Generate content
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
            )
        )
        
        content = response.text.strip()
        
        # Strip markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            lines = lines[1:]  # Remove first line with ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]  # Remove last line with ```
            content = "\n".join(lines)
        
        logger.info(f"Stripped content to parse: {content[:300]}...")
        return json.loads(content)
        
    except Exception as exc:
        logger.error(f"Failed to generate text: {exc}", exc_info=True)
        raise RuntimeError(f"Text generation error: {str(exc)}") from exc


async def _generate_image(prompt_text: str, placeholder_label: str) -> str:
    """
    Generate an image using Google Gemini's image generation model.
    Falls back to SVG placeholder if generation fails.
    """
    logger.info(f"Generating image for: {placeholder_label}")
    
    try:
        model = genai.GenerativeModel(settings.image_model)
        
        logger.info(f"Calling {settings.image_model} with prompt: {prompt_text[:100]}...")
        
        response = await asyncio.to_thread(
            model.generate_content,
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            )
        )
        
        if response.candidates:
            candidate = response.candidates[0]
            for part in candidate.content.parts:
                if hasattr(part, "inline_data"):
                    data = part.inline_data
                    if data.mime_type and "image" in data.mime_type:
                        base64_image = base64.b64encode(data.data).decode("utf-8")
                        data_url = f"data:{data.mime_type};base64,{base64_image}"
                        
                        logger.info(
                            "Successfully generated image",
                            extra={"size": len(data.data), "type": data.mime_type, "label": placeholder_label},
                        )
                        return data_url
        
        logger.warning("No image data found in response, using placeholder")
        return _generate_svg_placeholder(placeholder_label)
        
    except Exception as exc:
        logger.warning(f"Image generation failed for {placeholder_label}: {exc}, using placeholder")
        return _generate_svg_placeholder(placeholder_label)


def _generate_svg_placeholder(label: str) -> str:
    """Generate a simple SVG placeholder image."""
    import urllib.parse
    
    # Create a color based on the theme for visual variety
    color_code = abs(hash(label)) % 0xFFFFFF
    bg_color = f"#{color_code:06x}"
    
    theme_text = label[:50]  # Limit length
    
    # Create an SVG data URL
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
        <rect width="400" height="300" fill="{bg_color}" opacity="0.3"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" 
              fill="#333" text-anchor="middle" dominant-baseline="middle">
            {theme_text}
        </text>
        <text x="50%" y="60%" font-family="Arial, sans-serif" font-size="14" 
              fill="#666" text-anchor="middle" dominant-baseline="middle">
            (Image placeholder)
        </text>
    </svg>'''
    
    encoded_svg = urllib.parse.quote(svg)
    return f"data:image/svg+xml,{encoded_svg}"


def _index_components(components: Any) -> Dict[str, Dict[str, Any]]:
    """Index semantic components by their lowercased type."""
    indexed: Dict[str, Dict[str, Any]] = {}
    if not isinstance(components, list):
        return indexed
    for comp in components:
        comp_type = str(comp.get("type", "")).lower()
        if comp_type and comp_type not in indexed:
            indexed[comp_type] = comp
    return indexed


def _fallback_component(comp_type: str, theme: str, key_signs: List[str]) -> Dict[str, Any]:
    """Provide a simple fallback component if the model response is missing data."""
    label = theme if comp_type != "setting" else f"{theme} place"
    nzsl_sign = key_signs[0] if key_signs else label.upper()
    return {
        "type": comp_type,
        "label": label,
        "nzsl_sign": nzsl_sign,
        "semantic_role": f"Fallback {comp_type}",
    }


def _to_third_person(verb: str) -> str:
    """
    Convert a simple base verb to third-person singular.
    This covers regular verbs and a handful of common irregular forms.
    """
    word = (verb or "").strip()
    if not word:
        return "does"
    lower = word.lower()
    irregular = {
        "be": "is",
        "have": "has",
        "do": "does",
        "go": "goes",
        "wash": "washes",
    }
    if lower in irregular:
        inflected = irregular[lower]
    elif lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        inflected = lower[:-1] + "ies"
    elif lower.endswith(("s", "x", "z", "ch", "sh", "o")):
        inflected = lower + "es"
    else:
        inflected = lower + "s"
    return inflected


async def generate_pack(theme: str, level: str, keywords: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, str]]:
    text_json = await call_text(theme, level, keywords)
    
    # Generate scene seed from theme for visual coherence
    scene_seed = abs(hash(theme)) % 100000
    
    # Ensure learning prompts stay simple and ordered for Noun → Verb → Location
    default_learning_prompts = [
        "Name the noun first.",
        "Add the verb next.",
        "Finish with where it happens.",
    ]
    incoming_learning = text_json.get("learning_prompts", [])
    learning_prompts = [
        prompt.strip()
        for prompt in incoming_learning
        if isinstance(prompt, str) and prompt.strip()
    ][:3]
    for prompt in default_learning_prompts:
        if len(learning_prompts) >= 3:
            break
        if prompt not in learning_prompts:
            learning_prompts.append(prompt)
    text_json["learning_prompts"] = learning_prompts
    
    components = text_json.get("semantic_components", [])
    indexed_components = _index_components(components)
    
    key_signs = text_json.get("nzsl_story_prompt", {}).get("key_signs", [])
    
    noun_component = (
        indexed_components.get("agent")
        or indexed_components.get("object")
        or _fallback_component("agent", theme, key_signs)
    )
    action_component = indexed_components.get("action") or _fallback_component("action", theme, key_signs)
    location_component = (
        indexed_components.get("location")
        or indexed_components.get("setting")
        or _fallback_component("setting", theme, key_signs)
    )
    
    ordered_components = [noun_component, action_component, location_component]
    extra_components = [
        comp
        for comp in components
        if isinstance(comp, dict) and comp not in ordered_components
    ]
    component_list = ordered_components + extra_components
    
    # Build language steps with graceful fallbacks
    def _label_with_sign(component: Dict[str, Any]) -> Tuple[str, str]:
        label = str(component.get("label") or theme).strip()
        nzsl = str(component.get("nzsl_sign") or label.upper()).strip()
        return label or theme, nzsl or label.upper()
    
    noun_label, noun_sign = _label_with_sign(noun_component)
    verb_label, verb_sign = _label_with_sign(action_component)
    location_label, location_sign = _label_with_sign(location_component)
    
    language_steps = [
        step.strip()
        for step in text_json.get("language_steps", [])
        if isinstance(step, str) and step.strip()
    ]
    if len(language_steps) != 3:
        language_steps = [
            f"Noun: {noun_label} ({noun_sign})",
            f"Verb: {verb_label} ({verb_sign})",
            f"Location: {location_label} ({location_sign})",
        ]
    text_json["language_steps"] = language_steps
    
    # Use unified prompts with scene_seed for coherence
    def _normalise_type(component: Dict[str, Any], default: str) -> str:
        comp_type = str(component.get("type") or "").strip().lower()
        if not comp_type:
            return default
        if default == "setting" and comp_type in {"location", "place"}:
            return "setting"
        return comp_type
    
    noun_type = _normalise_type(noun_component, "agent")
    action_type = _normalise_type(action_component, "action")
    location_type = _normalise_type(location_component, "setting")
    
    noun_prompt = component_image_prompt(
        theme,
        noun_type,
        noun_label,
        noun_sign,
        scene_seed,
    )
    action_prompt = component_image_prompt(
        theme,
        action_type,
        verb_label,
        verb_sign,
        scene_seed,
    )
    location_prompt = component_image_prompt(
        theme,
        location_type,
        location_label,
        location_sign,
        scene_seed,
    )
    scene_prompt = scene_image_prompt(theme, keywords or "", component_list, scene_seed)
    
    noun_task = asyncio.create_task(_generate_image(noun_prompt, f"{theme} noun"))
    action_task = asyncio.create_task(_generate_image(action_prompt, f"{theme} verb"))
    location_task = asyncio.create_task(_generate_image(location_prompt, f"{theme} location"))
    scene_task = asyncio.create_task(_generate_image(scene_prompt, f"{theme} scene"))
    
    noun_image, action_image, location_image, scene_image = await asyncio.gather(
        noun_task, action_task, location_task, scene_task
    )
    
    scene_images = {
        "object": noun_image,
        "action": action_image,
        "setting": location_image,
        "scene": scene_image,
    }
    
    # Assemble simple bilingual sentence data
    def _sentence_case(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return ""
        return stripped[0].upper() + stripped[1:]
    
    noun_phrase_raw = noun_label.strip() or theme
    noun_phrase = noun_phrase_raw.title() if noun_phrase_raw.isupper() else _sentence_case(noun_phrase_raw)
    verb_phrase = _to_third_person(verb_label)
    location_raw = location_label.strip() or f"{theme} place"
    location_core = location_raw.title() if location_raw.isupper() else location_raw
    location_phrase = location_core
    if not location_phrase.lower().startswith("the "):
        location_phrase = f"the {location_phrase}"
    location_phrase = location_phrase.strip()
    
    sentence_en = f"The {noun_phrase} {verb_phrase} in {location_phrase}."
    sentence_nzsl = f"{noun_sign} {verb_sign} {location_sign}"
    
    sentence_payload = {
        "sentence_en": sentence_en,
        "sentence_nzsl": sentence_nzsl,
        "noun_label": noun_label,
        "verb_label": verb_label,
        "location_label": location_label,
        "noun_sign": noun_sign,
        "verb_sign": verb_sign,
        "location_sign": location_sign,
    }
    
    return text_json, scene_images, sentence_payload
