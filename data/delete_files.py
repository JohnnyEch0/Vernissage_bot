import os

RELEVANT_FILES = ".mp3"
# Get the current directory
current_dir = os.path.join(os.getcwd(), "data")

# Iterate through files in the current directory
for filename in os.listdir(current_dir):
    # Check if the file has .mp3 extension
    if filename.lower().endswith(RELEVANT_FILES):
        file_path = os.path.join(current_dir, filename)
        try:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {filename}")
        except OSError as e:
            print(f"Error deleting {filename}: {e}")

print("Deletion process completed.")
