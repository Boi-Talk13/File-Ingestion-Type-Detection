import pytest
import os
from fastapi.testclient import TestClient
from main import app, uploaded_hashes

client = TestClient(app)

# Configuration
TEST_FOLDER = "Test"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clears state before each test."""
    uploaded_hashes.clear()
    yield

# ======================================================
# 1. LIVE DATA INPUT (Your Folder)
# ======================================================
def test_upload_live_data_folder():
    """Iterates through My_files and prints results to CLI."""
    print(f"\n{'='*80}\nLIVE DATA TEST: Processing folder '{TEST_FOLDER}'\n{'='*80}")
    
    if not os.path.exists(TEST_FOLDER):
        pytest.fail(f"Directory '{TEST_FOLDER}' not found. Did you rebuild the Docker image?")

    files = [f for f in os.listdir(TEST_FOLDER) if os.path.isfile(os.path.join(TEST_FOLDER, f))]
    
    for filename in files:
        file_path = os.path.join(TEST_FOLDER, filename)
        with open(file_path, "rb") as f:
            response = client.post("/upload", files=[("files", (filename, f.read()))])
            assert response.status_code == 200
            data = response.json()
            
            for res in data:
                print(f"[LIVE] File: {res['file_name']:<25} | Type: {str(res['file_type']):<10} | Status: {res['status']}")

# ======================================================
# 2. POSITIVE TESTS
# ======================================================
def test_upload_valid_pdf():
    """Tests a standard PDF file ingestion."""
    content = b"%PDF-1.4 dummy content"
    response = client.post("/upload", files=[("files", ("test.pdf", content))])
    assert response.status_code == 200
    assert response.json()[0]["file_type"] == "pdf"

def test_upload_valid_json():
    """Tests a standard JSON file ingestion."""
    content = b'{"key": "value"}'
    response = client.post("/upload", files=[("files", ("data.json", content))])
    assert response.status_code == 200
    assert response.json()[0]["status"] == "validated"

# ======================================================
# 3. NEGATIVE TESTS
# ======================================================
def test_upload_empty_file():
    """Tests rejection of 0-byte files."""
    response = client.post("/upload", files=[("files", ("empty.txt", b""))])
    # The API returns a list of results
    assert response.json()[0]["status"] == "rejected"

def test_upload_oversized_file():
    """Tests rejection of files exceeding 100MB."""
    large_content = b"0" * (MAX_FILE_SIZE + 1)
    response = client.post("/upload", files=[("files", ("huge.zip", large_content))])
    assert response.json()[0]["status"] == "rejected"

# ======================================================
# 4. EDGE CASES
# ======================================================
def test_duplicate_file_detection():
    """Tests that the same content uploaded twice is flagged as a duplicate."""
    content = b"Unique Content 123"
    client.post("/upload", files=[("files", ("file1.txt", content))])
    response = client.post("/upload", files=[("files", ("file2.txt", content))])
    
    assert response.json()[0]["duplicate"] is True

def test_special_characters_filename():
    """Tests filenames with spaces and symbols."""
    name = "Test @ File # 1.txt"
    content = b"testing symbols"
    response = client.post("/upload", files=[("files", (name, content))])
    assert response.status_code == 200
    assert response.json()[0]["file_name"] == name
