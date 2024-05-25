import os
import shutil
import fitz  # PyMuPDF
import base64
import openai
import logging
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')
logger = logging.getLogger()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY') or 'YOUR_OPENAI_API_KEY'

# Directory for temporary files
TEMP_DIR = "temp"
CACHE_DIR = os.path.join(TEMP_DIR, "cache")

# Ensure the temp and cache directories exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Function to encode image to base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        return None

# Function to process PDF and save pages as images
def process_pdf(file_path):
    try:
        pdf_document = fitz.open(file_path)
        output_images = []

        for page_num in range(len(pdf_document)):
            img_path = os.path.join(TEMP_DIR, f"{os.path.basename(file_path)}_page_{page_num + 1}.png")
            if os.path.exists(img_path):
                logger.info(f"Skipping existing file: {img_path}")
                output_images.append(img_path)
                continue
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            pix.save(img_path)
            output_images.append(img_path)
            logger.info(f"Saved image: {img_path}")

        return output_images
    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {e}")
        return []

# Function to create messages for images
def create_image_message(image_file):
    image_content = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_image(image_file)}"}}
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all text from this image. Correct minor errors and provide only the text."},
                image_content
            ]
        }
    ]

# Function to analyze a single image
def analyze_image(image_file):
    cache_path = os.path.join(CACHE_DIR, os.path.basename(image_file) + ".txt")
    if os.path.exists(cache_path):
        logger.info(f"Cache hit for image {image_file}")
        with open(cache_path, "r") as cache_file:
            return cache_file.read()

    logger.info(f"Processing image {image_file} with OpenAI")
    messages = create_image_message(image_file)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2500  # Updated token limit
        )
        image_result = response.choices[0]['message']['content']

        with open(cache_path, "w") as cache_file:
            cache_file.write(image_result)

        return image_result
    except Exception as e:
        logger.error(f"Error processing image {image_file}: {e}")
        return "Error processing image."

# Function to process directory and generate a .docx file
def process_directory(directory, cleanup=True):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not filename.endswith('.pdf'):
            logger.info(f"Skipping non-PDF file: {filename}")
            continue

        logger.info(f"Processing PDF: {filename}")
        output_docx = os.path.join(TEMP_DIR, f"{os.path.splitext(filename)[0]}.docx")

        # Ensure file overwriting
        if os.path.exists(output_docx):
            os.remove(output_docx)

        document = Document()
        try:
            image_files = process_pdf(file_path)
            for img_path in image_files:
                analysis_result = analyze_image(img_path)
                try:
                    page_number = image_files.index(img_path) + 1
                    heading = f"{os.path.basename(file_path)} - Page {page_number}"
                    document.add_heading(heading, level=2)

                    paragraph = document.add_paragraph()
                    run = paragraph.add_run()
                    run.add_picture(img_path, width=Inches(3.75))  # Centered image at 50% scale
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

                    paragraph = document.add_paragraph(analysis_result)
                    paragraph_format = paragraph.paragraph_format
                    paragraph_format.left_indent = Inches(0.5)
                    paragraph_format.right_indent = Inches(0.5)
                    paragraph_format.space_before = Inches(0.5)
                    paragraph_format.space_after = Inches(0.5)

                    # Adding a page break after each page's content
                    document.add_page_break()
                except Exception as e:
                    logger.error(f"Error adding content for image {img_path}: {e}")
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")

        try:
            document.save(output_docx)
            logger.info(f"Document saved as {output_docx}")
        except Exception as e:
            logger.error(f"Error saving document {output_docx}: {e}")

    # Clean up temporary files if specified
    if cleanup:
        try:
            shutil.rmtree(TEMP_DIR)
            logger.info(f"Temporary files cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {e}")

if __name__ == "__main__":
    # Test with saving to temp\output.docx, and do not cleanup temp images
    process_directory(r"C:\Users\kenne\Videos\Captures\Process", cleanup=False)
