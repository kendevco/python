import requests
from requests.exceptions import HTTPError

from bs4 import BeautifulSoup
import csv
import http.client
from urllib.parse import urlparse
from lxml import etree

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
            sitemap_url = line.split("Sitemap: ")[1].strip()
            # Download the sitemap XML file
            try:
                response = requests.get(sitemap_url)
                response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}') 
            except Exception as err:
                print(f'Other error occurred: {err}') 
            else:
                return response.text

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
    for url in sitemap_xml.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(url.text)
    return urls

def parse_sitemap_xml_file(sitemap_xml_file):
    # Parse the sitemap XML file
    try:
        sitemap_xml = etree.fromstring(sitemap_xml_file.encode('utf-8'))
        return sitemap_xml
    except Exception as e:
        print(e)
        return None


from urllib.parse import urljoin

def scrape(url, collected_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')

    # Open the CSV file for writing
    with open('fbjlinks.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        # Iterate over each link
        for link in links:
            href = link.get('href')
            text = link.string

            # If the href attribute exists and is not a "tel:" or "javascript:" link
            if href is not None and not href.startswith(("tel:", "javascript:")):
                # Resolve relative links
                href = urljoin(url, href)
                
                # Check if the link is in the collected links set
                if href not in collected_links:
                    # Add the link to the collected links set
                    collected_links.add(href)

                    # Print the URL and link text to the terminal
                    print(f'URL: {href}, Link Text: {text}')

                    # Write the URL, link text, and page URL to the CSV file
                    writer.writerow([href, text, url])


# The URL to be scraped
url = 'https://www.foundationbarnesjewish.org'

sitemap_file = get_sitemap_xml_file(url)


if sitemap_file is not None:
    urls = get_urls_from_sitemap_xml_file(sitemap_file)

    # Create the collected links set
    collected_links = set()

   # Open the CSV file for writing
    with open('fbjlinks.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Link Text', 'Page URL'])

    for url in urls:
        scrape(url, collected_links)