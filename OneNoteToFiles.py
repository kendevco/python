import os
import json
import requests
from lxml import html
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()
 
# Read the access token from environment variable
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
 
# Set up the Graph API connection
GRAPH_SCOPE = ['https://graph.microsoft.com/.default']
PAGE_FOLDER = 'pages'
 
def sanitize_filename(filename: str) -> str:
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
 
def get_notebooks(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
 
    notebooks_endpoint = 'https://graph.microsoft.com/v1.0/me/onenote/notebooks'
    res = requests.get(notebooks_endpoint, headers=headers)
    response = res.json()
    return response['value']
 
def download_onenote_pages(token):
    for notebook in get_notebooks(token):
        notebook_name = sanitize_filename(notebook['displayName'])
        notebook_dir = os.path.join(PAGE_FOLDER, notebook_name)
        os.makedirs(notebook_dir, exist_ok=True)
 
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
 
        sections_endpoint = f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook['id']}/sections"
        sections_res = requests.get(sections_endpoint, headers=headers)
        sections_response = sections_res.json()
 
        for section in sections_response['value']:
            section_name = sanitize_filename(section['displayName'])
            section_dir = os.path.join(notebook_dir, section_name)
            os.makedirs(section_dir, exist_ok=True)
 
            pages_endpoint = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section['id']}/pages"
            res = requests.get(pages_endpoint, headers=headers)
            response = res.json()
 
            for page in response['value']:
                html_endpoint = page['contentUrl']
                html_content = requests.get(html_endpoint, headers=headers).text
                html_tree = html.fromstring(html_content)
 
                # Extract page title and content
                title = "".join(html_tree.xpath("//title/text()")).strip()
                sanitized_title = sanitize_filename(title)
                main_text = "".join(html_tree.xpath("//p/text()")).strip()
 
                # Save to a text file
                with open(os.path.join(section_dir, f'{sanitized_title}.txt'), 'w', encoding='utf-8') as f:
                    f.write(main_text)
 
                    content_length = len(main_text)
 
                    # Extract OCR'd image text from img element's "data-ocr-text" attribute
                    for img in html_tree.xpath("//img[@data-ocr-text]"):
                        ocr_text = img.get('data-ocr-text')
                        f.write('\n\n')
                        f.write(ocr_text)
 
                        content_length += len(ocr_text)
 
                    # Extract Text-to-Speech embedded audio results
                    for audio in html_tree.xpath("//audio[@data-tts-text]"):
                        tts_text = audio.get('data-tts-text')
                        f.write('\n\n')
                        f.write(tts_text)
 
                        content_length += len(tts_text)
 
                print(f"Written {notebook_name}/{section_name}/{sanitized_title}.txt with {content_length} characters")
 
if __name__ == '__main__':
    download_onenote_pages(ACCESS_TOKEN)
