# Libraries used:
from faker import Faker
from service import insert_into_redaction_table, insert_into_entity_table
from datetime import datetime

import en_ner_bc5cdr_md
from spacy.matcher import Matcher
# Recognized Entities: DRUG_DOSE, DISEASE, CHEMICAL
nlp_bc = en_ner_bc5cdr_md.load()

fake = Faker() 

def redact_pii(text, processor_type):

    replacement_list = []

    if(processor_type == "gpu"):
        nlp_bc.prefer_gpu = True
        nlp_bc.require_gpu = True
    else:
        nlp_bc.prefer_gpu = False
        nlp_bc.require_gpu = False

    start_time = datetime.now()

    doc = nlp_bc(text)

    pattern = [{'ENT_TYPE':'CHEMICAL'}, {'LIKE_NUM': True}, {'IS_ASCII': True}]
    matcher = Matcher(nlp_bc.vocab)
    matcher.add("DRUG_DOSE", [pattern])
    
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp_bc.vocab.strings[match_id]  # get string representation
        span = doc[start:end]  # the matched span adding drugs doses
        print(span.text, start, end, string_id,)
        # DRUG_DOSE
        replacement_list.append([start, end, span.text, "[" +string_id + "]"])
        # Add disease and drugs
    for ent in doc.ents:
        # DISEASE, CHEMICAL
        replacement_list.append([ent.start_char, ent.end_char, ent.text, "[" + ent.label_ + "]"])

    end_time = datetime.now()
    time_taken = ((end_time - start_time).total_seconds() * 1000)

    return ["PHI model", replacement_list, time_taken]

if __name__ == "__main__":
    print("PHI Model")
