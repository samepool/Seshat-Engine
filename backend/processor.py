import spacy
from spacy.pipeline import EntityRuler
import sqlite3

nlp = spacy.load("en_core_web_sm")
#Core English model

def load_custom_entities():
    """Reads the 'Galbark' names from the database to prime the brain."""
    conn = sqlite3.connect("seshat_bible.db")
    cursor = conn.cursor()
    patterns = []
    try:
        #We look for names you've manually registered
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
    # This ensures Galbark is always a PERSON
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        ruler = nlp.get_pipe("entity_ruler")

        patterns = load_custom_entities()
        ruler.clear()
        ruler.add_patterns(patterns)

        doc = nlp(text)

        analysis = {
            "characters": [],
            "place": [],
            "events": []
        }

        # 2. Extract Entities
        for ent in doc.ents:
            if ent.label_=="PERSON":
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
                
            return analysis