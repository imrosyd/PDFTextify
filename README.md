<div align="center">

# 📄 PDFTextify

### ✨ Transform Your PDFs into Searchable, Text-Extractable Documents ✨

*A powerful, fast, and elegant OCR service built with FastAPI*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-orange.svg)](https://github.com/tesseract-ocr/tesseract)

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🛠️ Installation](#%EF%B8%8F-installation) • [💡 Usage](#-usage) • [🤝 Contributing](#-contributing)

---

</div>

## 🎯 What is PDFTextify?

PDFTextify is a **modern OCR service** that transforms your scanned PDFs into fully searchable, text-extractable documents. Built with **FastAPI** and powered by **OCRmyPDF**, it offers both a beautiful web interface and a robust REST API.

<div align="center">

### 🌟 Perfect for:
**📚 Document Archives** • **📋 Business Reports** • **📄 Legal Documents** • **🎓 Academic Papers**

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔥 **Core Features**
- 🌐 **Dual Language OCR** - Indonesian & English support
- 🎨 **Modern Web Interface** - Clean, responsive design
- ⚡ **REST API** - Easy integration
- 🔄 **Auto Enhancement** - Rotation, deskew, upsampling
- 📁 **PDF/A-2 Output** - Archival quality format

</td>
<td width="50%">

### 🚀 **Technical Excellence**
- ⚡ **High Performance** - 300 DPI processing
- 🛡️ **Secure** - Input validation & error handling
- 📱 **Responsive** - Works on all devices
- 🌙 **Dark Mode** - Automatic theme switching
- 🔧 **Easy Deploy** - Single script startup

</td>
</tr>
</table>

## 🚀 Quick Start

Get PDFTextify running in **3 simple steps**:

### 1️⃣ Clone & Navigate
```bash
git clone https://github.com/imrosyd/PDFTextify.git
cd PDFTextify
```

### 2️⃣ Install Dependencies
```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install -y ocrmypdf tesseract-ocr tesseract-ocr-ind tesseract-ocr-eng

# Python dependencies
pip install -r requirements.txt
```

### 3️⃣ Launch
```bash
./start-pdftextify.sh
```

🎉 **That's it!** Open http://localhost:1100 in your browser

## 🛠️ Installation

<details>
<summary><b>📋 System Requirements</b></summary>

- **Python** 3.7 or higher
- **OCRmyPDF** - PDF processing engine
- **Tesseract OCR** - Text recognition engine
- **2GB RAM** minimum (4GB recommended)
- **1GB** free disk space

</details>

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ocrmypdf tesseract-ocr tesseract-ocr-ind tesseract-ocr-eng
pip install -r requirements.txt
```

### macOS
```bash
brew install ocrmypdf tesseract tesseract-lang
pip install -r requirements.txt
```

### Docker (Coming Soon)
```bash
docker run -p 1100:1100 pdftextify/app
```

## 💡 Usage

### 🌐 Web Interface
1. Open http://localhost:1100
2. Drag & drop your PDF or click to browse
3. Click **"Process PDF"**
4. Download your searchable PDF!

### 🔌 API Integration

#### Upload PDF for Processing
```bash
curl -X POST "http://localhost:1100/ocrpdf/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf" \
     --output searchable_document.pdf
```

#### Python Example
```python
import requests

url = "http://localhost:1100/ocrpdf/"
files = {"file": open("document.pdf", "rb")}
response = requests.post(url, files=files)

with open("searchable_document.pdf", "wb") as f:
    f.write(response.content)
```

#### JavaScript Example
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/ocrpdf/', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'processed.pdf';
    a.click();
});
```

## 📊 API Reference

### Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Web interface | HTML page |
| `POST` | `/ocrpdf/` | Process PDF | Processed PDF file |
| `GET` | `/ocrpdf/` | API info | JSON response |

### Request Format
- **Content-Type**: `multipart/form-data`
- **Field Name**: `file`
- **File Type**: PDF only
- **Max Size**: 50MB

### Response Codes
- `200` - Success
- `400` - Invalid file format
- `413` - File too large
- `500` - Processing error

## ⚙️ Configuration

### Environment Variables
```bash
export PDFTEXTIFY_HOST=0.0.0.0
export PDFTEXTIFY_PORT=1100
export PDFTEXTIFY_MAX_FILE_SIZE=52428800  # 50MB
```

### CORS Settings
Edit `main.py` to configure allowed origins:
```python
allow_origins=[
    "http://localhost:1100",
    "http://127.0.0.1:1100",
    "https://yourdomain.com",  # Add your domain
]
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Load testing:
```bash
pip install locust
locust -f tests/load_test.py
```

## 🚀 Deployment

### Production Setup
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:1100
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:1100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Bug Reports
Found a bug? [Open an issue](https://github.com/imrosyd/PDFTextify/issues) with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information

### 💡 Feature Requests
Have an idea? [Start a discussion](https://github.com/imrosyd/PDFTextify/discussions) or [open an issue](https://github.com/imrosyd/PDFTextify/issues).

### 🔧 Development
```bash
git clone https://github.com/imrosyd/PDFTextify.git
cd PDFTextify
pip install -r requirements.txt
# Make your changes
# Test your changes
# Submit a pull request
```

## 📈 Roadmap

- [ ] 🐳 **Docker Support** - Easy containerized deployment
- [ ] 🌍 **Multi-language OCR** - Support for more languages
- [ ] 📊 **Batch Processing** - Handle multiple files
- [ ] 🔄 **Queue System** - Background job processing
- [ ] 📱 **Mobile App** - iOS and Android support
- [ ] 🤖 **AI Enhancement** - ML-powered text recognition
- [ ] 📧 **Email Integration** - Send results via email
- [ ] ☁️ **Cloud Storage** - S3, Google Drive integration

## 📞 Support

<div align="center">

### Need Help?

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](https://github.com/imrosyd/PDFTextify/issues)
[![Discussions](https://img.shields.io/badge/GitHub-Discussions-blue?style=for-the-badge&logo=github)](https://github.com/imrosyd/PDFTextify/discussions)

### Connect with the Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-imrosyd-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/imrosyd)
[![Instagram](https://img.shields.io/badge/Instagram-imrosyd-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/imrosyd)

</div>

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

<div align="center">

---

### ⭐ Star this repo if PDFTextify helped you!

**Made with ❤️ by [imrosyd](https://github.com/imrosyd)**

*Transform your PDFs today with PDFTextify!*

</div>