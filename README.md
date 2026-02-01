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
- File upload using file picker  
- Automatic file type detection (limited)  
- MIME type identification  
- SHA-256 hash generation  
- Duplicate file detection  
- File size calculation  
- ZIP file handling  
- Scan-status placeholder for future virus scanning  
- Dummy login and signup flow  

---

## 🔐 Login & Signup (Dummy Authentication)

This project includes **Login** and **Signup** pages for demonstration purposes only.

- Authentication is **dummy and client-side only**
- **Any username and password will be accepted**
- No database validation
- No password encryption
- Login state is handled using browser storage

This is **not real authentication** and must **not be used in production**.  
It exists only to simulate UI flow for academic and demo purposes.

---

## ⚠️ Known Limitations in Current Implementation

### JSON File Type Detection
- JSON files are **not correctly recognized**
- File type is shown as **UNKNOWN**
- This happens due to limitations in the file type detection logic
- Content-based JSON inspection is not implemented yet

### Drag and Drop Upload
- Drag-and-drop functionality is **present in the UI**
- However, it is **not fully functional**
- Reliable uploads work only through the file selection button

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
2. (Optional) Logs in using dummy credentials  
3. Selects files using the file picker  
4. Clicks the upload button  
5. Files are sent to the `/upload` API endpoint  
6. Backend processes each file:
   - Reads file content  
   - Attempts MIME type detection  
   - Generates SHA-256 hash  
   - Checks for duplicates  
   - Collects metadata  
7. Results are returned as JSON  
8. Output is displayed on the same page  

---

## Project Structure

File-Ingestion-Type-Detection  
├── main.py  
├── index.html  
├── style.css  
├── app.js  
├── login.html  
├── signup.html  
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

## Positives of the Project

- Clean and simple single-page design  
- Demonstrates a complete file ingestion pipeline  
- Supports multiple file uploads  
- Uses hashing for duplicate detection  
- Modular backend logic, easy to extend  
- Clear separation between frontend and backend  

---

## Negatives of the Project

- JSON file type not properly detected  
- Drag-and-drop upload not fully functional  
- No persistent database storage  
- Dummy authentication only  
- No real malware scanning  
- No rate limiting or request validation  

---

## Future Enhancements / Initiatives

- Proper JSON file detection using content parsing  
- Fully functional drag-and-drop upload support  
- Database integration (PostgreSQL / MongoDB)  
- Real authentication using JWT  
- Virus scanning using ClamAV  
- Cloud object storage (AWS S3 / Google Cloud Storage)  
- Rate limiting and security hardening  
- Background processing using Celery or RQ  
- Detailed upload logs and audit trail  

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

This project is intended for **academic, demo, and prototype use**.
