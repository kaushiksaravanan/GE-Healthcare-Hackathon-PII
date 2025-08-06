# Libraries used:
# spacy
# Faker
from faker import Faker
from service import insert_into_redaction_table, insert_into_entity_table

fake = Faker() 

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig

# Initialize engines
analyzer = AnalyzerEngine()
fake = Faker()

# Mapping to store original and fake data
mapping = {}
generated_fake = []


def presido_redact(analyzer_results, text):
    anonymizer = AnonymizerEngine()
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "CREDIT_CARD": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "DATE_TIME": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "IP_ADDRESS": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "ORGANIZATION": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "US_DRIVER_LICENSE": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "US_PASSPORT": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "US_BANK_ACCOUNT": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "IBAN_CODE": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
        "DEFAULT": OperatorConfig("replace", {"new_value": "XXXXXXX"}),
    }
    for result in analyzer_results:
        if result.entity_type in operators:
            operators[result.entity_type].params["new_value"] = "XXXXXXX"
    result = anonymizer.anonymize(text=text, analyzer_results=analyzer_results, operators=operators)
    return result.text

def presido_anonymize(analyzer_results, text):
    anonymizer = AnonymizerEngine()
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": fake.name}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": fake.phone_number}),
    }

    for result in analyzer_results:
        if result.entity_type == "PERSON":
            operators[result.entity_type].params["new_value"] = presido_generate_n_save_mapping(result.entity_type, "PERSON")
        elif result.entity_type == "PHONE_NUMBER":
            operators[result.entity_type].params["new_value"] = presido_generate_n_save_mapping(result.entity_type, "PHONE_NUMBER")

    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=analyzer_results, operators=operators)
    return anonymized_result.text

def presido_generate_n_save_mapping(original, data_type):
    if data_type == 'PERSON':
        fake_value = fake.name()
    elif data_type == 'PHONE_NUMBER':
        fake_value = fake.phone_number()
    
    if fake_value not in mapping.values():
        mapping[original] = fake_value
        generated_fake.append(fake_value)
    return mapping[original]

def replace_pii(detection_type, text, user_id):

    result = ""

    is_replaced = True if (detection_type == "replace") else False

    # Text to analyze
    analyzer_results = analyzer.analyze(text=text, language="en")

    if(is_replaced):
        result = presido_anonymize(analyzer_results, text)
    else:
        result = presido_redact(analyzer_results, text)

    return result

if __name__ == "__main__":
    print("Presidio")
