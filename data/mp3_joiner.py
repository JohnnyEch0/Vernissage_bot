import os
from pydub import AudioSegment

folder_path = os.path.dirname(os.path.abspath(__file__))

def stitch_mp3_files(output_file):
    # Get all mp3 files in the folder
    mp3_files = [f for f in os.listdir(folder_path) if f.startswith("speech") and f.endswith(".mp3")]
    
    # Sort the files to ensure correct order
    mp3_files.sort(key=lambda x: int(x[6:-4]))  # Extract the number from "speech{i}.mp3"
    
    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()
    
    # Iterate through the sorted files and append each to the combined AudioSegment
    for mp3_file in mp3_files:
        full_path = os.path.join(folder_path, mp3_file)
        audio = AudioSegment.from_mp3(full_path)
        combined += audio
    
    # Export the combined audio to a new file
    combined.export(output_file, format="mp3")
    print(f"All MP3 files have been stitched together into {output_file}")

# Example usage
# Get the directory where the script is located


# Set the folder path to a 'data' subdirectory within the script's directory
if __name__ == "__main__":
    output_file = "combined_output.mp3"   # Name of the output file

    stitch_mp3_files(folder_path, output_file)
