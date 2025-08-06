import glob
import os
def fun(file_path):
    # Read and process each file
    try:
      all_contents = ""
      full_pattern = os.path.join(file_path, "*")
      print(full_pattern)
      for file in glob.glob(full_pattern):
          if (os.path.isfile(file)):
            with open(file, 'r') as f:
                content = f.read()
                all_contents += f"Content of {file}:\n"
                all_contents += content
                all_contents += "\n---\n"
      return all_contents
    except FileNotFoundError:
      return "Error: File not found at {file_path}"
    except Exception as e:
      return e

# def fun(file_path):
  
#   default_file_path = "D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/ftp/test_file.txt"

#   try:
#     # Open the file in read mode with context manager for automatic closing
#     with open(file_path, 'r') as file:
#       # Read all contents of the file into a string
#       contents = file.read()
#       return contents
#   except FileNotFoundError:
#     return "Error: File not found at {file_path}"
#   except Exception as e:
#     return "An error occurred while reading the file"

# res = fun("D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/assets")
# print(res)