import re

def find_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.finditer(pattern, text)
    emails = []
    for match in matches:
        start_index = match.start()
        end_index = match.end()
        email = match.group(0)
        emails.append((email, start_index, end_index))
    return emails

# Test the function
text = "Send an email to user@example.com or another.email@example.co.uk"
emails_found = find_emails(text)
print("Emails found:")
for email, start, end in emails_found:
    print(f"Email: {email}, Start Index: {start}, End Index: {end}")