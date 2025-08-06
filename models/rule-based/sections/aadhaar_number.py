import re

def find_aadhaar(text):
    aadhaar_pattern = r'\b(\d{4}\s?\d{4}\s?\d{4})\b'

    aadhaar_matches = re.finditer(aadhaar_pattern, text)

    aadhaar_data = [(match.group(1), match.start(), match.end()) for match in aadhaar_matches]

    return aadhaar_data

# Test the function
text = "My Aadhaar number is 1234 5678 9012."
aadhaar_numbers = find_aadhaar(text)
print("Aadhaar numbers found:")
for aadhaar, start, end in aadhaar_numbers:
    print(f"Aadhaar: {aadhaar}, Start Index: {start}, End Index: {end}, Matched String: {text[start:end]}")
