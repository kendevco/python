import os
import subprocess
import openai
from pydub import AudioSegment
import logging

# Set your OpenAI API key
openai.api_key = "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"

# Set the directory path containing the MP4 files
directory =  r"D:\Dev\Fullstack\Transcribe"


# Set up logging
logging.basicConfig(filename='transcribe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Iterate over the files in the directory
files = os.listdir(directory)

for filename in files:
    if filename.endswith(".mp4"):
        # Construct the input and output file paths
        input_file = os.path.join(directory, filename)
        output_file = os.path.splitext(input_file)[0] + ".mp3"
        transcript_file = os.path.splitext(input_file)[0] + ".txt"

        # Skip if the MP3 or transcript file already exists
        if os.path.exists(output_file):
            logging.info(f"Skipping converting {filename} - MP3 already exists")
        else:
            # Check if the MP4 file is playable using ffprobe
            result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0 or result.stdout.strip() != b"mp3":
                # Copy the audio stream to a new MP3 file using FFmpeg's copy codec
                subprocess.run(["ffmpeg", "-i", input_file, "-codec:a", "copy", output_file])
                logging.info(f"Fixed {filename} - copied audio stream to new MP3 file")
            else:
                # Convert the MP4 file to MP3 using FFmpeg
                subprocess.run(["ffmpeg", "-i", input_file, "-codec:a", "libmp3lame", output_file])
                logging.info(f"Converted {filename} to MP3")

        # Skip if the MP3 or transcript file already exists
        if os.path.exists(transcript_file):
            logging.info(f"Skipping {filename} - transcript file already exists")
            continue

        # Open the MP3 audio file in binary mode
        audio = AudioSegment.from_file(output_file, format="mp3")

        # Set the chunk size to 10 MB
        chunk_size = 5 * 1024 * 1024  # 10 MB

        # Iterate through the audio in chunks
        for i in range(0, len(audio), chunk_size):
            # Get the current chunk
            chunk = audio[i:i+chunk_size]

            # Export the chunk as a temporary MP3 file
            chunk_file = f"chunk_{i}.mp3"
            chunk.export(chunk_file, format="mp3")

            # Open the chunk audio file in binary mode
            audio_file = open(chunk_file, "rb")

            # Transcribe the audio using the Whisper model
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

            # Convert the transcript to a string
            transcript_str = str(transcript)

            # Print the transcription
            logging.info(f"Transcription for {filename} (Chunk {i+1}): {transcript_str}")

            # Save the transcript to a text file
            with open(transcript_file, "a") as f:
                f.write(transcript_str)

            # Close the audio file and remove the temporary chunk file
            audio_file.close()
            os.remove(chunk_file)

        logging.info(f"Transcription for {filename} completed")