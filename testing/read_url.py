import requests

url = 'https://stackoverflow.com/questions/76360770/python-saying-table-does-no-exist-but-the-table-is-in-db-browser'  # Replace with the URL of the webpage you want to read

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the content of the response (HTML code of the webpage)
    print(response.text)
else:
    print(f"Failed to retrieve webpage: {response.status_code}")