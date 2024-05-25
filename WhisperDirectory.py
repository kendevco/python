import os
import subprocess
import stable_whisper

# Load the whisper model
model = stable_whisper.load_model("base")

def convert_to_wav(filename):
    # Convert the audio file to wav using ffmpeg
    wav_filename = f"{os.path.splitext(filename)[0]}.wav"
    subprocess.run(["ffmpeg", "-i", filename, wav_filename])
    return wav_filename

def transcribe_file(filename):
    # Convert audio files to wav before transcribing
    if filename.lower().endswith(tuple(supported_extensions)):
        filename = convert_to_wav(filename)
        
    # Then, transcribe the audio
    result = model.transcribe(filename)

    # Save the transcription to a text file with the same name
    transcript_filename = f"{os.path.splitext(filename)[0]}.txt"
    with open(transcript_filename, 'w') as file:
        file.write(result)

    # Print the transcription filename
    print(f"Transcription saved to {transcript_filename}")

# File extensions supported by ffmpeg for conversion to wav
supported_extensions = [".mp3", ".mp4", ".flac", ".m4a"]

# Specify the directory containing your audio files
audio_directory =  r"C:\Users\kenne\Videos\Watch"

# Transcribe all supported audio files in the directory
for entry in os.scandir(audio_directory):
    if entry.path.lower().endswith(tuple(supported_extensions)):
        transcript_path = f"{os.path.splitext(entry.path)[0]}.txt"
        if os.path.exists(transcript_path):
            print(f"Skipping {entry.name} as a transcript file already exists.")
        else:
            print(f"Transcribing {entry.name}")
            transcribe_file(entry.path)