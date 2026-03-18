import spacy

#Core English model

try:
    nlp =spacy.load("en_core_web_sm")
except OSError:
    #Fallback if model isn't downloaded yet
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def analyze_writing(text: str):
    """
    The 'Key' Logic:
    1. Extracts Entities (Who/Where)
    2. Identifies Actions (What)
    3. Contextualizes Significance
    """
    doc = nlp(text)

    analysis = {
        "characters": [],
        "places": [],
        "events": []
    }

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in analysis["characters"]:
                analysis["characters"].append(ent.text)