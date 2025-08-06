# Libraries used:
# spacy
# Faker
from faker import Faker
from service import insert_into_redaction_table, insert_into_entity_table
import random
from datetime import datetime

from transformers import pipeline

fake = Faker() 

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
    entity_label = entity['entity_group']
    entity_word = entity['word']

    # Define replacements for each entity type
    replacements = {
        "FULLNAME": lambda: str(fake.name()),
        "FIRSTNAME": lambda: str(fake.name()),
        "MIDDLENAME": lambda: str(fake.name()),
        "LASTNAME": lambda: str(fake.name()),
    }

    if(is_replaced):
        if entity_label in replacements:
            replacement_function = replacements[entity_label]
            # Replace the entity with fake data
            fake_value = replacement_function()
    else:
        fake_value = "XXXXX"

    list_of_documents = ''
    # Insert the replace details into the table
    entity_id = insert_into_redaction_table(str(entity_word), entity_label, fake_value, int(is_replaced), user_id)
    # Insert into entity table
    insert_into_entity_table(user_id, entity_id, list_of_documents)
    
    return fake_value

def replace_pii(detection_type, text, user_id):

    gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
    all_entities = gen(text, aggregation_strategy="first")

    # Initialize a list to hold the new text parts
    new_text_parts = []
    last_end = 0

    for entity in all_entities:
        # Append text from the end of the last entity to the start of this one
        new_text_parts.append(text[last_end:entity['start']])
        # Append a placeholder for the PII
        # new_text_parts.append(f"[{ent.label_}]")
        if (detection_type == "redact"):
            new_text_parts.append(f" [{replace_with_fake('redact', entity, user_id)}] ")
        if (detection_type == "replace"):
            new_text_parts.append(f" [{replace_with_fake('replace', entity, user_id)}] ")
        # Update the last_end to the end of this entity
        last_end = entity['end']

    # Append any remaining text after the last entity
    new_text_parts.append(text[last_end:])

    # Join all parts into the final text
    new_text = ''.join(new_text_parts)
    return new_text

def replace_with_entity(entity, model_to_use):
    entity_label = entity['entity_group']
    entity_word = entity['word']
    # Define replacements for each entity type

    replacements = dict()

    if (model_to_use == "deberta"):
        replacements = {
            # "USERNAME": "PERSON",
            # "FIRSTNAME": "PERSON",
            # "LASTNAME": "PERSON",
            # "MIDDLENAME": "PERSON",
            # "FULLNAME": "PERSON",
            "STREETADDRESS": "STREETADDRESS",
            "COMPANY_NAME": "COMPANY_NAME",
            "JOBTYPE": "JOBTYPE",
            "USERAGENT": "USERAGENT",
            "VEHICLEVIN": "VEHICLEVIN"
        }

    if (model_to_use == "pii"):
        replacements = {
            "ACCOUNTNAME": "ACCOUNTNAME",
            "CREDITCARDCVV": "CREDITCARDCVV",
            "CREDITCARDISSUER": "CREDITCARDISSUER",
            "IBAN": "IBAN",
        }

    if entity_label in replacements:
        return "[" + replacements[entity_label] + "]"
    else:
        return entity_word

# This is the actual function which is used.
def redact_pii(text, model_to_use, processor_type):

    replacement_list = []

    start_time = datetime.now()

    all_entities = []
    
    if (model_to_use == "deberta"):
        if (processor_type == "gpu"):
            print("ProcessorType: GPU")
            gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device_map = 'cuda')
        else:
            print("ProcessorType: CPU")
            gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device = -1)
        all_entities = gen(text, aggregation_strategy="first")
    if (model_to_use == "pii"):
        if (processor_type == "gpu"):
            pipe = pipeline("token-classification", model="ab-ai/pii_model", device_map = 'cuda')
        else:
            pipe = pipeline("token-classification", model="ab-ai/pii_model", device = -1)
        
        all_entities = pipe(text, aggregation_strategy="first")

    # Initialize a list to hold the new text parts
    new_text_parts = []
    last_end = 0

    for entity in all_entities:

        entity_word = entity['word']

        # Code to remove the front and back space in the entity
        front_space = back_space = False

        # the first sentence of the word has space in front, so we detect it and remove that space.
        if (entity_word == " " + text[0: len(entity_word) - 1]):
            entity_word = entity_word[1:]

        # check whether the word has front space and remove it
        if (len(entity_word) > 0):
            if (entity_word != " " + text[0: len(entity_word) - 1]) and (entity_word[0] == " "):
                front_space = True

        # check whether the word has back space and remove it
        if (len(entity_word) > 0):
            if entity_word[-1] == " ":
                back_space = True

        if (front_space):
            entity_word = entity_word[1:]
            entity['start'] = entity['start'] + 1

        if (back_space):
            entity_word = entity_word[:-1]
            entity['end'] = entity['end'] - 1

        entity["word"] = entity_word

        # Append text from the end of the last entity to the start of this one
        new_text_parts.append(text[last_end:entity['start']])

        # Append a placeholder for the PII
        redact_text = replace_with_entity(entity, model_to_use)
        new_text_parts.append(f"{redact_text}")

        # Add to the list
        if(entity_word != redact_text):
            replacement_list.append([entity['start'], entity['start'] + len(entity_word), text[entity['start']:entity['start'] + len(entity_word)], redact_text])

        # Update the last_end to the end of this entity
        last_end = entity['end']

    # Append any remaining text after the last entity
    new_text_parts.append(text[last_end:])

    # Join all parts into the final text
    new_text = ''.join(new_text_parts)

    # print("Replacement")
    # print(replacement_list)

    end_time = datetime.now()
    time_taken = ((end_time - start_time).total_seconds() * 1000)

    return [new_text, replacement_list, time_taken]

if __name__ == "__main__":
    print("DeBERTA")
