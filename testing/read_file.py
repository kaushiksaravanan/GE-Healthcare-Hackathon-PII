def read_entire_file(file_path):
  """
  Reads the entire contents of a file at the given path.

  Args:
      file_path: The path to the file to read.

  Returns:
      A string containing the entire contents of the file, or None if the file
      could not be read.
  """

  try:
    # Open the file in read mode with context manager for automatic closing
    with open(file_path, 'r') as file:
      # Read all contents of the file into a string
      contents = file.read()
      return contents
  except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    return None
  except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    return None

# Example usage
file_contents = read_entire_file("D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/ftp/test_file.txt")

if file_contents:
  print(file_contents)
else:
  print("Failed to read the file.")