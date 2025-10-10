import logging
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .llm import generate_pack
from .schemas import (
    Activity,
    GenerateRequest,
    GenerateResponse,
    NZSLStoryPrompt,
    SemanticComponent,
    StoryScaffold,
)

logger = logging.getLogger("tohu-kaiako")
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))

app = FastAPI(title="Tohu Kaiako API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/generate_pack", response_model=GenerateResponse)
async def api_generate_pack(req: GenerateRequest) -> GenerateResponse:
    try:
        text_json, scene_images = await generate_pack(req.theme, req.level, req.keywords or "")
        
        # Parse story_scaffold if present
        story_scaffold = None
        if "story_scaffold" in text_json:
            story_scaffold = StoryScaffold(**text_json["story_scaffold"])
        
        # Parse vsd_hotspots if present - keep as raw dicts for MVP
        vsd_hotspots = text_json.get("vsd_hotspots", [])
        
        # Parse symbol_board if present - keep as raw dicts for MVP
        symbol_board = text_json.get("symbol_board", [])
        
        response_payload: Dict[str, Any] = {
            "image_url": scene_images["scene"],
            "nzsl_story_prompt": NZSLStoryPrompt(**text_json["nzsl_story_prompt"]),
            "activity_web": [Activity(**activity) for activity in text_json["activity_web"]],
            "semantic_components": [SemanticComponent(**comp) for comp in text_json.get("semantic_components", [])],
            "learning_prompts": text_json.get("learning_prompts", []),
            "scene_images": scene_images,
            "story_scaffold": story_scaffold,
            "vsd_hotspots": vsd_hotspots,
            "symbol_board": symbol_board,
        }
        return GenerateResponse(**response_payload)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Pack generation failed", extra={"error": str(exc)}, exc_info=True)
        # Provide more specific error messages
        error_msg = str(exc)
        if "401" in error_msg or "Unauthorized" in error_msg:
            detail = "API authentication failed. Please check your Google Generative AI API key and project billing."
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            detail = "Rate limit exceeded. Please wait a moment and try again."
        elif "timeout" in error_msg.lower():
            detail = "Request timed out. Please try again."
        elif "Invalid" in error_msg and "response" in error_msg:
            detail = "Invalid response from AI service. Please try again."
        else:
            detail = f"Generation failed: {error_msg}"
        raise HTTPException(status_code=500, detail=detail) from exc
