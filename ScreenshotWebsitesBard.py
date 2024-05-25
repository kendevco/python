import os
import sys
import time
import requests
import http.client

from urllib.parse import urlparse
from selenium import webdriver
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def main():
    # Get the list of websites to screenshot
    sites_list = [
        "https://kendev.co",
        "https://www.missouribaptist.org", 
        "https://www.barnesjewishwestcounty.org", 
        "https://www.bjsph.org", 
        "https://www.bjcstcharlescounty.org"
    ]

    # Get the number of processors on the system
    num_processors = os.cpu_count() - 1

    # Create the directory for the screenshots
    project_directory = os.path.dirname(os.path.realpath(__file__))
    screenshots_directory = os.path.join(project_directory, "screenshots")
    if not os.path.exists(screenshots_directory):
        os.makedirs(screenshots_directory)

    # Iterate through the list of websites
    with ThreadPoolExecutor(max_workers=num_processors) as executor:
        for site in sites_list:
            # Get the sitemap XML file
            sitemap_xml_file = get_sitemap_xml_file(site)
            if sitemap_xml_file is None:
                continue

            # Iterate through the sitemap XML file
            for url in get_urls_from_sitemap_xml_file(sitemap_xml_file):
                # Create a screenshot of the website
                screenshot_path = os.path.join(screenshots_directory, site + "_" + url.split("/")[-1] + ".png")
                if os.path.exists(screenshot_path):
                    continue

                executor.submit(screenshot, url)

    # Trim the screenshot
    def screenshot(url):
        # Create a screenshot of the website
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1)
        screenshot = driver.save_screenshot(screenshot_path)
        driver.quit()

        # Trim the screenshot
        image = Image.open(screenshot)
        bottom_center_pixel = image.getpixel((image.width // 2, image.height - 1))
        while bottom_center_pixel == image.getpixel((image.width // 2, image.height - 2)):
            image.crop((0, 0, image.width, image.height - 1))
        image.save(screenshot)

    # Ensure that all images have been loaded on the page prior to closing driver
    def ensure_images_loaded(driver):
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            while True:
                try:
                    driver.find_element_by_xpath("//img")
                except StaleElementReferenceException:
                    break

    # Iterate through the list of websites
    for site in sites_list:
        # Get the sitemap XML file
        sitemap_xml_file = get_sitemap_xml_file(site)
        if sitemap_xml_file is None:
            continue

        # Iterate through the sitemap XML file
        for url in get_urls_from_sitemap_xml_file(sitemap_xml_file):
            # Create a screenshot of the website
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(1)
            screenshot = driver.save_screenshot(screenshot_path)
            driver.quit()

            # Ensure that all images have been loaded on the page prior to closing driver
            ensure_images_loaded(driver)
            
def get_sitemap_xml_file(site):
    # Get the robots.txt file
    robots_txt_file = get_robots_txt_file(site)
    if robots_txt_file is None:
        return None

    # Split the content by newline to get an iterable list of lines
    lines = robots_txt_file.split('\n')

    # Search for the sitemap XML file in the robots.txt file
    for line in lines:
        if line.startswith("Sitemap: "):
            return line.split("Sitemap: ")[1].strip()

    return None

def get_robots_txt_file(site_url):
    parsed_site_url = urlparse(site_url)
    site_domain = parsed_site_url.hostname
    scheme = parsed_site_url.scheme

    if scheme == 'https':
        connection = http.client.HTTPSConnection(site_domain)
    else:
        connection = http.client.HTTPConnection(site_domain)

    connection.request("GET", "/robots.txt")
    response = connection.getresponse()

    # Check for 301 status code (redirect) and follow the new URL
    if response.status == 301:
        location = response.getheader('Location')
        return get_robots_txt_file(location)

    if response.status != 200:
        return None

    robots_txt_file = response.read().decode('utf-8')

    return robots_txt_file

def get_urls_from_sitemap_xml_file(sitemap_xml_file):
    # Parse the sitemap XML file
    sitemap_xml = parse_sitemap_xml_file(sitemap_xml_file)
    if sitemap_xml is None:
        return []

    # Get the URLs from the sitemap XML file
    urls = []
    for loc in sitemap_xml.loc:
        urls.append(loc.loc)
    return urls

def parse_sitemap_xml_file(sitemap_xml_file):
    # Create an XML parser
    parser = etree.XMLParser(remove_blank_text=True)

    # Parse the sitemap XML file
    try:
        sitemap_xml = etree.parse(sitemap_xml_file, parser=parser)
        return sitemap_xml
    except Exception as e:
        print(e)
        return None
if __name__ == "__main__":
    main()
