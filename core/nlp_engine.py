import spacy
import os

class NLPEngine:
    def __init__(self):
        model_name = "en_core_web_sm"
        try:
            # Try to load the model
            self.nlp = spacy.load(model_name)
        except OSError:
            # If model not found, download it automatically (Fix for Streamlit Cloud)
            import spacy.cli
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)

    def get_basic_entities(self, text):
        doc = self.nlp(text[:100000])
        entities = {
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
            "monetary_values": [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
        }
        return entities