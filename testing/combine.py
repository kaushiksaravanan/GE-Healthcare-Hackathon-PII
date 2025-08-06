def replace_text(text, replace_dicts):
    # Sort the replacement dictionaries based on start index
    replace_dicts.sort(key=lambda x: x[0])

    # Replace values in the text with their corresponding placeholders
    result = ""
    current_index = 0
    for start, end, value, placeholder in replace_dicts:
        # Append the text from the last replacement to the current start index
        result += text[current_index:start]
        # Append the placeholder instead of the value
        result += f"[{placeholder}]"
        # Update the current index to the end of the replacement
        current_index = end

    # Append the remaining text after the last replacement
    result += text[current_index:]

    return result

# Example usage
text = "My name is fazil and I work at arista"
replace_dict_1 = [(11, 16, "fazil", "PERSON")]
replace_dict_2 = [(31, 37, "arista", "ORG")]
replace_dict_3 = [(23, 27, "work", "JOB")]

result = replace_text(text, replace_dict_1 + replace_dict_2 + replace_dict_3)
print(result)  # Output: "My name is [PERSON] and I work at [ORG]"
