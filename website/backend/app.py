import MySQLdb
from flask import Flask, jsonify, request 
from flask_cors import CORS, cross_origin
from datetime import datetime
from database import ACCESS_RIGHTS_TABLE, DATABASE, DOCUMENT_TABLE, ENTITY_TABLE, PASSWORD, REDACTION_TABLE, SERVER, USERNAME, USERS_TABLE, APPLICATION_STATISTICS_TABLE
from service import insert_into_document_table, update_entity_table

# To generate random data
import random

# to fake the redacted data
from faker import Faker
from faker_crypto import CryptoAddress

# used in replace_placeholders function
import re

# multiprocessing
import multiprocessing

# models
import rule_based_approach_impl
import presidio_model
import deberta_model
import spacyner_model
import phi_model_impl

# to avoid warnings
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
# Enable CORS to access the application from the frontend.
CORS(app, support_credentials=True)

fake = Faker()
fake.add_provider(CryptoAddress)

def generate_indian_passport_number():
    letter_part = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    number_part = ''.join(fake.random_choices(elements=('0123456789'), length=7))
    return f"{letter_part}{number_part}"

def generate_fake_port_number():
    return random.randint(1, 65535)

def generate_semantic_version():
    major = random.randint(0, 9)   # Random number between 0 and 9 for major version
    minor = random.randint(0, 9)   # Random number between 0 and 9 for minor version
    patch = random.randint(0, 99)  # Random number between 0 and 99 for patch version
    return f"{major}.{minor}.{patch}"

def generate_vehicle_number():
    char_part = fake.random_letter() + fake.random_letter()  # Generate two random letters
    num_part1 = fake.random_number(digits=2)  # Generate two random digits
    num_part2 = fake.random_number(digits=4)  # Generate four random digits
    return f"{char_part} {num_part1} {char_part}{num_part2}"

# Fake data generating functions
def generate_drug():
    prefixes = ["Acetyl", "Allo", "Amino", "Bromo", "Chloro", "Cyano", "Dextro", "Epi", "Fluoro", "Glyco"]
    suffixes = ["amine", "azole", "caine", "cid", "dine", "dronate", "fen", "mab", "ol", "sartan"]

    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)

    return prefix + suffix

def generate_disease():
    prefixes = ["Auto", "Hyper", "Hypo", "Multi", "Neuro", "Pan", "Poly", "Pre", "Sub", "Uni"]
    suffixes = ["emia", "itis", "oma", "osis", "pathy", "plasia", "rrhage", "rrhea", "stasis", "thrombosis"]

    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)

    return prefix + suffix

replacements_dict = {
    "PERSON": lambda: str(fake.name()),                                                                 # Personal - SpacyNER
    "PERCENT": lambda: str(f"{random.randint(1, 100)}%"),                                               # Other - Rule-based
    "MONEY": lambda: str(f"${random.randint(1, 10000)}"),                                               # Amount - SpacyNER
    "QUANTITY": lambda: str(f"{random.randint(1, 100)} kg"),                                            # Other - SpacyNER
    "EVENT": lambda: str(random.choice(["Olympics", "World Cup", "Super Bowl"])),                       # Other - SpacyNER
    "WORK_OF_ART": lambda: str(random.choice(["Mona Lisa", "Beethoven's Fifth Symphony", "Hamlet"])),   # Other - SpacyNER
    "LAW": lambda: str(random.choice(["Patriot Act", "Clean Air Act", "Affordable Care Act"])),         # Other - SpacyNER
    "LANGUAGE": lambda: str(random.choice(["English", "Spanish", "Mandarin"])),                         # Other - SpacyNER
    "DATE": lambda: str(fake.date()),                                                                   # Other - Rule-based
    "STREETADDRESS": lambda: str(fake.street_address()),                                                # Location - DeBERTA
    "COMPANY_NAME": lambda: str(fake.company()),                                                        # Personal - DeBERTA
    "JOBTYPE": lambda: str(fake.job()),                                                                 # Personal - DeBERTA
    "EMAIL": lambda: str(fake.email()),                                                                 # Personal - Rule-based
    "PHONE_NUMBER": lambda: str(fake.phone_number()),                                                   # Personal - Rule-based
    "URL": lambda: str(fake.url()),                                                                     # Network - Rule-based
    "PATH": lambda: str(fake.file_path(depth=random.randint(1, 5), category=None, extension=None)),     # Network - Rule-based
    "TIME": lambda: str(fake.time()),                                                                   # Other - Rule-based
    "BITCOINADDRESS": lambda: str(fake.bitcoin_address()),                                              # Account - Rule-based
    "ETHEREUMADDRESS": lambda: str(fake.ethereum_address()),                                            # Account - Rule-based
    "IP": lambda: str(fake.ipv6()),                                                                     # Network - Rule-based
    "IPV4": lambda: str(fake.ipv4()),                                                                   # Network - Rule-based
    "MAC": lambda: str(fake.mac_address()),                                                             # Network - Rule-based
    "PORT": lambda: str(generate_fake_port_number()),                                                   # Network - Rule-based
    "USERAGENT": lambda: str(fake.user_agent()),                                                        # Network - DeBERTA
    "VEHICLEVIN": lambda: str(fake.hexify(text='*****************', upper=False)),                      # Personal - DeBERTA
    "VEHICLENUMBER": lambda: str(generate_vehicle_number()),                                            # Personal - Rule-based
    "AMOUNT": lambda: str(round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)),        # Account - PII
    "CREDITCARDISSUER": lambda: str(fake.credit_card_provider()),                                       # Account - PII
    "CREDITCARDCVV": lambda: str(fake.credit_card_security_code()),                                     # Account - PII
    "SSN": lambda: str(fake.ssn()),                                                                     # Personal - Rule-based
    "ZIPCODE": lambda: str(fake.zipcode()),                                                             # Location - Rule-based
    "CREDITCARDNUMBER": lambda: str(fake.credit_card_number()),                                         # Account - Rule-based
    "ACCOUNTNUMBER": lambda: str(fake.bban()),                                                          # Account - Rule-based
    "ACCOUNTNAME": lambda: str(fake.name()),                                                            # Account - PII
    "GENDER": lambda: str(fake.random_element(elements=("Male", "Female", "Non-binary", "Other"))),     # Personal - Rule-based
    "IBAN": lambda: str(fake.iban()),                                                                   # Account - PII
    "SEX": lambda: str(fake.random_element(elements=("M", "F", "X"))),                                  # Personal - PII
    "AADHAAR": lambda: str(fake.bothify(text='####-####-####', letters='0123456789')),                  # Account - Rule-based
    "PAN": lambda: str(fake.bothify(text='?????####?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')),# Account - Rule-based
    "IFSC": lambda: str(fake.bothify(text='????0######', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')),# Account - Rule-based
    "HEIGHT": lambda: str(round(random.uniform(140, 200), 2)),                                          # Health - Rule-based
    "WEIGHT": lambda: str(round(random.uniform(40, 150), 2)),                                           # Health - Rule-based
    "BMI": lambda: str(round(random.uniform(15.0, 40.0), 2)),                                           # Health - Rule-based
    "CHEMICAL": lambda: str(generate_drug()),                                                           # Health - PHI
    "DISEASE": lambda: str(generate_disease()),                                                         # Health - PHI
    "DRUG_DOSE": lambda: str(generate_drug()),                                                          # Health - PHI
    "US_DRIVER_LICENSE": lambda: str(fake.license_plate()),                                             # Personal - Presidio
    "US_PASSPORT": lambda: str(fake.name()),                                                            # Personal - Presidio
    "US_BANK_ACCOUNT": lambda: str(fake.name()),                                                        # Account - Presidio
    "PASSWORD": lambda: "*****",                                                                         # Account - PII
    "VERSION": lambda: str(generate_semantic_version),                                                   # Other - Rule-based
    "LATLNG": lambda: str(fake.latitude()) + ", " + str(fake.longitude()),                               # Location: Rule-based
    "PASSPORT": lambda: str(generate_indian_passport_number()),                                         # Personal - Rule-based
    "CITY": lambda: str(fake.city()),                                                                   # Location - Rule-based
    "CONTINENT": lambda: str(fake.random_element(elements=["Africa", "Antarctica", "Asia", "Europe", "North America", "Australia/Oceania", "South America"])),# Location - Rule-based
    "COUNTRY": lambda: str(fake.country()),                                                                  # Location - Rule-based
    "STATES": lambda: str(fake.state()),                                                                # Location - Rule-based
    "CURRENCY": lambda: str(fake.currency_name()),                                                        # Account - Rule-based
    "CURRENCY_SYMBOL": lambda: str(fake.currency_symbol()),                                              # Account - Rule-based
}

# Types:
# Personal
# Amount
# Location
# Network
# Health
# Other
type_of_pii_data = {
    "PERSON": "PERSONAL",
    "PERCENT": "OTHER",
    "MONEY": "ACCOUNT",
    "QUANTITY": "OTHER",
    "EVENT": "OTHER",
    "WORK_OF_ART": "OTHER",
    "LAW": "OTHER",
    "LANGUAGE": "OTHER",
    "DATE": "OTHER",
    "STREETADDRESS": "LOCATION",
    "COMPANY_NAME": "PERSONAL",
    "JOBTYPE": "PERSONAL",
    "EMAIL": "PERSONAL",
    "PHONE_NUMBER": "PERSONAL",
    "URL": "NETWORK",
    "PATH": "NETWORK",
    "TIME": "OTHER",
    "BITCOINADDRESS": "ACCOUNT",
    "ETHEREUMADDRESS": "ACCOUNT",
    "IP": "NETWORK",
    "IPV4": "NETWORK",
    "MAC": "NETWORK",
    "PORT": "NETWORK",
    "USERAGENT": "NETWORK",
    "VEHICLEVIN": "PERSONAL",
    "VEHICLENUMBER": "PERSONAL",
    "AMOUNT": "ACCOUNT",
    "CREDITCARDISSUER": "ACCOUNT",
    "CREDITCARDCVV": "ACCOUNT",
    "SSN": "PERSONAL",
    "ZIPCODE": "LOCATION",
    "CREDITCARDNUMBER": "ACCOUNT",
    "ACCOUNTNUMBER": "ACCOUNT",
    "ACCOUNTNAME": "ACCOUNT",
    "GENDER": "PERSONAL",
    "IBAN": "ACCOUNT",
    "SEX": "PERSONAL",
    "AADHAAR": "ACCOUNT",
    "PAN": "ACCOUNT",
    "IFSC": "ACCOUNT",
    "HEIGHT": "HEALTH",
    "WEIGHT": "HEALTH",
    "BMI": "HEALTH",
    "CHEMICAL": "HEALTH",
    "DISEASE": "HEALTH",
    "DRUG_DOSE": "HEALTH",
    "US_DRIVER_LICENSE": "PERSONAL",
    "US_PASSPORT": "PERSONAL",
    "US_BANK_ACCOUNT": "ACCOUNT",
    "PASSWORD": "ACCOUNT",
    "VERSION": "OTHER",
    "LATLNG": "LOCATION",
    "PASSPORT": "PERSONAL",
    "CITY":"LOCATION",
    "CONTINENT":"LOCATION",
    "COUNTRY": "LOCATION",
    "STATES":"LOCATION",
    "CURRENCY": "ACCOUNT",
    "CURRENCY_SYMBOL": "ACCOUNT"
}

# To remove the overlapping intervals returned by different models.
# def find_non_overlapping_intervals(intervals):
#     intervals.sort(key=lambda x: x[0])  # Sort intervals by start time
#     non_overlapping = []
#     for interval in intervals:
#         if not non_overlapping or non_overlapping[-1][1] < interval[0]:
#             non_overlapping.append(interval)
#     return non_overlapping

def find_non_overlapping_intervals(intervals, special_interval):
    # Add the special interval to the list of intervals
    intervals.extend(special_interval)
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    non_overlapping = []
    for interval in intervals:
        # If the special interval is in the list, it takes precedence over overlapping intervals
        if interval == special_interval:
            non_overlapping = [special_interval]
        else:
            if not non_overlapping or non_overlapping[-1][1] < interval[0]:
                non_overlapping.append(interval)
    
    print(non_overlapping)
    return non_overlapping

# This function will replace the entities with redact or replace value.
def replace_placeholders(text, replacements, detection_type):
    # To get total number of words that is replaced.
    replaced_count = 0
    def replace_match(match):
        key = match.group(1)
        if key in replacements:
            # return replacements[key]()
            nonlocal replaced_count
            replaced_count += 1
            # Replace
            if detection_type == "replace":
                return f"[[{replacements[key]()}]]"
            # Redact
            if detection_type == "redact":
                return f"[[XXXXX]]"
            # Entity
            if detection_type == "entity":
                return f"[[{key}]]"
        return match.group(0)  # If the key is not found, return the original match
    
    pattern = r'\[\[([A-Z_]+)\]\]'
    return [re.sub(pattern, replace_match, text), replaced_count]

# this will append the entity values into the text.
def replace_text_fn(text, replace_dicts, replacements, detection_type):

    replaced_count = 0

    # store all the replaced values.
    replaced_value_dict = dict()

    parent_pii_data_percentage_dict = {
        "PERSONAL" : 0,
        "ACCOUNT": 0,
        "LOCATION": 0,
        "NETWORK": 0,
        "HEALTH": 0,
        "OTHER": 0
    }

    # Sort the replacement dictionaries based on start index
    replace_dicts.sort(key=lambda x: x[0])

    # Replace values in the text with their corresponding placeholders
    result = ""
    highlighted_text = ""
    entity_text = ""
    redact_text = ""
    replace_text = ""

    current_index = 0
    for start, end, value, placeholder in replace_dicts:
        # Append the text from the last replacement to the current start index
        result += text[current_index:start]
        highlighted_text += text[current_index:start]
        entity_text += text[current_index:start]
        redact_text += text[current_index:start]
        replace_text += text[current_index:start]

        key = placeholder[1:len(placeholder)-1]

        # Replace the value if it is already present.
        if value in replaced_value_dict:
            result += f"[[{replaced_value_dict[value]}]]"
            highlighted_text += f"[[{text[start:end]}]]"
            entity_text += f"[[{key}]]"
            redact_text += f"[[XXXXX]]"
            replace_text += f"[[{replaced_value_dict[value]}]]"
        else:
            # Append the placeholder instead of the value
            value_to_be_replaced = ""
            # Remove the front and back brackets
            
            value_to_be_replaced = replacements[key]()

            highlighted_text += f"[[{text[start:end]}]]"
            entity_text += f"[[{key}]]"
            redact_text += f"[[XXXXX]]"
            replace_text += f"[[{value_to_be_replaced}]]"

            replaced_value_dict[value] = value_to_be_replaced

        replaced_count += 1

        # Update the current index to the end of the replacement
        current_index = end

        # Get the parent type of PII data
        # remove the [] from the staring
        pii_type_parent = type_of_pii_data[placeholder[1:len(placeholder)-1]]
        # Increment the value.
        parent_pii_data_percentage_dict[pii_type_parent] += 1
        
    # Append the remaining text after the last replacement
    result += text[current_index:]
    highlighted_text += text[current_index:]
    entity_text += text[current_index:]
    redact_text += text[current_index:]
    replace_text += text[current_index:]

    return [result, highlighted_text, entity_text, redact_text, replace_text, parent_pii_data_percentage_dict, replaced_count, replaced_value_dict]

# Rule based approach
def pii_detection_using_rulebased(detection_type, text, user_id, processor_type):
    replaced_text, replaced_list, time_taken = rule_based_approach_impl.redact_pii(text)
    return [replaced_text, replaced_list, time_taken]

# Presidio Model.
def pii_detection_using_presidio(detection_type, text, user_id, processor_type):
    replaced_list, time_taken = presidio_model.replace_pii(text)
    return ["presidio", replaced_list, time_taken]

# PII Model.
def pii_detection_using_pii(detection_type, text, user_id, processor_type):
    # replaced_text = deberta_model.replace_pii(detection_type, text, user_id)
    replaced_text, replaced_list, time_taken = deberta_model.redact_pii(text, "pii", processor_type)
    return [replaced_text, replaced_list, time_taken]

# DeBERTA Model.
def pii_detection_using_deBERTA(detection_type, text, user_id, processor_type):
    # replaced_text = deberta_model.replace_pii(detection_type, text, user_id)
    replaced_text, replaced_list, time_taken = deberta_model.redact_pii(text, "deberta", processor_type)
    return [replaced_text, replaced_list, time_taken]

# SpacyNER Model.
def pii_detection_using_spacyNER(detection_type, text, user_id, processor_type):
    # replaced_text = spacyner_model.replace_pii(detection_type, text, user_id)
    replaced_text, replaced_list, time_taken = spacyner_model.redact_pii(text, processor_type)
    return [replaced_text, replaced_list, time_taken]

# PHI Model.
def pii_detection_using_phi(detection_type, text, user_id, processor_type):
    # replaced_text = deberta_model.replace_pii(detection_type, text, user_id)
    replaced_text, replaced_list, time_taken = phi_model_impl.redact_pii(text, processor_type)
    return [replaced_text, replaced_list, time_taken]

# MULTIPROCESSING
# Rule based approach
def pii_detection_using_rulebased_multiprocessing(detection_type, text, user_id, result, index):
    result_text, result_list = pii_detection_using_rulebased(detection_type, text, user_id)
    result[index] = result_list

# PII Model.
def pii_detection_using_pii_multiprocessing(detection_type, text, user_id, result, index):
    result_text, result_list = pii_detection_using_pii(detection_type, text, user_id)
    result[index] = result_list

# DeBERTA Model.
def pii_detection_using_deBERTA_multiprocessing(detection_type, text, user_id, result, index):
    result_text, result_list = pii_detection_using_deBERTA(detection_type, text, user_id)
    result[index] = result_list

# SpacyNER Model.
def pii_detection_using_spacyNER_multiprocessing(detection_type, text, user_id, result, index):
    result_text, result_list = pii_detection_using_spacyNER(detection_type, text, user_id)
    result[index] = result_list

# PHI Model.
def pii_detection_using_phi_multiprocessing(detection_type, text, user_id, result, index):
    result_text, result_list = pii_detection_using_phi(detection_type, text, user_id)
    result[index] = result_list

# PII Detection Models.
# This function will contain all the models.
def pii_detection(detection_type, text, user_id, multithreading, processor_type):

    # Find the total word count.
    words = text.split()
    total_word_count = len(words)

    total_time_taken = 0
    time_taken_presidio_model = 0
    time_taken_deberta_model = 0
    time_taken_spacyner_model = 0

    replaced_count = 0
    replaced_value_dict = dict()

    # Start timing
    start_time_overall = datetime.now()

    if (multithreading == "yes"):

        print("Multiprocessing")

        # Create an array to store results
        manager = multiprocessing.Manager()
        multiprocessing_result = manager.list([[], [], [], [], []])

        # Create processes
        process_rulebased = multiprocessing.Process(target=pii_detection_using_rulebased_multiprocessing, args=(detection_type, text, user_id, multiprocessing_result, 0))
        process_pii = multiprocessing.Process(target=pii_detection_using_pii_multiprocessing, args=(detection_type, text, user_id, multiprocessing_result, 1))
        process_deberta = multiprocessing.Process(target=pii_detection_using_deBERTA_multiprocessing, args=(detection_type, text, user_id, multiprocessing_result, 2))
        process_spacyner = multiprocessing.Process(target=pii_detection_using_spacyNER_multiprocessing, args=(detection_type, text, user_id, multiprocessing_result, 3))
        process_phi = multiprocessing.Process(target=pii_detection_using_phi_multiprocessing, args=(detection_type, text, user_id, multiprocessing_result, 4))

        # Start processes
        process_rulebased.start()
        process_pii.start()
        process_deberta.start()
        process_spacyner.start()
        process_phi.start()

        # Wait for processes to complete
        process_rulebased.join()
        process_pii.join()
        process_deberta.join()
        process_spacyner.join()
        process_phi.join()

        result_rulebased = multiprocessing_result[0]
        result_pii = multiprocessing_result[1]
        result_deberta = multiprocessing_result[2]
        result_spacyner = multiprocessing_result[3]
        result_phi = multiprocessing_result[4]

        # TODO: Replace this
        result = replace_text(text, result_rulebased + result_pii + result_deberta + result_spacyner + result_phi)

        text = result

    else:

        print("No Multithreading")

        # Rule based approach.
        text_rulebased, list_rulebased, time_taken_rulebased = pii_detection_using_rulebased(detection_type, text, user_id, processor_type)

        # Presidio Model.
        text_presidio, list_presidio, time_taken_presidio = pii_detection_using_presidio(detection_type, text, user_id, processor_type)

        # PII Model.
        text_pii, list_pii, time_taken_pii = pii_detection_using_pii(detection_type, text, user_id, processor_type)

        # DeBERTA Model.
        text_deBERTA, list_deBERTA, time_taken_deberta = pii_detection_using_deBERTA(detection_type, text, user_id, processor_type)

        # SpacyNER Model.
        text_spacyNER, list_spacyNER, time_taken_spacyner = pii_detection_using_spacyNER(detection_type, text, user_id, processor_type)

        # PII Model.
        text_pii, list_phi, time_taken_phi = pii_detection_using_phi(detection_type, text, user_id, processor_type)

        total_time_taken = time_taken_rulebased + time_taken_presidio + time_taken_pii + time_taken_deberta + time_taken_spacyner + time_taken_phi

        # Combine all the data
        combined_replacement_list = list_rulebased + list_pii + list_presidio + list_deBERTA + list_spacyNER + list_phi

        print("Combined list")
        print(combined_replacement_list)

        # Remove overlapping
        final_replacement_list = find_non_overlapping_intervals(combined_replacement_list, list_rulebased)

        print("Final list")
        print(final_replacement_list)

        result, highlighted_text, entity_text, redact_text, replace_text, parent_pii_info, replaced_count, replaced_value_dict = replace_text_fn(text, final_replacement_list, replacements_dict, detection_type)
        # Testing purpose
        # result = replace_text(text, list_rulebased)

        text = result

    # End Timing
    end_time_overall = datetime.now()
    print("start time: ", start_time_overall)
    print("end time: ", end_time_overall)
    total_time_taken = (end_time_overall - start_time_overall)
    total_time_taken = (total_time_taken.total_seconds() * 1000) 

    # added all the things in the replace_text() itself
    # text, replaced_count = replace_placeholders(text, replacements_dict, detection_type)

    percentage_of_pii = (replaced_count / total_word_count) * 100

    # Process the parent_pii_info
    # Sort reverse
    parent_pii_info = dict(sorted(parent_pii_info.items(), key=lambda item: item[1], reverse=True))
    labels_for_chart = []
    data_for_chart = []
    for item in parent_pii_info.items():
        labels_for_chart.append(item[0]), data_for_chart.append(item[1])
    
    parent_pii_info_list = [labels_for_chart, data_for_chart]

    return [text, highlighted_text, entity_text, redact_text, replace_text, percentage_of_pii, parent_pii_info_list, replaced_value_dict, total_time_taken, time_taken_rulebased, time_taken_presidio, time_taken_pii, time_taken_deberta, time_taken_spacyner, time_taken_phi]

@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return "Hello, World!"

@app.route("/application/statistics")
@cross_origin(supports_credentials=True)
def application_statistics():
    noOfFiles = 0
    noOfWords = 0
    noOfPII = 0
    noOfTime = 0
    db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM " + APPLICATION_STATISTICS_TABLE + " ORDER BY id LIMIT 1"
    cursor.execute(sql)
    data_result = cursor.fetchall()
    cursor.close()
    db.close()
    personID = 0
    for data in data_result:
        noOfFiles = data[1]
        noOfWords = data[2]
        noOfPII = data[3]
        noOfTime = data[4]
    if(len(data_result) > 0):
        data = { 
            "auth" : "success", 
            "no_of_files": noOfFiles,
            "no_of_words": noOfWords,
            "no_of_pii": noOfPII,
            "no_of_time": noOfTime
        } 
    else:
        data = { 
            "auth" : "fail", 
            "no_of_files": 0,
            "no_of_words": 0,
            "no_of_pii": 0,
            "no_of_time": 0
        } 

    return jsonify(data)

# Get the contents from different sources
@app.route("/logs/getcontents", methods = ['POST'])
@cross_origin(supports_credentials=True)
def get_contents():
    request_data = request.get_json()
    data_get_type = request_data["data_get_type"]
    data_get_url = request_data["data_get_url"]

    database_host = request_data["database_host"]
    database_name = request_data["database_name"]
    database_user = request_data["database_user"]
    database_password = request_data["database_password"]

    response = ""
    if (data_get_type == "url-html"):
        import get_type_url_html
        response = get_type_url_html.fun(data_get_url)
    if (data_get_type == "url-contents"):
        import get_type_url_contents
        response = get_type_url_contents.fun(data_get_url)
    if (data_get_type == "ftp"):
        import get_type_ftp
        response = get_type_ftp.fun(database_host, database_user, database_password, database_name)
    if (data_get_type == "file-location"):
        import get_type_file
        response = get_type_file.fun(data_get_url)
    if ((data_get_type == "database-mysql") or (data_get_type == "database-postgres") or (data_get_type == "database-sqlite")):
        import get_type_database
        database_type = data_get_type.split("-")[1]
        response = get_type_database.fun(database_type, database_host, database_name, database_user, database_password)
    
    if (response != ""):
        result = {
                    'status': 'success',
                    'response': response,
                }
    else:
        result = {
                    'status': 'fail',
                    'response': response,
                }

    return result

# Add the logs
@app.route("/logs/add", methods = ['POST'])
@cross_origin(supports_credentials=True)
def add_logs():
    user_id = 1
    request_data = request.get_json()
    detection_type = request_data['detection_type']
    logs_content = request_data['logs_content']
    document_name = request_data['document_name']
    document_size = request_data['document_size']
    document_timestamp = request_data['document_timestamp']
    multithreading = request_data['multithreading']
    processor_type = request_data['processor_type']

    # sample_text = "John Doe's email is john.doe@example.com. He lives in New York and works at OpenAI. His phone number is 123-456-7890."
    [processed_text, highlighted_text, entity_text, redact_text, replace_text, percentage_of_pii, parent_pii_info_list, replaced_value_dict, total_time_taken, time_taken_rulebased, time_taken_presidio, time_taken_pii, time_taken_deberta, time_taken_spacyner, time_taken_phi] = pii_detection(detection_type, logs_content, user_id, multithreading, processor_type)

    # document_id = insert_into_document_table(document_name, document_size, document_timestamp, total_time_taken, user_id)

    # TODO: Check all the elements in the entity_table with is_updated=0 and append the latest document_id to the list_of_documents if it is not present.
    # update_entity_table(user_id, document_id)

    # Round to 2 decimals and convert it to string.
    percentage_of_pii = round(percentage_of_pii, 2)
    percentage_of_pii = str(percentage_of_pii)

    result = {
                'status': 'success',
                'text': processed_text,
                'highlighted_text': highlighted_text,
                'entity_text': entity_text,
                'redact_text': redact_text,
                'replace_text': replace_text,
                'parent_pii_info_list': parent_pii_info_list,
                'percentage_of_pii': percentage_of_pii,
                'replaced_value_dict': replaced_value_dict,
                'total_time_taken': round(total_time_taken / 1000, 2),
                'time_taken_rulebased_model': round(time_taken_rulebased, 2),
                'time_taken_presidio_model': round(time_taken_presidio, 2),
                'time_taken_pii_model': round(time_taken_pii, 2),
                'time_taken_deberta_model': round(time_taken_deberta, 2),
                'time_taken_spacyner_model': round(time_taken_spacyner, 2),
                'time_taken_phi_model': round(time_taken_phi, 2),
            }
    
    return result

# Save the logs
@app.route("/logs/save", methods = ['POST'])
@cross_origin(supports_credentials=True)
def save_logs():
    user_id = 1
    request_data = request.get_json()
    detection_type = request_data['detection_type']
    data_input = request_data['input']
    document_name = request_data['document_name']
    document_size = request_data['document_size']
    document_timestamp = request_data['document_timestamp']
    total_time_taken = request_data['total_time_taken']
    data_output = request_data['output']
    highlight_text = request_data['highlight_text']
    replaced_value_dict = request_data['replaced_value_dict']

    document_id = insert_into_document_table(document_name, document_size, document_timestamp, total_time_taken, data_input, data_output, highlight_text, replaced_value_dict, detection_type, user_id)

    result = {
                'status': 'success',
                'document_id': str(document_id)
            }
    
    return result


@app.route('/logs/get', methods = ['GET']) 
@cross_origin(supports_credentials=True)
def get_logs(): 
    db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM " + DOCUMENT_TABLE + " WHERE owner_id = 1"
    cursor.execute(sql)
    data_result = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for data in data_result:
        document_id = data[0]
        document_name = data[1]
        document_size = data[2]
        timestamp = data[3]
        processed_time = data[4]
        data_input = data[5]
        data_output = data[6]
        highlight_text = data[7]
        replaced_value_dict = data[8]
        detection_type = data[9]
        owner_id = data[10]

        obj = {
            'documentId': document_id,
            'documentName': document_name,
            'documentSize': document_size,
            'timestamp': timestamp,
            'processedTime': processed_time,
            'dataInput': data_input,
            'dataOutput': data_output,
            'highlightText': highlight_text,
            'replacedValueDict': replaced_value_dict,
            'detectionType': detection_type,
            'ownerId': owner_id,            
        }

        result.append(obj)

    return jsonify(result)

@app.route('/logs/view/get', methods = ['GET'])
@cross_origin(supports_credentials= True)
def get_individual_log():
    document_id = request.args['id']
    db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()
    sql = "SELECT * FROM " + DOCUMENT_TABLE + " WHERE document_id = " + str(document_id) + " AND owner_id = 1"
    print(sql)
    cursor.execute(sql)
    data_result = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for data in data_result:
        document_id = data[0]
        document_name = data[1]
        document_size = data[2]
        timestamp = data[3]
        processed_time = data[4]
        data_input = data[5]
        data_output = data[6]
        highlight_text = data[7]
        replaced_value_dict = data[8]
        detection_type = data[9]
        owner_id = data[10]

        obj = {
            'documentId': document_id,
            'documentName': document_name,
            'documentSize': document_size,
            'timestamp': timestamp,
            'processedTime': processed_time,
            'dataInput': data_input,
            'dataOutput': data_output,
            'highlightText': highlight_text,
            'replacedValueDict': replaced_value_dict,
            'detectionType': detection_type,
            'ownerId': owner_id,            
        }

        result.append(obj)

    return jsonify(result)


# Login
@app.route('/login', methods = ['POST']) 
@cross_origin(supports_credentials=True)
def login(): 
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    role = request_data['role']

    if (role == 'admin'):
        sql = "SELECT * FROM " + USERS_TABLE + " WHERE user_email = '" + username + "' AND user_password = '" + password + "'"
    else:
        sql = "SELECT * FROM " + USERS_TABLE + " WHERE user_email = '" + username + "' AND user_password = '" + password + "'"
    db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()
    cursor.execute(sql)
    myresult = cursor.fetchall()
    cursor.close()
    db.close()
    personID = 0
    for x in myresult:
        personID = x[0]
    if(len(myresult) > 0):
        data = { 
            "auth" : "success", 
            "userid": personID
        } 
    else:
        data = { 
            "auth" : "fail", 
            "userid": "0"
        } 

    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0')