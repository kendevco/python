import os
import time
import requests
import logging
from PIL import Image
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER as SELENIUM_LOGGER
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse

sites_list = [
    "https://www.bjcmedicalgroup.org"
    #"https://legacy.bjc.org",
    #"https://www.bjc.org"
    # "https://www.missouribaptist.org", 
    # "https://www.barnesjewishwestcounty.org", 
    # "https://www.bjsph.org", 
    # "https://www.bjcstcharlescounty.org",
    # "https://www.altonmemorialhospital.org",
    # "https://www.bjchomecare.org",
    # "https://www.bjcbehavioralhealth.org",
    ""
    ]

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

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

def does_screenshot_exist(url, base_folder, project_path):
   
    parsed_url = urlparse(url)

    # Determine the filename based on the URL path
    if parsed_url.path.strip() == '' or parsed_url.path.strip() == '/':
        filename = 'default.png'
    else:
        # Join folder and file names with underscores
        filename = '_'.join(parsed_url.path.strip('/').split('/')) + '.png'

    target_folder = os.path.join(project_path, base_folder, parsed_url.hostname)
    target_file = os.path.join(target_folder, filename)

    screenshot_exists = os.path.exists(target_file)
    logging.debug(f"Screenshot for {url} exists: {screenshot_exists}")

    return screenshot_exists

def take_single_screenshot(url, root_folder, project_path):
    logging.debug(f"Taking screenshot of {url}")
 
    # Set up the ChromeDriver service
    service = Service(executable_path='C:\ProgramData\chromedriver\chromedriver.exe')

    # Create a new Chrome browser instance with desired options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    
        # Set the desired capabilities to suppress console errors
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'SEVERE'}
    
     # Update the Selenium and Chrome log levels to suppress unnecessary logs
    SELENIUM_LOGGER.setLevel(logging.WARNING)   
    
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.set_page_load_timeout(60)

    def page_is_visually_loaded(driver):
        # Check document is ready
        is_ready = driver.execute_script("return document.readyState") == 'complete'
        if not is_ready:
            return False

        # Check if all images are loaded
        images_loaded = driver.execute_script("return Array.from(document.images).every(img => img.complete);")
        if not images_loaded:
            return False

        return True

    # Wait for the page to load
    #WebDriverWait(browser, 30).until(lambda d: d.execute_script("return document.readyState") == 'complete')
    # WebDriverWait(browser, 30).until(lambda d: d.execute_script("return Array.from(document.images).every(img => img.complete);"))

    try:
        # Navigate to the URL
        browser.get(url)      
          
        # Wait for the page to load
        WebDriverWait(browser, 60).until(lambda d: d.execute_script("return Array.from(document.images).every(img => img.complete);"))
        #WebDriverWait(browser, 45).until(page_is_visually_loaded)
        
    except TimeoutException:
        logging.warning(f"Timeout waiting for images to load on {url}. Skipping screenshot.")
        browser.quit()
        return False
    except Exception as e:
        logging.warning(f"Error occurred while loading {url}: {str(e)}. Skipping screenshot.")
        browser.quit()
        return False
    
    # Save the screenshot with the desired name
    screenshot_path = create_screenshot_path(url, root_folder, project_path)
    desired_width, desired_height = 1280, 720
    S = lambda X: browser.execute_script('return document.body.parentNode.scroll' + X)
    browser.set_window_size(desired_width, max(S('Height'), desired_height))
    ActionChains(browser).send_keys(Keys.HOME).perform()
    prefs = {"profile.managed_default_content_settings.images": -1}
    chrome_options.add_experimental_option("prefs", prefs)
    browser.save_screenshot(screenshot_path)

    logging.debug(f"Screenshot saved for {url} at {screenshot_path}")
    # Close the browser
    browser.quit()

    # Crop the screenshot to remove the whitespace below the blue line
    crop_screenshot(screenshot_path)
    # Print a message to indicate progress
    logging.debug(f"Cropped screenshot saved for {url}")

num_workers = max(1, os.cpu_count() - 1)  # Use one less than the number of available CPUs

def take_screenshots(url_list, root_folder, project_path, workers=num_workers):
    logging.debug(f"Starting take_screenshots function with {len(url_list)} URLs")

    # Filter the URLs that need screenshots
    urls_to_screenshot = [url for url in url_list if not does_screenshot_exist(url, root_folder, project_path)]

    logging.debug(f"Found {len(urls_to_screenshot)} URLs that need screenshots")

    # Use ThreadPoolExecutor to run multiple instances simultaneously
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(take_single_screenshot, url, root_folder, project_path) for url in urls_to_screenshot]
        for future in futures:
            logging.debug("Waiting for a thread to complete")
            future.result()
            logging.debug("Thread completed")

    logging.debug("All threads completed")  # Wait for the threads to complete

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
    sitemap_url = urljoin(base_url, "/Sitemap.aspx")
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")

    url_elements = soup.find_all("url")
    urls = [url_element.find("loc").text for url_element in url_elements if url_element.find("loc")]
        
    return urls

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


root_output_folder = "screenshots/"
project_path = os.path.dirname(os.path.abspath(__file__))

for site in sites_list:
    site_sitemap_urls = get_sitemap_urls(site)
    unique_site_sitemap_urls = unique_urls(site_sitemap_urls)
    
    # Replace 'www.bjc.org' with 'legacy.bjc.org' in 'unique_site_sitemap_urls'
    unique_site_sitemap_urls = [url.replace('www.bjc.org', 'legacy.bjc.org') for url in unique_site_sitemap_urls]

    
    take_screenshots(unique_site_sitemap_urls, root_output_folder, project_path)
