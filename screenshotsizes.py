# Importing the required libraries
import os

# Initialize variables to hold total size and total number of files
total_size = 0
total_files = 0

# Specify the root directory from where to start the search. Replace this with the actual path.
root_directory = "D:\Dev\Python\screenshots"

# Iterate through the directories and sub-directories
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        # Construct the full path to the file
        file_path = os.path.join(dirpath, filename)
        
        # Get the file size and add it to the total
        file_size = os.path.getsize(file_path)
        total_size += file_size
        total_files += 1

# Calculate the average size
if total_files == 0:
    average_size = 0
else:
    average_size = total_size / total_files

# Convert bytes to kilobytes (1 KB = 1024 Bytes)
average_size_kb = average_size / 1024

# Output the results
print(f"Total size: {total_size} bytes")
print(f"Total files: {total_files}")
print(f"Average size: {average_size_kb:.2f} KB")