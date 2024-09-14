import os
from pydub import AudioSegment

folder_path = os.path.dirname(os.path.abspath(__file__))

def stitch_mp3_files(output_file):
    mp3_files = [f for f in os.listdir(folder_path) if f.startswith("speech") and f.endswith(".mp3")]
    mp3_files.sort(key=lambda x: int(x[6:-4]))
    combined = AudioSegment.empty()
    for mp3_file in mp3_files:
        full_path = os.path.join(folder_path, mp3_file)
        audio = AudioSegment.from_mp3(full_path)
        combined += audio
    combined.export(output_file, format="mp3")
    print(f"All MP3 files have been stitched together into {output_file}")



if __name__ == "__main__":
    output_file = "combined_output.mp3"   # Name of the output file
    stitch_mp3_files(folder_path, output_file)
