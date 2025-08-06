import re

def detect_bmi(text):
  """
  This function detects BMI data in the provided text and returns information with start and end indices.

  Args:
      text: The text string to search for BMI data.

  Returns:
      A list of dictionaries containing keys:
          value (float): The parsed BMI value.
          unit (str, optional): The unit of the BMI value (if found).
          start_index (int): The starting index of the BMI value in the text.
          end_index (int): The ending index (exclusive) of the BMI value in the text.
  """
  # Regex pattern for BMI values (float number)
  bmi_pattern = r"([0-9]+\.[0-9]+)"

  # Regex pattern for optional unit (kg/m2)
  unit_pattern = r"\s*(kg\/m²?)"

  matches = []
  for match in re.finditer(bmi_pattern, text):
    value = float(match.group())
    unit = None
    start_index = match.start()
    # Check if unit pattern exists after the value
    unit_match = re.search(unit_pattern, text[match.end():])
    if unit_match:
      unit = "kg/m²"
      end_index = unit_match.end() + match.end()  # Include unit in end index
    else:
      end_index = match.end()  # Only BMI value

    matches.append({"value": value, "unit": unit, "start_index": start_index, "end_index": end_index})
  return matches

# Example usage
text = "Your BMI is 25.3 kg/m2. This is considered overweight."
matches = detect_bmi(text)

if matches:
  for match in matches:
    print(f"Found BMI: value: {match['value']}{' ' + match['unit'] if match['unit'] else ''}, start: {match['start_index']}, end: {match['end_index']}")
else:
  print("No BMI data found in the text.")
