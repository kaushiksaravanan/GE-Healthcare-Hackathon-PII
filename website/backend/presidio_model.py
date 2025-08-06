# Libraries used:
# spacy
# Faker
from faker import Faker

from datetime import datetime

fake = Faker() 

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig

# Initialize engines
analyzer = AnalyzerEngine()
fake = Faker()

# Mapping to store original and fake data
mapping = {}
generated_fake = []

def presido_anonymize_with_indices(analyzer_results, text):
    anonymizer = AnonymizerEngine()
    operators = {
        "CREDIT_CARD": "CREDITCARDNUMBER",
        # "LOCATION": "CITY",
        "ORGANIZATION": "COMPANY_NAME",
        # "US_DRIVER_LICENSE": "US_DRIVER_LICENSE",
        # "US_PASSPORT": "US_PASSPORT",
        # "US_BANK_ACCOUNT": "US_BANK_ACCOUNT",
        "IBAN_CODE": "IBAN",
    }

    anonymized_entities = []

    for result in analyzer_results:
        if result.entity_type in operators:
            original_start = result.start
            original_end = result.end
            entity_type = result.entity_type
            entity_value = text[original_start: original_end]  # Access the recognized entity value

            # anonymized_value = anonymizer.anonymize(text=text, analyzer_results=[result], operators=operators).text
            anonymized_entities.append((original_start, original_end, entity_value, "[" + operators[entity_type] + "]"))

    return anonymized_entities

def presido_generate_n_save_mapping(original, data_type):
    if data_type == 'PERSON':
        fake_value = fake.name()
    elif data_type == 'PHONE_NUMBER':
        fake_value = fake.phone_number()
    
    if fake_value not in mapping.values():
        mapping[original] = fake_value
        generated_fake.append(fake_value)
    return mapping[original]

def replace_pii(text):

    result = ""

    start_time = datetime.now()

    # Text to analyze
    analyzer_results = analyzer.analyze(text=text, language="en")

    result = presido_anonymize_with_indices(analyzer_results, text)

    end_time = datetime.now()
    time_taken = ((end_time - start_time).total_seconds() * 1000)

    return [result, time_taken]
