import re

def find_height_and_weight(text):
    height_pattern = r'\b(\d{1,3})\s*(?:cm|centimeters|mm|millimeters|meters|m)\b'
    weight_pattern = r'\b(\d{1,3})\s*(?:kg|kilograms|lbs|pounds)\b'

    height_matches = re.finditer(height_pattern, text)
    weight_matches = re.finditer(weight_pattern, text)

    heights = [(match.group(0), match.start(), match.end()) for match in height_matches]
    weights = [(match.group(0), match.start(), match.end()) for match in weight_matches]

    return heights, weights

# Test the function
text = "He is 180 cm tall and weighs 75 kg."
heights, weights = find_height_and_weight(text)
print("Heights found:")
for height, start, end in heights:
    print(f"Height: {height}, Start Index: {start}, End Index: {end}")
print("\nWeights found:")
for weight, start, end in weights:
    print(f"Weight: {weight}, Start Index: {start}, End Index: {end}")
