# File Ingestion Type Detection

A single-page web application for uploading and analyzing files with automatic type detection, hashing, duplicate detection, and metadata extraction.

This project is a **pipeline demonstration**, not a hardened production system.

---

## Overview

This application allows users to upload multiple files from a single interface.  
Each uploaded file is processed by the backend to extract useful metadata such as file type, MIME type, size, hash value, and duplicate status.

All results are displayed on the same page without navigation or reloads.

---

## Features

- Single-page user interface
- Multiple file upload support
- Drag-and-drop file upload
- Automatic file type detection
- MIME type identification
- SHA-256 hash generation
- Duplicate file detection
- File size calculation
- ZIP file handling
- Scan-status placeholder for future virus scanning

---

## Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn
- python-magic
- hashlib
- mimetypes
- zipfile

### Frontend
- HTML
- CSS
- JavaScript

---

## Application Flow

1. User opens the application
2. Selects or drags files into the upload area
3. Clicks the upload button
4. Files are sent to the `/upload` API endpoint
5. Backend processes each file:
   - Reads file content
   - Detects MIME type
   - Generates SHA-256 hash
   - Checks for duplicates
   - Collects metadata
6. Results are returned as JSON
7. Output is displayed on the same page

---

## Project Structure

File-Ingestion-Type-Detection  
├── main.py  
├── index.html  
├── style.css  
├── app.js  
└── README.md  

---

## Installation

### Clone the repository

git clone https://github.com/your-username/File-Ingestion-Type-Detection.git  
cd File-Ingestion-Type-Detection  

### Create and activate virtual environment

python3 -m venv venv  
source venv/bin/activate  

### Install dependencies

pip install fastapi uvicorn python-magic  

macOS users may also need:

brew install libmagic  

---

## Running the Application

uvicorn main:app --reload  

Open your browser and visit:

http://127.0.0.1:8000  

---

## API Endpoint

### POST /upload

**Request**
- multipart/form-data
- Field name: `files`
- Supports multiple files

**Response Fields**
- file_name
- file_type
- size_kb
- hash
- status
- mime_type
- uploaded_at
- duplicate
- scan_status

---

## Limitations

- No persistent storage
- No authentication or authorization
- No real malware scanning
- No rate limiting
- No sandboxing of uploaded files

---

## Future Enhancements

- Database integration (PostgreSQL or MongoDB)
- JWT-based authentication
- Virus scanning using ClamAV
- Cloud object storage (S3 or GCS)
- Rate limiting and request validation
- Background processing with Celery or RQ

---

## Deployment Notes

- Frontend and backend run together locally
- For production deployment:
  - Backend: Render, Railway, Fly.io, or VPS
  - Frontend: Vercel or Netlify (static only)

Note: Vercel does not run FastAPI directly.

---

## License

MIT License  

This project is intended for academic, demo, and prototype use.
