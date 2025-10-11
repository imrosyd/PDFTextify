"""
Main application file for the PDFTextify API.

This file contains the FastAPI application, API endpoints, and OCR processing logic.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import tempfile, subprocess, os, shutil, pathlib

# Define the base directory and the static directory
BASE_DIR = pathlib.Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Create the FastAPI application
app = FastAPI(title="PDFTextify API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1100",
        "http://127.0.0.1:1100",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """
    Serve the index.html file as the root page.
    """
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return HTMLResponse(content=index.read_text(encoding="utf-8"))


@app.options("/ocrpdf")
@app.options("/ocrpdf/")
def ocrpdf_options():
    """
    Handle OPTIONS requests for the /ocrpdf/ endpoint.
    """
    return Response(status_code=204)


@app.get("/ocrpdf")
@app.get("/ocrpdf/")
def ocrpdf_info():
    """
    Provide information about how to use the /ocrpdf/ endpoint.
    """
    return {"detail": "Use POST multipart form-data with 'file' field containing PDF."}


@app.post("/ocrpdf/")
async def ocrpdf(file: UploadFile = File(...)):
    """
    Process a PDF file with OCR and return the processed file.
    """
    # Check if the uploaded file is a PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be PDF")

    # Set up the environment for the OCR process
    env = os.environ.copy()
    project_dir = BASE_DIR.parent
    jbig2_dir = project_dir / "tools" / "jbig2enc"
    if jbig2_dir.is_dir():
        path_value = env.get("PATH", "")
        env["PATH"] = (
            os.pathsep.join([str(jbig2_dir), path_value])
            if path_value
            else str(jbig2_dir)
        )

        ld_value = env.get("LD_LIBRARY_PATH", "")
        env["LD_LIBRARY_PATH"] = (
            os.pathsep.join([str(jbig2_dir), ld_value]) if ld_value else str(jbig2_dir)
        )

    # Find the ocrmypdf executable
    ocrmypdf_bin = shutil.which("ocrmypdf", path=env.get("PATH"))
    if not ocrmypdf_bin:
        raise HTTPException(status_code=500, detail="ocrmypdf not found in PATH")

    # Create a temporary directory to store the input and output files
    with tempfile.TemporaryDirectory() as tmpdir:
        inp = os.path.join(tmpdir, "input.pdf")
        outp = os.path.join(tmpdir, "output.pdf")

        # Save the uploaded file to the temporary directory
        data = await file.read()
        with open(inp, "wb") as f:
            f.write(data)

        # Define the command to run OCRmyPDF
        cmd = [
            ocrmypdf_bin,
            "--language",
            "ind+eng",
            "--rotate-pages",
            "--deskew",
            "--oversample",
            "300",
            "--optimize",
            "3",
            "--output-type",
            "pdfa-2",
            "--force-ocr",
            inp,
            outp,
        ]
        try:
            # Run the OCRmyPDF command
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,
                env=env,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Subprocess error: {e}")

        # Check if the OCR process was successful
        if res.returncode != 0 or not os.path.exists(outp):
            err = (res.stderr or res.stdout or "").strip()[:4000]
            raise HTTPException(status_code=500, detail=f"OCR failed: {err}")

        # Read the processed PDF file
        pdf_bytes = pathlib.Path(outp).read_bytes()

    # Define the output filename
    outname = f'{file.filename.rsplit(".",1)[0]}_ocr.pdf'
    # Return the processed PDF file as a response
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{outname}"'},
    )