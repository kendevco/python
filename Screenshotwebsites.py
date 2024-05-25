import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

def create_screenshot_path(url, base_folder, project_path):
    parsed_url = urlparse(url)

    # Determine the filename based on the URL path
    if parsed_url.path.strip() == '' or parsed_url.path.strip() == '/':
        filename = 'default.png'
    else:
        # Join folder and file names with underscores
        filename = '_'.join(parsed_url.path.strip('/').split('/')) + '.png'

    target_folder = os.path.join(project_path, base_folder, parsed_url.hostname)
    os.makedirs(target_folder, exist_ok=True)
    target_file = os.path.join(target_folder, filename)

    return target_file

def take_screenshots(url_list, root_folder,  project_path):
    # Set up the ChromeDriver service
    service = Service(executable_path='C:\ProgramData\chromedriver\chromedriver.exe')

    # Create a new Chrome browser instance with desired options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # Loop through the list of URLs and take screenshots
    for url in url_list:
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Save the screenshot with the desired name
        screenshot_path = create_screenshot_path(url, root_folder, project_path)

        desired_width, desired_height = 1280, 720
        S = lambda X: browser.execute_script('return document.body.parentNode.scroll'+X)
        browser.set_window_size(desired_width, max(S('Height'), desired_height))
        ActionChains(browser).send_keys(Keys.HOME).perform()
        browser.save_screenshot(screenshot_path)

        # Crop the screenshot to remove the whitespace below the blue line
        crop_screenshot(screenshot_path)

        # Print a message to indicate progress
        print(f"Saved screenshot of {url} to {screenshot_path}")

    # Close the browser
    browser.quit()

def crop_screenshot(img_path, strip_width=20):
    # Load the screenshot image
    screenshot = Image.open(img_path)

    # Calculate the horizontal limits for the evaluation strip
    strip_start = screenshot.width // 2 - strip_width // 2
    strip_end = strip_start + strip_width

    # Define the initial background color at the very bottom of the evaluation strip
    initial_color = screenshot.getpixel((strip_start, screenshot.height - 1))

    # Initialize the bottom_pos variable
    bottom_pos = screenshot.height

    # Loop through the rows of the screenshot from bottom to top within the evaluation strip
    for y in range(screenshot.height - 1, 0, -1):
        row_colors = [screenshot.getpixel((x, y)) for x in range(strip_start, strip_end)]
        different_colors = sum(color != initial_color for color in row_colors)

        # Check if any color in the row is different from the initial background color
        if different_colors > 0:
            # The loop has reached the bottom of the page theme
            bottom_pos = y
            break

    # Crop the image above the bottom position
    cropped_screenshot = screenshot.crop((0, 0, screenshot.width, bottom_pos))

    # Save the cropped image
    cropped_screenshot.save(img_path)
    
def get_sitemap_urls(base_url):
    sitemap_url = urljoin(base_url, "/sitemaps")
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "html.parser")

    lst_pages = soup.find("div", id="lstPages")
    if lst_pages:
        urls = []
        for a in lst_pages.find_all("a", href=True):
            is_valid, absolute_url = process_url(a["href"], base_url)
            if is_valid:
                urls.append(absolute_url)
        return urls
    else:
        return []

def create_output_directory(base_dir, site_folder):
    full_dir = os.path.join(base_dir, site_folder)
    os.makedirs(full_dir, exist_ok=True)
    return full_dir

def unique_urls(urls_list):
    seen = set()
    unique_urls_list = []

    for url in urls_list:
        if url not in seen:
            unique_urls_list.append(url)
            seen.add(url)
    
    return unique_urls_list

def process_url(url, base_url):
    url = url.replace("http://", "https://")

    if not url.startswith("http"):
        if not url.startswith(base_url):
            url = urljoin(base_url, url)
    else:
        # Exclude off-site URLs
        if not url.startswith(base_url):
            return False, None

    if "javascript:" in url:
        return False, None
    if "tel:" in url:
        return False, None
    if url.endswith((".js", ".css")):
        return False, None
    return True, url

sites_list = ["https://www.barnesjewish.org"]

root_output_folder = "screenshots/"
project_path = os.path.dirname(os.path.abspath(__file__))


for site in sites_list:
    site_sitemap_urls = get_sitemap_urls(site)
    unique_site_sitemap_urls = unique_urls(site_sitemap_urls)
    take_screenshots(unique_site_sitemap_urls, root_output_folder, project_path)
