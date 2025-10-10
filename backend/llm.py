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


async def generate_pack(theme: str, level: str, keywords: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
    text_json = await call_text(theme, level, keywords)
    
    # Generate scene seed from theme for visual coherence
    scene_seed = abs(hash(theme)) % 100000
    
    # Ensure learning prompts cover the desired pedagogy
    learning_prompts = text_json.setdefault("learning_prompts", [])
    scaffold_prompts = [
        "Sequence the isolated images to retell the story.",
        "Label each isolated image with its NZSL sign.",
        "Retell or sign the scene using the four images.",
        "Record or sign back your own version of the scene.",
    ]
    for prompt in scaffold_prompts:
        if prompt not in learning_prompts:
            learning_prompts.append(prompt)
    
    components = text_json.get("semantic_components", [])
    indexed_components = _index_components(components)
    
    key_signs = text_json.get("nzsl_story_prompt", {}).get("key_signs", [])
    
    object_component = indexed_components.get("object") or indexed_components.get("agent") or _fallback_component("object", theme, key_signs)
    action_component = indexed_components.get("action") or _fallback_component("action", theme, key_signs)
    setting_component = indexed_components.get("setting") or _fallback_component("setting", theme, key_signs)
    
    component_list = [object_component, action_component, setting_component]
    
    # Use unified prompts with scene_seed for coherence
    object_prompt = component_image_prompt(theme, "object", object_component["label"], object_component.get("nzsl_sign", object_component["label"].upper()), scene_seed)
    action_prompt = component_image_prompt(theme, "action", action_component["label"], action_component.get("nzsl_sign", action_component["label"].upper()), scene_seed)
    setting_prompt = component_image_prompt(theme, "setting", setting_component["label"], setting_component.get("nzsl_sign", setting_component["label"].upper()), scene_seed)
    scene_prompt = scene_image_prompt(theme, keywords or "", component_list, scene_seed)
    
    object_task = asyncio.create_task(_generate_image(object_prompt, f"{theme} object"))
    action_task = asyncio.create_task(_generate_image(action_prompt, f"{theme} action"))
    setting_task = asyncio.create_task(_generate_image(setting_prompt, f"{theme} setting"))
    scene_task = asyncio.create_task(_generate_image(scene_prompt, f"{theme} scene"))
    
    object_image, action_image, setting_image, scene_image = await asyncio.gather(
        object_task, action_task, setting_task, scene_task
    )
    
    scene_images = {
        "object": object_image,
        "action": action_image,
        "setting": setting_image,
        "scene": scene_image,
    }
    
    return text_json, scene_images
