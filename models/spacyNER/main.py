# Libraries used
# spacy
# Faker
import spacy
from faker import Faker

fake = Faker() 

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def replace_with_fake(entity_label):
    # Replace only the name.
    if (entity_label == "PERSON"):
        return fake.name()
    else:
        return entity_label

def replace_pii(text):
    # Process the text with spaCy
    doc = nlp(text)
    
    # Define the PII labels we are interested in
    pii_labels = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

    # Initialize a list to hold the new text parts
    new_text_parts = []
    last_end = 0

    # Iterate over the entities detected by spaCy
    for ent in doc.ents:
        if ent.label_ in pii_labels:
            # Append text from the end of the last entity to the start of this one
            new_text_parts.append(text[last_end:ent.start_char])
            # Append a placeholder for the PII
            # new_text_parts.append(f"[{ent.label_}]")
            new_text_parts.append(f"[{replace_with_fake(ent.label_)}]")
            # Update the last_end to the end of this entity
            last_end = ent.end_char

    # Append any remaining text after the last entity
    new_text_parts.append(text[last_end:])

    # Join all parts into the final text
    new_text = ''.join(new_text_parts)
    return new_text

# Test the function
sample_text = "John Doe's email is john.doe@example.com. He lives in New York and works at OpenAI. His phone number is 123-456-7890."
replaced_text = replace_pii(sample_text)
print(replaced_text)