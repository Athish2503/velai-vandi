import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> list[str]:
    doc = nlp(text.lower())
    return [t.lemma_ for t in doc if not t.is_stop and not t.is_punct and t.pos_ in ("NOUN", "VERB")]
