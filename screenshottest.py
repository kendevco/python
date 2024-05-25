from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Set up the ChromeDriver service
service = Service(executable_path='C:\ProgramData\chromedriver\chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True 
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.set_page_load_timeout(5)


# Navigate to the URL
url = 'https://folio.kendev.co'
browser.get(url)

# Get the page title and remove any invalid characters
title = browser.title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

# Get the file extension (if any)
file_extension = os.path.splitext(title)[1]

# Save the screenshot as a PNG file
if file_extension:
    filename = title.replace(file_extension, '') + '.png'
else:
    filename = title + '.png'
    
browser.save_screenshot(filename)

# Quit the driver
browser.quit()