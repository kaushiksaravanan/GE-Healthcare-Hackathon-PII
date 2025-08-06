from faker import Faker
# import presido_anonymize
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer.predefined_recognizers import SpacyRecognizer

# Initialize faker and analyzer engine
fake = Faker()
analyzer = AnalyzerEngine()
spacy_recognizer = SpacyRecognizer()
analyzer.registry.add_recognizer(spacy_recognizer)

# Generate fake data
text = f"""
Name: {fake.name()}
Phone Number: {fake.phone_number()}
IP Address: {fake.ipv4()}
MAC Address: {fake.mac_address()}
Address: {fake.address()}
City: {fake.city()}
State: {fake.state()}
Country: {fake.country()}
Zip Code: {fake.zipcode()}
Email ID: {fake.email()}
Credit Card: {fake.credit_card_number()}
Aadhaar: {fake.ssn()}  # Using SSN as a placeholder for Aadhaar
PAN Card: {fake.bban()}  # Using BBAN as a placeholder for PAN Card
Driving License: {fake.license_plate()}  # Using license plate as a placeholder for DL
Health Insurance Card Number: {fake.ean13()}
SSN Number: {fake.ssn()}
Birth Date: {fake.date_of_birth()}
Tax Number: {fake.itin()}
Passport Number: {fake.swift8()}  # Using SWIFT as a placeholder for Passport
GPS Latitude/Longitude: {fake.latitude()}, {fake.longitude()}
Vehicle Address Number: {fake.license_plate()}
Date: {fake.date()}
Time: {fake.time()}
Patient Number: {fake.random_number(digits=10)}
Billing Number: {fake.random_number(digits=10)}
Religion: {fake.random_element(elements=('Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Atheism'))}
Gender: {fake.random_element(elements=('Male', 'Female', 'Other'))}
Weight: {fake.random_int(min=50, max=100)} kg
Height: {fake.random_int(min=150, max=200)} cm
BMI: {fake.random_int(min=18, max=30)}
Passcode: {fake.password()}
Age: {fake.random_int(min=18, max=80)}
"""
print(text)
# Analyze the text
print( analyzer.analyze(text=text, language="en"))

# Anonymize the text
# anonymized_text = presido_anonymize(analyzer_results, text)
# print(anonymized_text)
