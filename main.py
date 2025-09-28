from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import tempfile, subprocess, os, shutil, pathlib

app = FastAPI(title="PDFTextify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1100",
        "http://127.0.0.1:1100",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    index = pathlib.Path("static/index.html")
    if not index.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return HTMLResponse(content=index.read_text(encoding="utf-8"))

@app.options("/ocrpdf")
@app.options("/ocrpdf/")
def ocrpdf_options():
    return Response(status_code=204)

@app.get("/ocrpdf")
@app.get("/ocrpdf/")
def ocrpdf_info():
    return {"detail": "Use POST multipart form-data with 'file' field containing PDF."}

@app.post("/ocrpdf/")
async def ocrpdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be PDF")

    ocrmypdf_bin = shutil.which("ocrmypdf")
    if not ocrmypdf_bin:
        raise HTTPException(status_code=500, detail="ocrmypdf not found in PATH")

    with tempfile.TemporaryDirectory() as tmpdir:
        inp = os.path.join(tmpdir, "input.pdf")
        outp = os.path.join(tmpdir, "output.pdf")

        # Save uploaded file
        data = await file.read()
        with open(inp, "wb") as f:
            f.write(data)

        # Run OCR processing
        cmd = [
            ocrmypdf_bin,
            "--language", "ind+eng",
            "--rotate-pages", "--deskew",
            "--oversample", "300",
            "--optimize", "3",
            "--output-type", "pdfa-2",
            "--force-ocr",
            inp, outp,
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Subprocess error: {e}")

        if res.returncode != 0 or not os.path.exists(outp):
            err = (res.stderr or res.stdout or "").strip()[:4000]
            raise HTTPException(status_code=500, detail=f"OCR failed: {err}")

        pdf_bytes = pathlib.Path(outp).read_bytes()

    outname = f'{file.filename.rsplit(".",1)[0]}_ocr.pdf'
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{outname}"'}
    )
