"""Image conversion: image to PDF and image to Word."""
import os
from pathlib import Path

from PIL import Image
from docx import Document
from docx.shared import Inches

from backend.config import OUTPUT_DIR


def image_to_pdf(input_path: str) -> str:
    """Convert a single image to PDF.

    Opens the image with Pillow, converts to RGB if needed, and saves as PDF.
    """
    input_path = os.path.abspath(input_path)
    stem = Path(input_path).stem
    output_path = os.path.join(OUTPUT_DIR, f"{stem}.pdf")

    img = Image.open(input_path)

    if img.mode in ("RGBA", "LA", "P", "PA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode in ("RGBA", "LA"):
            background.paste(img, mask=img.split()[-1])
        else:
            background.paste(img)
        img = background
    elif img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    img.save(output_path, "PDF", resolution=100.0)
    return output_path


def image_to_docx(input_path: str) -> str:
    """Embed an image into a Word document, centered with max 6-inch width."""
    input_path = os.path.abspath(input_path)
    stem = Path(input_path).stem
    output_path = os.path.join(OUTPUT_DIR, f"{stem}.docx")

    doc = Document()
    paragraph = doc.add_paragraph()
    paragraph.alignment = 1  # center
    run = paragraph.add_run()
    run.add_picture(input_path, width=Inches(6.0))

    doc.save(output_path)
    return output_path
