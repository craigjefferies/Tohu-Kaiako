import asyncio
import json
import logging
import base64
from typing import Any, Dict, Tuple

import google.generativeai as genai

from .prompts import image_prompt, text_system_prompt
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


async def call_image(theme: str, keywords: str) -> str:
    """
    Generate an image using Google Gemini's image generation model.
    Falls back to SVG placeholder if generation fails.
    """
    logger.info(f"Generating image for theme: {theme}")
    
    try:
        # Use Gemini's image generation model
        model = genai.GenerativeModel(settings.image_model)
        prompt_text = image_prompt(theme, keywords)
        
        logger.info(f"Calling {settings.image_model} with prompt: {prompt_text[:100]}...")
        
        # Generate content
        response = await asyncio.to_thread(
            model.generate_content,
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            )
        )
        
        # Extract image data from response
        if response.candidates:
            candidate = response.candidates[0]
            for part in candidate.content.parts:
                # Look for inline image data
                if hasattr(part, 'inline_data'):
                    data = part.inline_data
                    if data.mime_type and 'image' in data.mime_type:
                        # Convert to base64 data URL
                        base64_image = base64.b64encode(data.data).decode('utf-8')
                        data_url = f"data:{data.mime_type};base64,{base64_image}"
                        
                        logger.info(f"Successfully generated image (size: {len(data.data)} bytes, type: {data.mime_type})")
                        return data_url
        
        # If we got here, no image was found in response
        logger.warning("No image data found in response, using placeholder")
        return _generate_svg_placeholder(theme)
        
    except Exception as exc:
        logger.warning(f"Image generation failed: {exc}, using placeholder")
        return _generate_svg_placeholder(theme)


def _generate_svg_placeholder(theme: str) -> str:
    """Generate a simple SVG placeholder image."""
    import urllib.parse
    
    # Create a color based on the theme for visual variety
    color_code = abs(hash(theme)) % 0xFFFFFF
    bg_color = f"#{color_code:06x}"
    
    theme_text = theme[:50]  # Limit length
    
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


async def generate_pack(theme: str, level: str, keywords: str) -> Tuple[Dict[str, Any], str]:
    text_task = asyncio.create_task(call_text(theme, level, keywords))
    image_task = asyncio.create_task(call_image(theme, keywords or ""))

    text_json, image_url = await asyncio.gather(text_task, image_task)
    return text_json, image_url
