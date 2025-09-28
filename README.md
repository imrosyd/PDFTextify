# PDFTextify

PDFTextify is a FastAPI-based OCR service that converts PDF files to searchable PDFs using OCRmyPDF.

## Features

- PDF OCR processing with Indonesian and English language support
- Web interface for file upload
- REST API endpoint
- Automatic image enhancement
- PDF/A-2 output format

## Requirements

- Python 3.7+
- OCRmyPDF
- Tesseract OCR

## Installation

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ocrmypdf tesseract-ocr tesseract-ocr-ind tesseract-ocr-eng

# macOS
brew install ocrmypdf tesseract tesseract-lang
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the server:
```bash
# Using the startup script
./start-pdftextify.sh

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 1100
```

### API Endpoints

- `GET /` - Web interface
- `POST /ocrpdf/` - Upload PDF for OCR processing

### Example API usage:
```bash
curl -X POST "http://localhost:1100/ocrpdf/" \
     -H "accept: application/pdf" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your-file.pdf" \
     --output result_ocr.pdf
```

## Configuration

The service supports CORS configuration for development and production environments.

## License

Apache License 2.0