import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to read
url = 'https://stackoverflow.com/questions/76360770/python-saying-table-does-no-exist-but-the-table-is-in-db-browser'  # Replace with the actual URL

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the text from the parsed HTML
    page_text = soup.get_text(separator='\n', strip=True)
    
    # Print the extracted text
    print(page_text)
else:
    print(f"Failed to retrieve webpage: {response.status_code}")
