import os
import subprocess
import whisper
import json
import torch  # Add this line

# Directory containing the audio files
directory = r"C:\Users\kenne\Videos\Watch"

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=device)

# Load the Whisper model
# Lmodel = whisper.load_model("base")

print(model.device)

# Process each file in the directory
for filename in os.listdir(directory):
    
    if filename.endswith(".m4a") or filename.lower().endswith(".mp4"):
        # Get the base filename without the extension
        base_filename = os.path.splitext(filename)[0]
        # Construct the full path to the output .txt file
        full_path_txt = os.path.join(directory, base_filename + ".txt")
        # Construct the full path to the result.json file
        full_path_json = os.path.join(directory, base_filename + "_result.json")

        # Check if the output files already exist
        if os.path.exists(full_path_txt) and os.path.exists(full_path_json):
            print(f"Output files for {filename} already exist, skipping...")
            continue

        # Construct the full path to the file
        full_path_m4a = os.path.join(directory, filename)
        # Construct the full path to the output .wav file
        full_path_wav = os.path.join(directory, base_filename + ".wav")

        if not os.path.exists(full_path_wav):   
            # Convert the .m4a file to .wav using ffmpeg
            subprocess.run(["ffmpeg", "-i", full_path_m4a, full_path_wav])

        # Transcribe the .wav file using Whisper
        result = model.transcribe(full_path_wav)

        # Write the result to the result.json file
        with open(full_path_json, "w") as json_file:
            json.dump(result, json_file)

        # Write the transcription to a .txt file
        with open(full_path_txt, "w", encoding="utf-8") as f:
            f.write(str(result["text"]))

        print(f"Transcription for {filename} completed")