import sys
import os
import pytest
import shutil
from fastapi.testclient import TestClient

# --- THE BRIDGE: Injecting the backend directory into the Python Path ---
# This allows the test to "see" main.py, processor.py, and database.py
current_dir = os.path.dirname(__file__)
backend_path = os.path.abspath(os.path.join(current_dir, "..", "backend"))
sys.path.insert(0, backend_path)

# Now we can import the app object from main.py
from main import app 

client = TestClient(app)

# Use 'manuscript' to match your main.py MANUSCRIPT_DIR
TEST_MANUSCRIPT_DIR = "manuscript"

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Manages the lifecycle of the test environment."""
    # Ensure the manuscript directory exists before tests
    if not os.path.exists(TEST_MANUSCRIPT_DIR):
        os.makedirs(TEST_MANUSCRIPT_DIR)
    yield
    # Optional: Clean up specific test project folders after run
    # test_project_path = os.path.join(TEST_MANUSCRIPT_DIR, "TestProject")
    # if os.path.exists(test_project_path):
    #     shutil.rmtree(test_project_path)

# --- BATTERY 1: LOCAL-FIRST FILE PERSISTENCE ---

def test_file_saving_and_directory_logic():
    """Verify Seshat creates nested directories and saves the .md file correctly."""
    payload = {
        "project": "TestProject",
        "subfolder": "Arc_1",
        "filename": "Opening_Scene",
        "content": "Eldrin stood upon the Iron Peaks."
    }
    
    response = client.post("/process_session", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "Success"
    
    # Verification of physical file (The Local-First Proof)
    expected_path = os.path.join(TEST_MANUSCRIPT_DIR, "TestProject", "Arc_1", "Opening_Scene.md")
    assert os.path.exists(expected_path), f"File not found at {expected_path}"
    
    with open(expected_path, "r", encoding="utf-8") as f:
        assert f.read() == "Eldrin stood upon the Iron Peaks."

def test_list_chapters_endpoint():
    """Verify that the /list_chapters endpoint sees the newly created file."""
    response = client.get("/list_chapters")
    assert response.status_code == 200
    
    # Path is relative to the manuscript folder
    expected_rel_path = os.path.join("TestProject", "Arc_1", "Opening_Scene.md")
    assert expected_rel_path in response.json()["chapters"]

# --- BATTERY 2: NLP & LORE REGISTRY (THE ELDRIN FIX) ---

def test_lore_registration_endpoint():
    """Verify we can teach the brain new names via the Registry."""
    # Matches your LoreEntry model: name and type
    payload = {"name": "Eldrin", "type": "PERSON"}
    response = client.post("/register_lore", json=payload)
    
    assert response.status_code == 200
    assert "registered as PERSON" in response.json()["message"]

def test_analysis_payload_structure():
    """Ensure the analysis return has the keys needed for the UI sidebar."""
    payload = {
        "project": "NLP_Test",
        "subfolder": "",
        "filename": "test_nlp",
        "content": "Eldrin went to the Citadel."
    }
    response = client.post("/process_session", json=payload)
    
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    
    # Check for the keys your processor.py returns to bible_data
    assert "characters" in analysis
    assert "places" in analysis
    assert "events" in analysis

# --- BATTERY 3: SYSTEM RESILIENCE ---

def test_load_nonexistent_chapter():
    """Ensure a 404 is returned for files that don't exist."""
    response = client.get("/load_chapter/fake_project/missing_file.md")
    assert response.status_code == 404

def test_filename_sanitization():
    """Verify that filenames with illegal characters are cleaned."""
    payload = {
        "project": "SanityTest",
        "subfolder": "",
        "filename": "Bad/File?Name", 
        "content": "Testing sanitization logic."
    }
    response = client.post("/process_session", json=payload)
    assert response.status_code == 200
    
    # Your code strips / and ? so BadFileName.md is the expected output
    saved_name = response.json()["saved_to"]
    assert "BadFileName.md" in saved_name