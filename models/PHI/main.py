# NER specific models
# INSTALL: !pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
import en_ner_bc5cdr_md
from spacy.matcher import Matcher

nlp_bc = en_ner_bc5cdr_md.load()

sample_text ="""
John Doe, a 47-year-old man with a history of hypertension, presented with a week-long struggle of throbbing headaches on the right side of his head, worsening with activity, and accompanied by dizziness upon standing. His blood pressure reading of 140/90 mmHg raised concerns, even though he takes Lisinopril daily for control. To determine the cause of his headaches, further evaluation with brain imaging and continued blood pressure management are recommended, along with over-the-counter pain relief for symptom control. A follow-up appointment is scheduled to discuss test results and potentially adjust the treatment plan.
"""

pattern = [{'ENT_TYPE':'CHEMICAL'}, {'LIKE_NUM': True}, {'IS_ASCII': True}]
matcher = Matcher(nlp_bc.vocab)
matcher.add("DRUG_DOSE", [pattern])
doc = nlp_bc(sample_text)
matches = matcher(doc)
print("Matches:")
for match_id, start, end in matches:
    string_id = nlp_bc.vocab.strings[match_id]  # get string representation
    span = doc[start:end]  # the matched span adding drugs doses
    print(span.text, start, end, string_id,)
    # Add disease and drugs
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)