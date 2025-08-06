from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from faker import Faker

# Set seeds for random generators
Faker.seed(4321)

# Initialize engines
analyzer = AnalyzerEngine()
fake = Faker()

# Mapping to store original and fake data
mapping = {}
generated_fake = []

# Text to analyze
text = "His name is Mr. Jones and his phone number is 212-555-5555"
analyzer_results = analyzer.analyze(text=text, language="en")

# Functions

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
    }
    for result in analyzer_results:
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

# Run functions and print results
redacted_text = presido_redact(analyzer_results, text)
print("Redacted Text: ", redacted_text)

anonymized_text = presido_anonymize(analyzer_results, text)
print("Anonymized Text: ", anonymized_text)
