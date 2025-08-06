import requests

def fun(url):

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the content of the response (HTML code of the webpage)
        return response.text
    else:
        return "Failed to retrieve webpage: {response.status_code}"