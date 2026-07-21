"""Office format conversions via LibreOffice headless."""
import subprocess
import shutil
import os
from pathlib import Path

from backend.config import OUTPUT_DIR


def _find_soffice() -> str:
    """Find the LibreOffice executable path."""
    candidates = [
        "soffice",
        "libreoffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
        "/opt/libreoffice/program/soffice",
    ]
    for candidate in candidates:
        if shutil.which(candidate) or os.path.exists(candidate):
            return candidate
    return "soffice"


def convert_office(input_path: str, source_ext: str, target_ext: str) -> str:
    """Convert an office document using LibreOffice headless.

    Returns the path to the converted file.
    """
    input_path = os.path.abspath(input_path)
    output_dir = os.path.abspath(OUTPUT_DIR)
    input_file = Path(input_path)
    expected_output = os.path.join(output_dir, f"{input_file.stem}.{target_ext}")

    soffice = _find_soffice()
    cmd = [
        soffice,
        "--headless",
        "--convert-to", target_ext,
        "--outdir", output_dir,
        input_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed ({source_ext} -> {target_ext}): {result.stderr}"
        )

    if not os.path.exists(expected_output):
        raise RuntimeError(
            f"Converted file not found at {expected_output}"
        )

    return expected_output
