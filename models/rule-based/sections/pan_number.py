import re

def find_pan_numbers(text):
    pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'

    pan_matches = re.finditer(pan_pattern, text)

    pan_data = [(match.group(0), match.start(), match.end()) for match in pan_matches]

    return pan_data

# Test the function
text = "My PAN number is ABCDE1234F."
pan_numbers = find_pan_numbers(text)
print("PAN numbers found:")
for pan, start, end in pan_numbers:
    print(f"PAN: {pan}, Start Index: {start}, End Index: {end}, Matched String: {text[start:end]}")
