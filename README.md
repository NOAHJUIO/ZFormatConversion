# Ztransfer

Document format conversion tool — convert between PDF, Word, Excel, and images.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Supported Conversions

| Source | Target | Method |
|--------|--------|--------|
| Word (.docx) | PDF | LibreOffice |
| PDF | Word (.docx) | LibreOffice |
| Excel (.xlsx) | PDF | LibreOffice |
| PDF | Excel (.xlsx) | LibreOffice |
| Word ↔ Excel | ↔ | LibreOffice |
| Image (.jpg/.png/.bmp/.gif/.webp) | PDF | Pillow |
| Image (.jpg/.png/.bmp/.gif/.webp) | Word (.docx) | python-docx |

## Architecture

```
miniprogram (WeChat) ──HTTPS──> FastAPI backend ──> LibreOffice / Pillow
```

## Quick Start

### Prerequisites

- Python 3.10+
- [LibreOffice](https://www.libreoffice.org/download/) (required for Office format conversions)

### Setup

```bash
# Clone
git clone https://github.com/your-username/ztransfer.git
cd ztransfer

# Install Python dependencies
pip install -r backend/requirements.txt

# Start the server
python backend/app.py
```

The API runs at `http://localhost:8000`.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/formats` | List supported conversion pairs |
| `POST` | `/convert?target=pdf` | Upload file and convert |

### Usage Example

```bash
# Convert docx to pdf
curl -X POST "http://localhost:8000/convert?target=pdf" \
  -F "file=@document.docx" \
  -o output.pdf

# Convert image to pdf
curl -X POST "http://localhost:8000/convert?target=pdf" \
  -F "file=@photo.jpg" \
  -o output.pdf
```

## WeChat Mini Program

The `miniprogram/` directory contains the WeChat Mini Program frontend.

1. Open [WeChat DevTools](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. Import the `miniprogram/` directory
3. Replace `appid` in `project.config.json` with your AppID
4. Update `apiBase` in `app.js` to your backend URL

## Project Structure

```
ztransfer/
├── backend/
│   ├── app.py              # FastAPI entry point
│   ├── config.py           # Configuration
│   ├── converters/
│   │   ├── office.py       # LibreOffice wrapper
│   │   └── image.py        # Image to PDF/Word
│   ├── uploads/            # Temp uploads (gitignored)
│   └── outputs/            # Temp outputs (gitignored)
├── miniprogram/            # WeChat Mini Program
│   ├── app.js / app.json / app.wxss
│   ├── pages/index/        # Main page
│   └── utils/api.js        # API helper
└── README.md
```

## License

MIT
