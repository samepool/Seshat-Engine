import spacy
from spacy.pipeline import EntityRuler
import sqlite3

# Core English model
nlp = spacy.load("en_core_web_sm")

def load_custom_entities():
    """Reads the 'Galbark' names from the database to prime the brain."""
    conn = sqlite3.connect("seshat_bible.db")
    cursor = conn.cursor()
    patterns = []
    try:
        # We look for names you've manually registered
        cursor.execute("SELECT name, entity_type FROM custom_lore")
        for row in cursor.fetchall():
            patterns.append({"label": row[1], "pattern": row[0]})
    except:
        pass # Table might not exist yet
    finally:
        conn.close()
    return patterns

def analyze_writing(text: str):
    # 1. Setup Custom Rules (The 'Lore Primer')
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")

    # Always update patterns from the DB
    patterns = load_custom_entities()
    ruler.clear()
    ruler.add_patterns(patterns)

    # CRITICAL: doc = nlp(text) must be out here, NOT indented under 'else'
    doc = nlp(text)

    analysis = {
        "characters": [],
        "places": [], # Fixed: changed from 'place' to 'places'
        "events": []
    }

    # 2. Extract Entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in analysis["characters"]:
                analysis["characters"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC", "FAC"]:
            if ent.text not in analysis["places"]:
                analysis["places"].append(ent.text)

    # 3. Extract Actions (ROOT Verbs)
    for sent in doc.sents:
        action = None
        for token in sent:
            if token.dep_ == "ROOT":
                action = token.lemma_ # Use lemma (walked -> walk)

        analysis["events"].append({
            "context": sent.text.strip(),
            "main_action": action
        })
    
    # Return MUST be at this level (the end of the function)
    return analysis