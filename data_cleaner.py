import os
import pandas as pd

# Define the directory path
directory = 'data/features'

# Initialize counters
total_files = 0
empty_files = 0

# Iterate through the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):  # Assuming the files are in CSV format
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        total_files += 1
        if df.empty:
            empty_files += 1

# Calculate the percentage of empty files
empty_percentage = (empty_files / total_files) * 100

# Prompt user for confirmation to delete empty files
confirmation = input(f"There are {empty_files} empty files out of {total_files} total files. Do you want to delete them? (yes/no): ")

if confirmation.lower() == 'yes':
    # Delete empty files
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            if df.empty:
                os.remove(file_path)
                print(f"Deleted {filename}")
else:
    print("No files were deleted.")