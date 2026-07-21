"""Ztransfer API server — document format conversion."""
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.config import UPLOAD_DIR, OUTPUT_DIR, MAX_FILE_SIZE, ALL_PAIRS, EXTENSION_MIME, IMAGE_PAIRS
from backend.converters.office import convert_office
from backend.converters.image import image_to_pdf, image_to_docx

app = FastAPI(title="Ztransfer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/formats")
def list_formats():
    """Return all supported conversion pairs."""
    pairs = [{"from": src, "to": dst} for src, dst in ALL_PAIRS]
    return {"pairs": pairs}


@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    target: str = Query(..., description="Target format, e.g. 'pdf', 'docx'"),
):
    """Upload a file and convert it to the target format."""
    # Validate file
    if not file.filename:
        raise HTTPException(400, "No file provided")

    # Determine source extension
    source_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if not source_ext:
        raise HTTPException(400, "Cannot determine source file format from filename")

    target = target.lower()

    # Validate conversion pair
    if (source_ext, target) not in ALL_PAIRS:
        raise HTTPException(
            400,
            f"Unsupported conversion: {source_ext} → {target}. "
            f"Call GET /formats to see supported pairs.",
        )

    # Save uploaded file
    file_id = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.{source_ext}")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)} MB.")

    with open(input_path, "wb") as f:
        f.write(content)

    # Convert
    try:
        if (source_ext, target) in IMAGE_PAIRS:
            if target == "pdf":
                output_path = image_to_pdf(input_path)
            elif target == "docx":
                output_path = image_to_docx(input_path)
            else:
                raise HTTPException(500, "Image conversion logic error")
        else:
            output_path = convert_office(input_path, source_ext, target)
    except RuntimeError as e:
        raise HTTPException(500, str(e))
    finally:
        # Clean up uploaded file
        if os.path.exists(input_path):
            os.remove(input_path)

    output_filename = f"{os.path.splitext(file.filename)[0]}.{target}"
    media_type = EXTENSION_MIME.get(target, "application/octet-stream")

    return FileResponse(
        output_path,
        media_type=media_type,
        filename=output_filename,
        background=lambda: os.remove(output_path) if os.path.exists(output_path) else None,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
