from urllib.request import urlopen

# Replace with your FTP server details (ensure anonymous login is allowed)
ftp_url = f"ftp://{your_ftp_server_address}/{remote_filename}"

try:
    # Open the FTP URL
    with urlopen(ftp_url) as response:
        # Read the file content and decode (assuming UTF-8 encoding for text files)
        data = response.read().decode('utf-8')
        print("Downloaded file content:")
        print(data)

except Exception as e:
    print("Error:", e)
