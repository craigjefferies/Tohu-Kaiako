import base64
import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .llm import generate_pack
from .pdf_utils import build_single_page_pdf
from .schemas import GenerateRequest, GenerateResponse
from .settings import settings

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
    firebase_config = None
    if settings.firebase_config_json:
        try:
            firebase_config = json.loads(settings.firebase_config_json)
        except json.JSONDecodeError:
            logger.warning("Invalid firebase_config_json; falling back to None.")
            firebase_config = None
    context = {
        "request": request,
        "firebase_config": firebase_config,
        "firebase_app_id": settings.firebase_app_id,
        "firebase_initial_token": settings.firebase_initial_token,
    }
    return templates.TemplateResponse("index.html", context)


@app.post("/api/generate_pack", response_model=GenerateResponse)
async def api_generate_pack(req: GenerateRequest) -> GenerateResponse:
    try:
        pack_payload = await generate_pack(req.theme, req.level, req.keywords or "", req.subject, req.activity)
        scene_images = pack_payload.get("scene_images") or {}
        sentence_en = pack_payload["sentence_en"]
        sentence_nzsl = pack_payload["sentence_nzsl"]
        
        pdf_bytes = build_single_page_pdf(
            theme=pack_payload["theme"],
            images=scene_images,
            sentence_nzsl=sentence_nzsl,
            sentence_en=sentence_en,
        )
        pdf_base64 = base64.b64encode(pdf_bytes).decode("ascii")
        
        pack_payload["pdf_base64"] = pdf_base64
        return GenerateResponse(**pack_payload)
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
