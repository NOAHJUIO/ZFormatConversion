import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping of file extensions to LibreOffice filter names and MIME types
EXTENSION_MIME = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "bmp": "image/bmp",
    "gif": "image/gif",
    "webp": "image/webp",
}

# Supported conversion pairs
# Office conversions (require LibreOffice)
OFFICE_PAIRS = [
    ("docx", "pdf"),
    ("pdf", "docx"),
    ("xlsx", "pdf"),
    ("pdf", "xlsx"),
    ("docx", "xlsx"),
    ("xlsx", "docx"),
]

# Image conversions (pure Python, no LibreOffice needed)
IMAGE_PAIRS = [
    ("jpg", "pdf"),
    ("jpeg", "pdf"),
    ("png", "pdf"),
    ("bmp", "pdf"),
    ("gif", "pdf"),
    ("webp", "pdf"),
    ("jpg", "docx"),
    ("jpeg", "docx"),
    ("png", "docx"),
    ("bmp", "docx"),
    ("gif", "docx"),
    ("webp", "docx"),
]

ALL_PAIRS = OFFICE_PAIRS + IMAGE_PAIRS
