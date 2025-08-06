import re

def find_matches(text, pattern, data_type, matches):
    # Iterate over all the matches.
    for match in re.finditer(pattern, text):
        start_index = match.start()
        end_index = match.end()
        match_tuple = (match.group(0), start_index, end_index, data_type)

        # Check for overlaps with existing matches
        not_overlapping = True
        if len(matches) > 0:
            not_overlapping = all(
                ((start < start_index and end < end_index) or (start > start_index and end > end_index)) for _, start, end, _ in matches
            )

        # Add to the list if it doesn't overlap.
        if not_overlapping:
            matches.append(match_tuple)

    return matches

def find_pii_info(text):
    # Patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    aadhaar_pattern = r'\b(\d{4}\s?\d{4}\s?\d{4})\b'
    pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
    bank_account_number_pattern = r'\b\d{9,18}\b'  # Assuming account numbers can be between 9 to 18 digits
    ifsc_code_pattern = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
    height_pattern = r'\b(\d{1,3})\s*(?:cm|centimeters|mm|millimeters|meters|m)\b'
    weight_pattern = r'\b(\d{1,3})\s*(?:kg|kilograms|lbs|pounds)\b'
    bmi_pattern = r"([0-9]+\.[0-9]+)\s*(kg\/m²?)"

    matches = []

    # Find matched using functions
    find_matches(text, email_pattern, "email", matches)
    find_matches(text, aadhaar_pattern, "aadhaar", matches)
    find_matches(text, pan_pattern, "PAN", matches)
    find_matches(text, bank_account_number_pattern, "Bank Account Number", matches)
    find_matches(text, ifsc_code_pattern, "IFSC", matches)
    find_matches(text, height_pattern, "height", matches)
    find_matches(text, weight_pattern, "weight", matches)
    find_matches(text, bmi_pattern, "BMI", matches)

    # Sort matches based on start index
    matches.sort(key=lambda x: x[1])

    return matches

# Test the function
text = "He is 180 cm tall and weighs 75 kg. Send an email to user@example.com or another.email@example.co.uk. My PAN number is ABCDE1234F. My bank account number is 123456789012345 and IFSC code is ABCD0123456. My Aadhaar number is 1234 5678 9012. Your BMI is 25.3 kg/m2. This is considered overweight."
data = find_pii_info(text)
print("Sentence:", text)
for item in data:
    print(f"Word: {item[0]}, Start Index: {item[1]}, End Index: {item[2]}, Type: {item[3]}")
