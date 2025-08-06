import re

def find_bank_info(text):
    # Regular expression patterns for Indian bank account numbers and IFSC codes
    account_number_pattern = r'\b\d{9,18}\b'  # Assuming account numbers can be between 9 to 18 digits
    ifsc_code_pattern = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'

    # Find all occurrences of bank account numbers and IFSC codes in the text
    account_number_matches = re.finditer(account_number_pattern, text)
    ifsc_code_matches = re.finditer(ifsc_code_pattern, text)

    # Extract the start and end indices of each match
    account_numbers = [(match.group(0), match.start(), match.end()) for match in account_number_matches]
    ifsc_codes = [(match.group(0), match.start(), match.end()) for match in ifsc_code_matches]

    return account_numbers, ifsc_codes

# Test the function
text = "My bank account number is 123456789012345 and IFSC code is ABCD0123456."
account_numbers, ifsc_codes = find_bank_info(text)
print("Bank account numbers found:")
for account_number, start, end in account_numbers:
    print(f"Account Number: {account_number}, Start Index: {start}, End Index: {end}, Matched String: {text[start:end]}")
print("\nIFSC codes found:")
for ifsc_code, start, end in ifsc_codes:
    print(f"IFSC Code: {ifsc_code}, Start Index: {start}, End Index: {end}, Matched String: {text[start:end]}")
