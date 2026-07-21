"""Quick e2e test script — image to PDF (no LibreOffice needed)"""
import requests
import os
import sys

BASE = "http://localhost:8000"

# Check server
r = requests.get(f"{BASE}/health")
assert r.status_code == 200, "Server not running"
print("[OK] Server is up")

# Test image -> PDF conversion
test_img = os.path.join(os.path.dirname(__file__), "backend", "uploads", "test_img.png")
if not os.path.exists(test_img):
    from PIL import Image
    Image.new("RGB", (100, 100), "red").save(test_img)
    print("[OK] Test image created")

with open(test_img, "rb") as f:
    r = requests.post(f"{BASE}/convert?target=pdf", files={"file": ("test.png", f, "image/png")})

assert r.status_code == 200, f"Conversion failed: {r.status_code} {r.text}"

out_path = os.path.join(os.path.dirname(__file__), "backend", "uploads", "test_output.pdf")
with open(out_path, "wb") as f:
    f.write(r.content)

print(f"[OK] Image -> PDF: {os.path.getsize(out_path)} bytes written to test_output.pdf")
print("All tests passed!")
