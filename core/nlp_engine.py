import spacy

class NLPEngine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def get_basic_entities(self, text):
        doc = self.nlp(text[:100000]) # Limit length for performance
        entities = {
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
            "monetary_values": [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
        }
        return entities