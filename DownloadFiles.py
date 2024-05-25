import os
import requests
import logging
import http.client
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from lxml import etree
from helpers.sitemap_helper import get_all_urls


sites_list = [
    "https://kendev.co",
]

file_formats = ['.xls', '.xlsx', '.doc', '.docx', '.pdf', '.zip', '.ppt', '.pptx']

def process_single_page(url, root_folder, project_path):
    logging.debug(f"Processing page {url}")

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    filename = path_parts[-1]
    extension = os.path.splitext(filename)[1]

    if extension.lower() in file_formats:
        target_folder = os.path.join(project_path, root_folder, parsed_url.hostname, *path_parts[:-1])
        target_file = os.path.join(target_folder, filename)

        os.makedirs(target_folder, exist_ok=True)
        response = requests.get(url)

        if response.status_code == 200:
            with open(target_file, 'wb') as f:
                f.write(response.content)
            logging.info(f'Downloaded {filename} from {url} to {target_file}')
        else:
            logging.warning(f'Unable to download {filename} from {url}: {response.status_code}')
    else:
        logging.debug(f'Ignoring file with invalid format: {filename}')

def download_files(url_list, root_folder, project_path, workers=4):
    logging.debug(f"Starting file_download function with {len(url_list)} URLs")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_page, url, root_folder, project_path) for url in url_list]
        for future in futures:
            logging.debug("Waiting for a thread to complete")
            future.result()
            logging.debug("Thread completed")

    logging.debug("All threads completed")

root_output_folder = "downloaded_files/"
project_path = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

for site in sites_list:
    all_unique_urls = get_all_urls(site, max_workers=os.cpu_count() * 2)
    download_files(all_unique_urls, root_output_folder, project_path)