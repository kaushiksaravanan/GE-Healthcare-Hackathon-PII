# Libraries used:
# spacy
# Faker
# import spacy
from faker import Faker
from service import insert_into_redaction_table, insert_into_entity_table
import random

from spacy import load
nlp = load("en_core_web_sm")

from datetime import datetime

fake = Faker() 

# Load the spaCy model
# INSTALL: !python -m spacy download en_core_web_sm

def fake_ordinal_number(n):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return str(n) + suffix

def replace_with_fake(detection_type, entity, user_id):

    fake_value = ""

    is_replaced = True if (detection_type == "replace") else False
    
    # Replace only the name.
    entity_label = entity.label_

    # Define replacements for each entity type
    replacements = {
        "PERSON": lambda: str(fake.name()),
        "NORP": lambda: str(random.choice(["American", "Chinese", "French", "Indian"])),
        "FAC": lambda: str(random.choice(["Empire State Building", "Golden Gate Bridge", "Eiffel Tower"])),
        "ORG": lambda: str(fake.company()),
        "GPE": lambda: str(fake.city()),
        "LOC": lambda: str(random.choice(["Mount Everest", "Amazon River", "Sahara Desert"])),
        "PRODUCT": lambda: str(random.choice(["iPhone", "Tesla Model S", "Big Mac"])),
        "EVENT": lambda: str(random.choice(["Olympics", "World Cup", "Super Bowl"])),
        "WORK_OF_ART": lambda: str(random.choice(["Mona Lisa", "Beethoven's Fifth Symphony", "Hamlet"])),
        "LAW": lambda: str(random.choice(["Patriot Act", "Clean Air Act", "Affordable Care Act"])),
        "LANGUAGE": lambda: str(random.choice(["English", "Spanish", "Mandarin"])),
        "DATE": lambda: str(fake.date()),
        "TIME": lambda: str(fake.time()),
        "PERCENT": lambda: str(f"{random.randint(1, 100)}%"),
        "MONEY": lambda: str(f"${random.randint(1, 10000)}"),
        "QUANTITY": lambda: str(f"{random.randint(1, 100)} kg"),
        "ORDINAL": lambda:  str(fake_ordinal_number(random.randint(1, 100))),
        "CARDINAL": lambda: str(random.randint(1, 1000)),
    }

    if(is_replaced):
        replacement_function = replacements[entity_label]
        # Replace the entity with fake data
        fake_value = replacement_function()
    else:
        fake_value = "XXXXX"

    list_of_documents = ''
    # Insert the replace details into the table
    entity_id = insert_into_redaction_table(str(entity), entity_label, fake_value, int(is_replaced), user_id)
    # Insert into entity table
    insert_into_entity_table(user_id, entity_id, list_of_documents)
    
    return fake_value

def replace_pii(detection_type, text, user_id):
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
            if (detection_type == "redact"):
                new_text_parts.append(f"[{replace_with_fake('redact', ent, user_id)}]")
            if (detection_type == "replace"):
                new_text_parts.append(f"[{replace_with_fake('replace', ent, user_id)}]")
            # Update the last_end to the end of this entity
            last_end = ent.end_char

    # Append any remaining text after the last entity
    new_text_parts.append(text[last_end:])

    # Join all parts into the final text
    new_text = ''.join(new_text_parts)
    return new_text

def replace_with_entity(entity):
    
    entity_label = entity.label_

    # Define the PII labels we are interested in
    all_replacements = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

    # Define replacements for each entity type
    replacements = {
        "PERSON": "PERSON",
        "MONEY": "MONEY",
        "QUANTITY": "QUANTITY",
        "EVENT": "EVENT",
        "WORK_OF_ART": "WORK_OF_ART",
        "LAW": "LAW",
        "LANGUAGE": "LANGUAGE"
    }

    if entity_label in replacements:
        return "[" + replacements[entity_label] + "]"
    else:
        return str(entity)

def redact_pii(text, processor_type):

    replacement_list = []

    if(processor_type == "gpu"):
        nlp.prefer_gpu = True
        nlp.require_gpu = True
    else:
        nlp.prefer_gpu = False
        nlp.require_gpu = False

    start_time = datetime.now()
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Initialize a list to hold the new text parts
    new_text_parts = []
    last_end = 0

    # Iterate over the entities detected by spaCy
    for ent in doc.ents:
        # Append text from the end of the last entity to the start of this one
        new_text_parts.append(text[last_end:ent.start_char])
        entity_word = str(ent)
        # Append a placeholder for the PII
        redact_text = replace_with_entity(ent)
        new_text_parts.append(f"{redact_text}")

        # Add to the list
        if(entity_word != redact_text):
            replacement_list.append([ent.start_char, ent.start_char + len(entity_word), text[ent.start_char:ent.start_char + len(entity_word)], redact_text])

        # Update the last_end to the end of this entity
        last_end = ent.end_char

    # Append any remaining text after the last entity
    new_text_parts.append(text[last_end:])

    # Join all parts into the final text
    new_text = ''.join(new_text_parts)

    end_time = datetime.now()
    time_taken = ((end_time - start_time).total_seconds() * 1000)

    # print("Replacement")
    # print(replacement_list)

    return [new_text, replacement_list, time_taken]

if __name__ == "__main__":
    print("spacyNER")
