# 📄 PDFTextify

### ✨ Transform Your PDFs into Searchable, Text-Extractable Documents ✨

*A powerful, fast, and elegant OCR service built with FastAPI*

---

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
- 🔧 **Easy Deploy** - Systemd service support

</td>
</tr>
</table>

---

## 🛠️ Installation

### 1️⃣ Clone & Navigate
```bash
git clone https://github.com/imrosyd/pdftextify.git
cd pdftextify
```

### 2️⃣ Install Dependencies
```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install -y ocrmypdf tesseract-ocr tesseract-ocr-ind tesseract-ocr-eng

# Python dependencies
pip install -r requirements.txt
```

### 3️⃣ Run for Development
```bash
uvicorn app:app --host 0.0.0.0 --port 1100
```
🎉 **That's it!** Open http://localhost:1100 in your browser. For production, see the [Deployment](#-deployment) section.

---

## 🚀 Deployment

### Using systemd (Recommended on Linux)

To run the application as a systemd service, create a file named `pdftextify.service` in `/etc/systemd/system/` with the following content.

**Important:** You must replace `your_user` and `your_group` with your actual username and group, and ensure the `WorkingDirectory` and `ExecStart` paths are correct for your environment.

```ini
[Unit]
Description=PDFTextify Service
After=network.target

[Service]
User=your_user
Group=your_group
WorkingDirectory=/path/to/your/pdftextify_project
ExecStart=/path/to/your/venv/bin/uvicorn app:app --host 0.0.0.0 --port 1100
Restart=always

[Install]
WantedBy=multi-user.target
```

After creating the file, run the following commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now pdftextify.service
```

#### Manage the Service:
- **Check Status:** `sudo systemctl status pdftextify.service`
- **View Logs:** `journalctl -u pdftextify.service -f`
- **Stop/Start:** `sudo systemctl stop/start pdftextify.service`

### Using Gunicorn
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:1100
```

---

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

---
## ⚙️ Configuration

### Directory Structure

```
pdftextify/
├── app.py
├── logs/
├── pdfs/
├── src/
│   └── pdftextify/
│       ├── __init__.py
│       ├── main.py
│       └── static/
├── tests/
├── tools/
└── README.md, LICENSE, ...
```

 * `app.py` – Entry point that bootstraps the package in `src/`.
 * `logs/` – Runtime log output (created automatically).
 * `pdfs/` – (Future use) Storage for raw and final PDFs.
 * `src/pdftextify/` – The main application package (FastAPI app, static files, etc.).
 * `tests/` - Unit and integration tests (contains sample `test.pdf`).
 * `tools/` - Additional tools used by the project.
 * `cache/`, `temp/` – Generated artefacts; safe to purge when not running.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Bug Reports
Found a bug? [Open an issue](https://github.com/imrosyd/pdftextify/issues) with a clear description, steps to reproduce, and environment details.

### 💡 Feature Requests
Have an idea? [Start a discussion](https://github.com/imrosyd/pdftextify/discussions) or [open an issue](https://github.com/imrosyd/pdftextify/issues).

### 🔧 Development
1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✅ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
5. 📫 Open a Pull Request

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

 * 🔍 OCRmyPDF: For excellent OCR processing capabilities
 * 🐍 FastAPI: For the robust web framework
 * 🎨 Tesseract: For reliable text recognition
