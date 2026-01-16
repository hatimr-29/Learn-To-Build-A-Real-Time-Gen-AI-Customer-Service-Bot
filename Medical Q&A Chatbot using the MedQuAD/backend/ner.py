
import re
from typing import Dict, List


SYMPTOM_KEYWORDS = {
    "fever", "cough", "headache", "nausea", "vomiting", "fatigue", "tiredness",
    "pain", "chest pain", "shortness of breath", "dizziness", "rash",
    "diarrhea", "constipation", "bleeding", "sore throat"
}

DISEASE_KEYWORDS = {
    "cancer", "breast cancer", "lung cancer", "diabetes", "type 1 diabetes",
    "type 2 diabetes", "hypertension", "high blood pressure", "asthma",
    "stroke", "heart attack", "myocardial infarction", "covid-19",
    "coronavirus", "flu", "influenza", "arthritis", "depression"
}

TREATMENT_KEYWORDS = {
    "chemotherapy", "radiation therapy", "radiotherapy", "surgery", "operation",
    "insulin", "metformin", "antibiotic", "antibiotics", "vaccine", "vaccination",
    "physical therapy", "physiotherapy", "radiation", "tablet", "injection",
    "dose", "dosage", "therapy", "medication", "drug"
}


def _find_keywords(text: str, keywords: set) -> List[str]:
    text_l = text.lower()
    found = set()

    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, text_l):
            found.add(kw)

    return sorted(found)


def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """Very basic keyword-based entity extraction."""
    if not text:
        return {"symptoms": [], "diseases": [], "treatments": []}

    symptoms = _find_keywords(text, SYMPTOM_KEYWORDS)
    diseases = _find_keywords(text, DISEASE_KEYWORDS)
    treatments = _find_keywords(text, TREATMENT_KEYWORDS)

    return {
        "symptoms": symptoms,
        "diseases": diseases,
        "treatments": treatments,
    }
