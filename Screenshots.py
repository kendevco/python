from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

def take_screenshots(url_list, output_dir):
    # Set up the ChromeDriver service
    service = Service(executable_path='C:\ProgramData\chromedriver\chromedriver.exe')

    # Create a new Chrome browser instance with desired options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # Loop through the list of URLs and take screenshots
    for i, url in enumerate(url_list):
        # Navigate to the URL
        browser.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Save the screenshot with the desired name
        url_name = url.replace("https://www.bjcmedicalgroup.org/Find-a-Location/", "").strip("/")
        screenshot_path = f"{output_dir}/{url_name}.png"

        desired_width, desired_height = 1280, 720
        S = lambda X: browser.execute_script('return document.body.parentNode.scroll'+X)
        browser.set_window_size(desired_width, max(S('Height'), desired_height))
        ActionChains(browser).send_keys(Keys.HOME).perform()
        browser.save_screenshot(screenshot_path)

        # Print a message to indicate progress
        print(f"Saved screenshot of {url} to {screenshot_path}")

    # Close the browser
    browser.quit()

def load_urls_from_file(filepath):
    with open(filepath, 'r') as file:
        return [url.strip() for url in file.readlines()]

def create_output_directory(base_dir):
    i = 1
    while os.path.exists(f"{base_dir}/{i}"):
        i += 1
    os.makedirs(f"{base_dir}/{i}")
    return f"{base_dir}/{i}"

# Load URLs from medgrouplinks.txt
url_list = load_urls_from_file('medgrouplinks.txt')

# Create a new folder in the screenshots directory and increment its name
output_dir = create_output_directory("screenshots")

# Call the function to take screenshots
take_screenshots(url_list, output_dir)