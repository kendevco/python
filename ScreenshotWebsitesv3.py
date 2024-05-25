import os
import requests
from PIL import Image
from bs4 import BeautifulSoup
import csv
import logging
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER as SELENIUM_LOGGER
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urljoin, urlparse
import time

sites_list = ["https://folio.kendev.co/"]

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def create_screenshot_path(url, base_folder, project_path):
    parsed_url = urlparse(url)
    filename = 'default.png' if parsed_url.path.strip() in ('', '/') else '_'.join(parsed_url.path.strip('/').split('/')) + '.png'
    target_folder = os.path.join(project_path, base_folder, parsed_url.hostname)
    os.makedirs(target_folder, exist_ok=True)
    return os.path.join(target_folder, filename)

def does_screenshot_exist(url, base_folder, project_path):
    return os.path.exists(create_screenshot_path(url, base_folder, project_path))

def take_single_screenshot(url, root_folder, project_path):
    logging.debug(f"Taking screenshot of {url}")
 
    # Set up the ChromeDriver service
    service = Service(executable_path='C:\ProgramData\chromedriver\chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    SELENIUM_LOGGER.setLevel(logging.WARNING)   
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.set_page_load_timeout(60)

    def page_is_visually_loaded(driver):
        return driver.execute_script("return document.readyState") == 'complete' and \
               driver.execute_script("return Array.from(document.images).every(img => img.complete);")

    try:
        browser.get(url)      
        WebDriverWait(browser, 60).until(page_is_visually_loaded)
        
    except (TimeoutException, Exception) as e:
        logging.warning(f"Error occurred while loading {url}: {str(e)}. Skipping screenshot.")
        browser.quit()
        return False
    
    screenshot_path = create_screenshot_path(url, root_folder, project_path)
    S = lambda X: browser.execute_script('return document.body.parentNode.scroll' + X)
    browser.set_window_size(1280, max(S('Height'), 720))
    ActionChains(browser).send_keys(Keys.END).perform()
    prefs = {"profile.managed_default_content_settings.images": -1}
    chrome_options.add_experimental_option("prefs", prefs)
    browser.save_screenshot(screenshot_path)
    browser.quit()

    crop_screenshot(screenshot_path)

def take_screenshots(url_list, root_folder, project_path):
    urls_to_screenshot = [url for url in url_list if not does_screenshot_exist(url, root_folder, project_path)]
    num_screenshots = len(urls_to_screenshot)
    max_workers = min(num_screenshots, max(1, os.cpu_count() - 1))
    if max_workers > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda url: take_single_screenshot(url, root_folder, project_path), urls_to_screenshot)

def crop_screenshot(img_path, strip_width=20):
    screenshot = Image.open(img_path)
    strip_start = screenshot.width // 2 - strip_width // 2
    strip_end = strip_start + strip_width
    initial_color = screenshot.getpixel((strip_start, screenshot.height - 1))
    for y in range(screenshot.height - 1, 0, -1):
        if any(screenshot.getpixel((x, y)) != initial_color for x in range(strip_start, strip_end)):
            break
    cropped_screenshot = screenshot.crop((0, 0, screenshot.width, y))
    cropped_screenshot.save(img_path)
    
def get_sitemap_urls(base_url):
    try:
        response = requests.get(urljoin(base_url, "/Sitemap.aspx"))
        soup = BeautifulSoup(response.content, "xml")
        return [url_element.find("loc").text for url_element in soup.find_all("url") if url_element.find("loc")]
    except Exception as e:
        logging.warning(f"Failed to retrieve a sitemap from {base_url}: {str(e)}. Falling back to spider crawl.")
        return get_all_website_links(base_url)


def save_links_to_csv(base_url, urls):
    filename = base_url.replace(".", "_").replace("/", "_").replace(":", "_") + '.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for url in urls:
            writer.writerow([url])

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url, urls=set()):
    domain_name = urlparse(url).netloc

    try:
        print(f"Processing: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid_url(href):
                continue
            if href in urls:
                continue
            if domain_name not in href:
                continue
            urls.add(href)
            get_all_website_links(href, urls)
        time.sleep(1)
    except (requests.exceptions.TooManyRedirects, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(f"Error occurred while processing {url}: {str(e)}")

    save_links_to_csv(url, urls)
    return urls

root_output_folder = "screenshots/"
project_path = os.path.dirname(os.path.abspath(__file__))

for site in sites_list:
    site_sitemap_urls = get_all_website_links(site)
    unique_site_sitemap_urls = list(set(site_sitemap_urls))
    take_screenshots(unique_site_sitemap_urls, root_output_folder, project_path)