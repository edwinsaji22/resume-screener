import spacy
from skills_db import SKILLS_DB

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    text_lower = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text_lower]
    return list(set(found_skills))

def extract_entities(text):
    doc = nlp(text)
    entities = {"ORG": [], "PERSON": [], "DATE": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def extract_education(text):
    edu_keywords = ["bachelor", "master", "mca", "bca", "b.tech", "m.tech", "phd", "degree"]
    text_lower = text.lower()
    found = [kw for kw in edu_keywords if kw in text_lower]
    return found