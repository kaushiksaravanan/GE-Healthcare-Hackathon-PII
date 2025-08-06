import ftplib

# Replace with your FTP server details
ftp_server = "192.168.18.40"
username = "fazil"
password = "fazil"

# Replace with the remote filename (path) on the FTP server
remote_filename = "test_file.txt"

try:
    # Connect to the FTP server
    ftp = ftplib.FTP(ftp_server)

    # Login with credentials
    ftp.login(username, password)
    print("Logged in successfully.")

    # Download the file content (using a buffer for efficiency)
    with ftplib.FTP(ftp_server) as ftp_plain:  # Basic FTP connection
        # Open a buffer to store the file content
        data = b""
        def download_callback(chunk):
            global data
            data += chunk

        # Retrieve the file content in binary mode
        ftp.retrbinary('RETR ' + remote_filename, download_callback, blocksize=8192)

        # Process the downloaded content (decode if necessary)
        print("Downloaded file content:")
        print(data.decode('utf-8'))  # Assuming UTF-8 encoding for text files (adjust if needed)

except ftplib.all_errors as e:
    print("Error:", e)
finally:
    # Close the FTP connection
    if ftp:
        ftp.quit()
        print("Disconnected from FTP server.")
