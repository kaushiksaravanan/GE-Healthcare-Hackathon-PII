import re
from datetime import datetime

import klepto

file_path = './assets/location'
archive = klepto.archives.file_archive(file_path, cached=False, serialized=True)
archive.load()
location_dict = archive['data']

def find_matches_cache(text, dict_val, matches):
    text_lower = text.lower()  # Convert text to lowercase for case insensitive matching
    def find_all(text, phrase):
        return [match.start() for match in re.finditer(phrase, text)]
    # Iterate through each phrase in dict_val
    for phrase in dict_val:
        # Ensure whole words by using regex word boundaries
        if phrase in text_lower:
            # print(find_all(text, phrase),phrase,dict_val[phrase])
            for match in find_all(text_lower, phrase):
                matches.append((match, match + len(phrase), phrase, dict_val[phrase]))
    return matches


def find_matches(text, pattern, data_type, matches):
    # Iterate over all the matches.
    for match in re.finditer(pattern, text):
        start_index = match.start()
        end_index = match.end()
        # Format: [start, end, word, entity]
        match_tuple = [start_index, end_index, match.group(0), data_type]

        # Check for overlaps with existing matches
        not_overlapping = True
        if len(matches) > 0:
            not_overlapping = all(
                ((start < start_index and end < end_index) or (start > start_index and end > end_index)) for [start, end, _, _ ] in matches
            )

        # Add to the list if it doesn't overlap.
        if not_overlapping:
            matches.append(match_tuple)

    return matches

def redact_pii(text):

    start_time = datetime.now()

    # Patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    aadhaar_pattern = r'\b(\d{4}\s?\d{4}\s?\d{4})\b'
    pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
    bank_account_number_pattern = r'\b\d{14,18}\b'  # Assuming account numbers can be between 9 to 18 digits
    ifsc_code_pattern = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
    height_pattern = r'\b(\d{1,3})\s*(?:cm|centimeters|mm|millimeters|meters|m)\b'
    weight_pattern = r'\b\d+(?:\.\d+)?\s*(?:mg|g|kg|kilograms|tons?|lbs?|pounds|oz)\b'
    bmi_pattern = r"([0-9]+\.[0-9]+)\s*(kg\/m²?)"

    ipv4_pattern = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
    ipv6_pattern = (r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,"
                    r"6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,"
                    r"4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,"
                    r"4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{"
                    r"1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,"
                    r"1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(["
                    r"0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,"
                    r"1}[0-9]){0,1}[0-9]))")
    
    mac_address_pattern = r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b"

    bitcoin_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"
    ethereum_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"

    date_pattern = r"\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{1,2} [A-Za-z]{3} \d{4}|\d{4}[A-Za-z]{3}\d{2}|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4})\b"
    time_pattern = r"\b\d{2}:\d{2}(:\d{2})?\b"

    url_pattern = r'\b(?:https?|ftp|file):\/\/[-A-Za-z0-9+&@#\/%?=~_|!:,.;]*[-A-Za-z0-9+&@#\/%=~_|]\b'
    # file_path_pattern = r'\b(?:\/(?:[^\/\n]+\/)*[^\/\n]+|(?:(?:[A-Za-z]:)?\\|(?:file:\/\/\/))[^\n]+)\b'
    file_path_pattern = r'\b(?:\/(?:[^\/\s]+\/)*[^\/\s]+|(?:(?:[A-Za-z]:)?\\|(?:file:\/\/\/))[^\s]+)\b'

    vehicle_number_pattern = r'\b(?:[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}|[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,2}\s*\d{4})\b'

    gender_pattern = r'\b(?:male|female|man|woman|transgender|trans|non[-\s]?binary|gender[-\s]?fluid|gender[-\s]?queer|agender|bigender|pangender|androgyne|demiboy|demigirl|two[-\s]?spirit|gender[-\s]?nonconforming|gender[-\s]?variant|neutrois|intersex)\b'

    semantic_version_pattern = (r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-]["
                                    r"0-9a-zA-Z-])(?:\.(?:0|[1-9]\d|\d*[a-zA-Z-][0-9a-zA-Z-]))))?(?:\+([0-9a-zA-Z-]+("
                                    r"?:\.[0-9a-zA-Z-]+)*))?$")
    
    lat_long_pattern = r'\b-?\d{1,2}\.\d+,-?\d{1,3}\.\d+\b'

    port_pattern = (r"^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,"
                    r"5})|([0-9]{1,4}))$")
    
    ssn_pattern = r"^(?!(000|666|9))\d{3}-(?!00)\d{2}-(?!0000)\d{4}$|^(?!(000|666|9))\d{3}(?!00)\d{2}(?!0000)\d{4}$"

    passport_number_pattern = r'\b[A-Z][0-9]{7}\b'

    phone_number_pattern = r'((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}'

    zip_code_pattern = r'\b\d{6}\b'

    credit_card_pattern = r'\b(?:\d[ -]*?){13,16}\b'

    percent_pattern = r'((\+|-)?\d+(\.\d+)?%)|\d+(\.\d+)?%'

    matches = []

    # Find matched using functions
    find_matches(text, email_pattern, "[EMAIL]", matches)
    find_matches(text, aadhaar_pattern, "[AADHAAR]", matches)
    find_matches(text, pan_pattern, "[PAN]", matches)
    find_matches(text, bank_account_number_pattern, "[ACCOUNTNUMBER]", matches)
    find_matches(text, ifsc_code_pattern, "[IFSC]", matches)
    find_matches(text, height_pattern, "[HEIGHT]", matches)
    find_matches(text, weight_pattern, "[WEIGHT]", matches)
    find_matches(text, bmi_pattern, "[BMI]", matches)

    find_matches(text, ipv4_pattern, "[IPV4]", matches)
    find_matches(text, ipv6_pattern, "[IP]", matches)
    find_matches(text, mac_address_pattern, "[MAC]", matches)

    find_matches(text, bitcoin_address_pattern, "[BITCOINADDRESS]", matches)
    find_matches(text, ethereum_address_pattern, "[ETHEREUMADDRESS]", matches)

    find_matches(text, date_pattern, "[DATE]", matches)
    find_matches(text, time_pattern, "[TIME]", matches)

    find_matches(text, url_pattern, "[URL]", matches)
    find_matches(text, file_path_pattern, "[PATH]", matches)

    find_matches(text, vehicle_number_pattern, "[VEHICLENUMBER]", matches)

    find_matches(text, gender_pattern, "[GENDER]", matches)

    find_matches(text, semantic_version_pattern, "[VERSION]", matches)

    find_matches(text, lat_long_pattern, "[LATLNG]", matches)

    find_matches(text, port_pattern, "[PORT]", matches)

    find_matches(text, ssn_pattern, "[SSN]", matches)

    find_matches(text, passport_number_pattern, "[PASSPORT]", matches)

    find_matches(text, phone_number_pattern, "[PHONE_NUMBER]", matches)

    find_matches(text, zip_code_pattern, "[ZIPCODE]", matches)

    find_matches(text, credit_card_pattern, "[CREDITCARDNUMBER]", matches)

    find_matches(text, percent_pattern, "[PERCENT]", matches)

    find_matches_cache(text, location_dict, matches)

    # Sort matches based on start index
    matches.sort(key=lambda x: x[1])

    end_time = datetime.now()
    time_taken = ((end_time - start_time).total_seconds() * 1000)

    return ["rule-based", matches, time_taken]

if __name__ == "__main__":
    print("Rule based approach")