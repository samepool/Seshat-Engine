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

    # 1. Extract Characters and Places using Named Entity Recognition
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text not in analysis["characters"]:
                analysis["characters"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC", "FAC"]:
            if ent.text not in analysis["places"]:
                analysis["places"].append(ent.text)

    # 2. Extract 'Significance' / Events
    # We look for 'ROOT' verbs (the main action of a sentence)
    for sent in doc.sents:
        action = None
        for token in sent:
            if token.dep_ == "ROOT": # The main verb
                action = token.text

    # Create a summary entry for this sentence\
        analysis["events"].append({
         "context": sent.text.strip(),
         "main_action": action
    })
    
    return analysis

# Test run
if __name__ == "__main__":
    test_text = "Mark walked down Briton Beach towards Lefton. Sheri met Mark in Lefton Square."

