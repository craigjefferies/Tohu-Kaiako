import base64
import os
import tempfile
from typing import Dict, Optional

from fpdf import FPDF


def _data_url_to_bytes(data_url: str) -> Optional[bytes]:
    """Extract raw image bytes from a data URL."""
    if not data_url or not data_url.startswith("data:"):
        return None
    try:
        _, _, encoded = data_url.partition(",")
        if not encoded:
            return None
        return base64.b64decode(encoded)
    except (ValueError, base64.binascii.Error):
        return None


def build_single_page_pdf(
    theme: str,
    images: Dict[str, str],
    sentence_nzsl: str,
    sentence_en: str,
) -> bytes:
    """
    Create a one-page PDF handout with four images and bilingual sentences.
    Images should be provided as data URLs in the order object, action, setting, scene.
    """
    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(False)
    pdf.add_page()
    
    # Header
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, theme, ln=True, align="C")
    pdf.ln(2)
    
    margin = 12
    image_height = 55
    spacing = 4
    available_width = pdf.w - 2 * margin - 3 * spacing
    image_width = available_width / 4
    
    temp_paths = []
    y_start = pdf.get_y()
    x = margin
    for key in ["object", "action", "setting", "scene"]:
        img_bytes = _data_url_to_bytes(images.get(key, ""))
        if img_bytes:
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            tmp_file.write(img_bytes)
            tmp_file.flush()
            tmp_file.close()
            temp_paths.append(tmp_file.name)
            pdf.image(tmp_file.name, x=x, y=y_start, w=image_width, h=image_height)
        x += image_width + spacing
    
    pdf.set_y(y_start + image_height + 10)
    
    # Sentences
    pdf.set_font("Helvetica", "B", 28)
    pdf.multi_cell(0, 14, sentence_nzsl, align="C")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 20)
    pdf.multi_cell(0, 12, sentence_en, align="C")
    
    # Clean up temp files
    for path in temp_paths:
        try:
            os.unlink(path)
        except OSError:
            pass
    
    output = pdf.output(dest="S")
    if isinstance(output, str):
        return output.encode("latin1")
    if isinstance(output, bytearray):
        return bytes(output)
    return output
