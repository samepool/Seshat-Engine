import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .processor import analyze_writing # This connects Processer.py to the sytem
from .database import save_entity, save_event, initialize_db

app = FastAPI (title="Seshat Engine")

initialize_db()

# --- CORS MIDDLEWARE ---
# This allows the HTML/JS frontened to talk to this Python Server
# without being blocked by browser security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Ensure our manuscript storage folder exists
MANUSCRIPT_DIR = 'manuscript'
if not os.path.exists(MANUSCRIPT_DIR):
    os.makedirs(MANUSCRIPT_DIR)

# Data structure for incoming writing sessions
class WritingSession(BaseModel):
    filename: str
    content: str

@app.get("/")
async def root():
    return {"message": "Seshat Backend is Online"}

@app.post("/process_session")
async def process_session(session: WritingSession):
    """
    The Core Workflow:
    1. Sanitize and Save the .md file.
    2. Analyze the text for Who, What, Where, and Significance
    """

    safe_name = "".join([c for c in session.filename if c.isalnum() or c in (' ', '.', '_')]).strip()
    if not (safe_filename_endswith := safe_name.lower().endswith(".md")):
        safe_name += ".md"
    
    file_path = os.path.join(MANUSCRIPT_DIR, safe_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(session.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")
    
    #---Step B: The Key (The 'Brain' requirement) ---
    # Pass the raw text to SpaCy for NLP analysis
    bible_data = analyze_writing(session.content)

    # --- STEP C: Persistence (The 'World Bible' requirement) ---
    # Save extracted characters
    for char in bible_data["characters"]:
        save_entity("person", char)

    #Save extracted Places
    for place in bible_data["places"]:
        save_entity("place", place)
    
    #Save extracted Events (Significance)
    for event in bible_data["events"]:
        # event["main_action"] comes from the 'ROOT' verb logic in processor.py
        save_event(event["context"], event["main_action"])
    
    # REturn the analysis immediately to update the Frontend Sidebar
    return {
       "status": "Success",
       "saved_to": safe_name,
       "analysis": bible_data 
    }