# Libraries used:
# spacy
# Faker
from faker import Faker
from service import insert_into_redaction_table, insert_into_entity_table

fake = Faker() 

def replace_with_entity(entity):
    entity_label = entity['entity_group']
    entity_word = entity['word']
    # Define replacements for each entity type
    replacements = {
        # "FIRSTNAME": "PERSON",
        # "LASTNAME": "PERSON",
        # "USERNAME": "PERSON",
        "PASSWORD": "PASSWORD",
        # "DATE": "DATE",
        "STREETADDRESS": "STREETADDRESS",
        "STATE": "STATE",
        "COMPANY_NAME": "COMPANY_NAME",
        "JOBTYPE": "JOBTYPE",
        "EMAIL": "EMAIL",
        "PHONE_NUMBER": "PHONE_NUMBER",
        "CITY": "CITY",
        "URL": "URL",
        "CURRENCYSYMBOL": "CURRENCYSYMBOL",
        "TIME": "TIME"
    }

    if entity_label in replacements:
        return "[" + replacements[entity_label] + "]"
    else:
        return entity_word

def redact_pii(text):

    replacement_list = []

    from transformers import pipeline
    pipe = pipeline("token-classification", model="ab-ai/pii_model")
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
        if (entity_word != " " + text[0: len(entity_word) - 1]) and (entity_word[0] == " "):
            front_space = True

        # check whether the word has back space and remove it
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
        redact_text = replace_with_entity(entity)
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

    return [new_text, replacement_list]

if __name__ == "__main__":
    print("PII Model")
