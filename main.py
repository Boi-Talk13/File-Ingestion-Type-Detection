from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import hashlib
import zipfile
import io
from datetime import datetime, timezone
import magic
import mimetypes
import json

# ======================================================
# APP
# ======================================================
app = FastAPI(title="File Ingestion & Validation Portal")

# ======================================================
# CORS
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# STATIC FILES
# ======================================================
app.mount("/static", StaticFiles(directory="."), name="static")

# ======================================================
# CONSTANTS
# ======================================================
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
uploaded_hashes = set()

# ======================================================
# UTILITIES
# ======================================================
def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def base_record(name: str):
    return {
        "file_name": name,
        "file_type": None,
        "size_kb": None,
        "hash": None,
        "status": None,
        "mime_type": None,
        "uploaded_at": utc_now(),
        "duplicate": None,
        "scan_status": None
    }

def is_valid_zip_entry(name: str, content: bytes) -> bool:
    if name.startswith("__MACOSX/"):
        return False
    if name.split("/")[-1].startswith("._"):
        return False
    if len(content) == 0:
        return False
    return True

# ======================================================
# FILE TYPE DETECTION (FIXED ✅)
# ======================================================
def detect_file_type(name: str, content: bytes):
    name_lower = name.lower()

    # ✅ 1. EXTENSION FIRST (MOST RELIABLE FOR JSON)
    if name_lower.endswith(".json"):
        return "json", "application/json"

    # 2. MIME DETECTION
    detected_mime = magic.Magic(mime=True).from_buffer(content)
    ext_mime, _ = mimetypes.guess_type(name)
    final_mime = detected_mime or ext_mime or "application/octet-stream"

    if final_mime == "application/pdf":
        return "pdf", final_mime

    if "wordprocessingml" in final_mime:
        return "docx", final_mime

    if "spreadsheetml" in final_mime:
        return "excel", final_mime

    if "presentationml" in final_mime:
        return "ppt", final_mime

    if final_mime == "text/plain":
        return "txt", final_mime

    if final_mime == "text/csv":
        return "csv", final_mime

    if final_mime.startswith("image/"):
        return "image", final_mime

    return "unknown", final_mime

# ======================================================
# FILE PROCESSING
# ======================================================
def process_regular_file(name: str, content: bytes):
    record = base_record(name)

    file_type, mime_type = detect_file_type(name, content)
    file_hash = sha256(content)

    duplicate = file_hash in uploaded_hashes
    if not duplicate:
        uploaded_hashes.add(file_hash)

    record.update({
        "file_type": file_type,
        "size_kb": round(len(content) / 1024, 2),
        "hash": file_hash,
        "status": "validated",
        "mime_type": mime_type,
        "duplicate": duplicate,
        "scan_status": "clean"
    })

    # ✅ OPTIONAL: JSON CONTENT VALIDATION
    if file_type == "json":
        try:
            json.loads(content.decode("utf-8"))
        except Exception:
            record["status"] = "rejected"
            record["scan_status"] = "invalid_json"

    return record

# ======================================================
# ROUTES (HTML)
# ======================================================
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/login.html", response_class=HTMLResponse)
def serve_login():
    with open("login.html", encoding="utf-8") as f:
        return f.read()

@app.get("/signup.html", response_class=HTMLResponse)
def serve_signup():
    with open("signup.html", encoding="utf-8") as f:
        return f.read()

# ======================================================
# FILE UPLOAD API
# ======================================================
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        content = await file.read()
        record = base_record(file.filename)

        if not content or len(content) > MAX_FILE_SIZE:
            record.update({
                "status": "rejected",
                "scan_status": "not_applicable"
            })
            results.append(record)
            continue

        filename_lower = file.filename.lower()

        # ZIP HANDLING
        if filename_lower.endswith(".zip"):
            try:
                zip_data = zipfile.ZipFile(io.BytesIO(content))

                record.update({
                    "file_type": "zip",
                    "size_kb": round(len(content) / 1024, 2),
                    "hash": sha256(content),
                    "status": "container",
                    "mime_type": "application/zip",
                    "duplicate": False,
                    "scan_status": "clean"
                })
                results.append(record)

                for inner_name in zip_data.namelist():
                    if inner_name.endswith("/"):
                        continue

                    inner_content = zip_data.read(inner_name)
                    if not is_valid_zip_entry(inner_name, inner_content):
                        continue

                    results.append(process_regular_file(inner_name, inner_content))

                continue

            except zipfile.BadZipFile:
                record.update({
                    "status": "rejected",
                    "scan_status": "not_applicable"
                })
                results.append(record)
                continue

        # ALL OTHER FILES
        results.append(process_regular_file(file.filename, content))

    return results
