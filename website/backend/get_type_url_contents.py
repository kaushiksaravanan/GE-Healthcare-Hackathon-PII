import requests
from bs4 import BeautifulSoup

def fun(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the text from the parsed HTML
        page_text = soup.get_text(separator='\n', strip=True)
        
        # Print the extracted text
        return page_text
    else:
        return "Failed to retrieve webpage: {response.status_code}"
