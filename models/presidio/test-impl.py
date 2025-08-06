# Libraries used:
# spacy
# Faker
from faker import Faker

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
        "PERSON": OperatorConfig("replace", {"new_value": fake.name}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": fake.phone_number}),
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
    }

    anonymized_entities = []

    for result in analyzer_results:
        if result.entity_type in operators:
            original_start = result.start
            original_end = result.end
            entity_type = result.entity_type
            entity_value = text[original_start: original_end]  # Access the recognized entity value

            if entity_type == "PERSON":
                operators[entity_type].params["new_value"] = presido_generate_n_save_mapping(entity_value, "PERSON")
            elif entity_type == "PHONE_NUMBER":
                operators[entity_type].params["new_value"] = presido_generate_n_save_mapping(entity_value, "PHONE_NUMBER")

            anonymized_value = anonymizer.anonymize(text=text, analyzer_results=[result], operators=operators).text
            anonymized_entities.append((original_start, original_end, entity_type))

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

    # Text to analyze
    analyzer_results = analyzer.analyze(text=text, language="en")

    result = presido_anonymize_with_indices(analyzer_results, text)

    return result


# result = replace_pii("My name is Fazil")
result = replace_pii("John Smith, from Acme Corporation, provided his US_DRIVER_LICENSE (DL1234567890), US_PASSPORT (P123456789), and US_BANK_ACCOUNT (9876543210) details for the transaction. His email address is john.smith@example.com, phone number +1 (555) 987-6543, and credit card number is 1234 5678 9101 1121 (Visa). The transaction occurred on January 1, 2023, from IP address 192.168.0.1 in New York City, NY.")
print(result)
