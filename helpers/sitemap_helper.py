import os
import requests
import logging
import http.client
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

def get_all_urls(base_url, max_workers=None):
    sitemap_urls = get_sitemap_urls(base_url)
    crawled_urls = crawl_website_multithreaded(base_url, max_workers=max_workers)

    all_urls = sitemap_urls + list(crawled_urls)
    unique_urls = set(all_urls)

    return list(unique_urls)

def process_url_queue(q, visited_urls, site_domain):
    while not q.empty():
        url = q.get()

        # Check if the URL domain matches the provided site domain
        url_domain = urlparse(url).hostname
        if url_domain != site_domain:
            q.task_done()
            continue

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get content at {url}: {e}")
            q.task_done()
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a", href=True):
            href = link['href']
            absolute_url = urljoin(url, href)

            if absolute_url not in visited_urls:
                visited_urls.add(absolute_url)
                q.put(absolute_url)

        q.task_done()

def crawl_website_multithreaded(start_url, max_workers=None):
    if max_workers is None:
        max_workers = os.cpu_count() * 2

    site_domain = urlparse(start_url).hostname
    visited_urls = set()
    q = Queue()
    q.put(start_url)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        threads = []
        for _ in range(max_workers):
            threads.append(executor.submit(process_url_queue, q, visited_urls, site_domain))

        # Wait for all the threads to complete
        for future in as_completed(threads):
            future.result()

    return visited_urls

def get_sitemap_urls(base_url):
    # Get the sitemap XML file URLs from the robots.txt file
    sitemap_xml_urls = get_sitemap_xml_files(base_url)

    if not sitemap_xml_urls:
        sitemap_xml_urls = [urljoin(base_url, "/sitemap.xml")]
    
    all_urls = []

    for sitemap_url in sitemap_xml_urls:
        try:
            sitemap_xml_content = requests.get(sitemap_url).content
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get sitemap XML file at {sitemap_url}: {e}")
            continue

        # Get the URLs from the sitemap XML file
        sitemap_urls = get_urls_from_sitemap_xml_file(sitemap_xml_content)
        all_urls.extend(sitemap_urls)

    return all_urls

def get_sitemap_xml_files(site):
    # Get the robots.txt file
    robots_txt_file = get_robots_txt_file(site)
    if robots_txt_file is None:
        return []

    # Split the content by newline to get an iterable list of lines
    lines = robots_txt_file.split('\n')

    sitemap_urls = []

    # Search for the sitemap XML file(s) in the robots.txt file
    for line in lines:
        if line.startswith("Sitemap: "):
            sitemap_url = line.split("Sitemap: ")[1].strip()
            sitemap_urls.append(sitemap_url)

    return sitemap_urls

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
    for loc in sitemap_xml.xpath("//ns:loc", namespaces={'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}):
        urls.append(loc.text)
    return urls

def parse_sitemap_xml_file(sitemap_xml_file):
    # Create an XML parser
    parser = etree.XMLParser(remove_blank_text=True)

    # Parse the sitemap XML file
    try:
        sitemap_xml = etree.fromstring(sitemap_xml_file, parser=parser)
        return sitemap_xml
    except Exception as e:
        logging.error(f"Failed to parse sitemap XML file: {e}")
        return None

def unique_urls(urls_list):
    seen = set()
    unique_urls_list = []

    for url in urls_list:
        if url not in seen:
            unique_urls_list.append(url)
            seen.add(url)

    return unique_urls_list