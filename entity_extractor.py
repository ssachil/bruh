import spacy
from typing import List, Dict
import json

class EntityExtractor:
    def __init__(self):
        # Load the English language model
        self.nlp = spacy.load("en_core_web_lg")
        
        # Define entity types we're interested in
        self.entity_types = {
            'PERSON': 'Person',
            'ORG': 'Organization',
            'GPE': 'Location',
            'DATE': 'Date',
            'EVENT': 'Event',
            'PRODUCT': 'Product',
            'LAW': 'Law',
            'WORK_OF_ART': 'Work of Art',
        }
    
    def extract_entities(self, text: str, source_file: str) -> List[Dict]:
        """
        Extract entities from text using spaCy.
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                # Get the context (surrounding text)
                start = max(0, ent.start_char - 50)
                end = min(len(text), ent.end_char + 50)
                context = text[start:end].strip()
                
                entity = {
                    "name": ent.text,
                    "type": self.entity_types[ent.label_],
                    "source_file": source_file,
                    "confidence": ent._.confidence if hasattr(ent._, 'confidence') else 1.0,
                    "context": context
                }
                entities.append(entity)
        
        return entities
    
    def get_entity_statistics(self, text: str) -> Dict:
        """
        Get statistics about entities found in the text.
        """
        doc = self.nlp(text)
        stats = {}
        
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                entity_type = self.entity_types[ent.label_]
                if entity_type not in stats:
                    stats[entity_type] = 0
                stats[entity_type] += 1
        
        return stats 