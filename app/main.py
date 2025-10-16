from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import os, uuid
from .utils import convert_image_local, convert_with_external_api
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Image Converter")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/convert")
async def convert_api(file: UploadFile = File(...), method: str = Form("grayscale"), use_external: bool = Form(False)):
    content = await file.read()
    if use_external and os.getenv("EXTERNAL_AI_PROVIDER", "none").lower() != "none":
        out_bytes = convert_with_external_api(content, {"method": method})
    else:
        out_bytes = convert_image_local(content, method)
    filename = f"{uuid.uuid4().hex}.png"
    with open(os.path.join(TEMP_DIR, filename), "wb") as f:
        f.write(out_bytes)
    return {"url": f"/download/{filename}"}

@app.get("/download/{filename}")
def download(filename: str):
    path = os.path.join(TEMP_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png", filename=filename)
    return {"error": "file not found"}
