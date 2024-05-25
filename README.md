# Audio Transcription with Whisper

This project is a Python script that transcribes audio files using the Whisper model developed by OpenAI. It supports transcribing audio files in various formats, including `.m4a` and `.mp4`.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.6 or later installed on your system
- FFmpeg installed (for converting audio files to `.wav` format)

## Installation

1. Clone the repository or download the source code.
2. Install the required Python packages by running the following command:
    ```sh
    pip install openai whisper torch
    ```

3. Download the Whisper model by running the following command:
    ```sh
    python -m whisper.utils transcribe --model_dir /path/to/model/dir
    ```
   Replace `/path/to/model/dir` with the directory where you want to download the Whisper model.

## Usage

1. Open the `WhisperDirectory2.py` file and modify the `directory` variable to point to the directory containing your audio files.

2. (Optional) If you have an NVIDIA GPU and want to use it for faster transcription, uncomment the following line in the script:
    ```python
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ```

3. Run the script with the following command:
    ```sh
    python WhisperDirectory2.py
    ```

The script will process each audio file in the specified directory, transcribe it using the Whisper model, and save the transcription as a text file with the same name as the audio file (but with a `.txt` extension) in the same directory.

## Notes

- The script supports audio files with the following extensions: `.m4a` and `.mp4`.
- If an audio file is in the `.m4a` or `.mp4` format, the script will first convert it to a `.wav` file using FFmpeg before transcribing it.
- The script uses the base model of Whisper by default. You can change the model by modifying the `model` variable in the script.
- If you have an NVIDIA GPU and want to use it for faster transcription, make sure you have the appropriate CUDA drivers installed and the `torch` package is installed with GPU support.

## License

This project is licensed under the MIT License.

---

# PDF Text Extraction with OpenAI GPT-4

This project is a Python script that extracts text from PDF files using OpenAI's GPT-4 model. It converts each page of a PDF file into an image, sends the image to the GPT-4 model for text extraction, and saves the extracted text in a Word document (.docx) file.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.6 or later installed on your system
- OpenAI API key (sign up at [OpenAI](https://openai.com/) to get an API key)

## Installation

1. Clone the repository or download the source code.
2. Install the required Python packages by running the following command:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Set your OpenAI API key as an environment variable:

- On Windows:
    ```sh
    setx OPENAI_API_KEY "your_openai_api_key"
    ```
- On Linux/macOS:
    ```sh
    export OPENAI_API_KEY="your_openai_api_key"
    ```
Replace `"your_openai_api_key"` with your actual OpenAI API key.

(Optional) Modify the `TEMP_DIR` and `CACHE_DIR` variables in the `ChunkGPT4o.py` file to specify the desired locations for temporary and cache files.

## Usage

1. Place the PDF files you want to process in a directory on your system.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the `ChunkGPT4o.py` script with the following command:
    ```sh
    python ChunkGPT4o.py /path/to/pdf/files/directory
    ```
   Replace `/path/to/pdf/files/directory` with the actual path to the directory containing your PDF files.

The script will process each PDF file, convert each page to an image, analyze the image with the GPT-4 model, and generate a `.docx` file with the analysis results. The `.docx` files will be saved in the temp directory (or the directory specified by the `TEMP_DIR` variable).

## Notes

- The script supports PDF files only. Other file formats will be skipped.
- The script uses multithreading to process multiple PDF files concurrently, which can improve performance on systems with multiple CPU cores.
- The script caches the results of processed images to avoid redundant API calls and improve performance for subsequent runs.

## License

This project is licensed under the MIT License.

---

## Files in the Project

- **ChunkGPT4o.py**: This script processes PDF files by converting each page to an image, sending the image to the OpenAI GPT-4 model for text extraction, and saving the extracted text in a Word document (.docx) file.
- **Screenshots.py**: Contains helper functions for creating output directories.
- **Screenshotwebsites.py**: Takes screenshots of websites and saves them to a specified directory.
- **OneNoteToFiles.py**: Downloads OneNote pages and saves them as text files.
- **parserewrites.py**: Parses an XML file and extracts data from it.
- **parse_links.py**: Extracts links from a website and saves them to a CSV file.
- **FBJLinks.py**: Retrieves the sitemap XML file for a given website.
- **WhisperDirectory.py**: Transcribes audio files using the Whisper model.
- **WhisperDirectory2.py**: Main script for transcribing audio files.
- **WhisperDirectory3.py**: Transcribes audio files using the Whisper model and the OpenAI API.
- **vtt2text.py** and **vtt2text2.py**: Convert VTT files to text files.
- **ScreenshotWebsitesv2.py** and **ScreenshotWebsitesv3.py**: Take screenshots of websites and save them to a specified directory.

---

## Running WhisperDirectory2.py

`WhisperDirectory2.py` is a script that transcribes audio files using the Whisper model. Here are the steps to run it:

1. Make sure you have Python 3.6 or later installed on your system.
2. Install the required Python packages by running the following command:
    ```sh
    pip install openai whisper torch
    ```

3. Download the Whisper model by running the following command:
    ```sh
    python -m whisper.utils transcribe --model_dir /path/to/model/dir
    ```
   Replace `/path/to/model/dir` with the directory where you want to download the Whisper model.

4. Open the `WhisperDirectory2.py` file and modify the `directory` variable to point to the directory containing your audio files.

5. (Optional) If you have an NVIDIA GPU and want to use it for faster transcription, uncomment the following line in the script:
    ```python
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ```

6. Run the script with the following command:
    ```sh
    python WhisperDirectory2.py
    ```

The script will process each audio file in the specified directory, transcribe it using the Whisper model, and save the transcription as a text file with the same name as the audio file (but with a `.txt` extension) in the same directory.

## Notes

- The script supports audio files with the following extensions: `.m4a` and `.mp4`.
- If an audio file is in the `.m4a` or `.mp4` format, the script will first convert it to a `.wav` file using FFmpeg before transcribing it.
- The script uses the base model of Whisper by default. You can change the model by modifying the `model` variable in the script.
- If you have an NVIDIA GPU and want to use it for faster transcription, make sure you have the appropriate CUDA drivers installed and the `torch` package is installed with GPU support.

By embracing AI and custom solutions, we can overcome challenges and achieve results that were once thought impossible. Happy coding!
