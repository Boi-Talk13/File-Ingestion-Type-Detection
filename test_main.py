import pytest
from fastapi.testclient import TestClient
from main import app, uploaded_hashes
import io
import zipfile

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_hashes():
    """Clears the global hash set before each test to ensure isolation."""
    uploaded_hashes.clear()

def test_serve_index():
    """Tests if the homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert "File Ingestion & Type Detection" in response.text

def test_upload_regular_file():
    """Tests uploading a single standard text file."""
    file_content = b"Hello world"
    files = [("files", ("test.txt", file_content, "text/plain"))]
    
    response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["file_name"] == "test.txt"
    assert data[0]["file_type"] == "txt"
    assert data[0]["duplicate"] is False

def test_upload_duplicate_file():
    """Tests that uploading the same content twice marks the second as a duplicate."""
    file_content = b"Unique content"
    file_info = ("files", ("file1.txt", file_content, "text/plain"))
    
    # First upload
    client.post("/upload", files=[file_info])
    
    # Second upload (same content)
    response = client.post("/upload", files=[file_info])
    data = response.json()
    
    assert data[0]["duplicate"] is True

def test_upload_zip_file():
    """Tests the extraction and validation of files inside a ZIP archive."""
    # Create a dummy ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("inner1.txt", b"Inside zip 1")
        zip_file.writestr("inner2.pdf", b"%PDF-1.4 dummy content")
        
    zip_buffer.seek(0)
    files = [("files", ("archive.zip", zip_buffer.read(), "application/zip"))]
    
    response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should contain 3 records: 1 for the ZIP itself, 2 for the contents
    assert len(data) == 3
    filenames = [item["file_name"] for item in data]
    assert "archive.zip" in filenames
    assert "inner1.txt" in filenames
    assert "inner2.pdf" in filenames

def test_upload_empty_file():
    """Tests that empty files are rejected as per logic in main.py."""
    files = [("files", ("empty.txt", b"", "text/plain"))]
    
    response = client.post("/upload", files=files)
    data = response.json()
    
    assert data[0]["status"] == "rejected"

def test_file_type_detection_logic():
    """Tests that magic/mimetypes correctly identify specific formats."""
    # Testing an Image
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" # Partial PNG header
    files = [("files", ("picture.png", image_content, "image/png"))]
    
    response = client.post("/upload", files=files)
    data = response.json()
    
    assert data[0]["file_type"] == "image"
    assert "image/png" in data[0]["mime_type"]