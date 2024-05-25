import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url, urls=set()):
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    try:
        print(f"Processing: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                # not a valid URL
                continue
            if href in urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                continue
            urls.add(href)
            # call the function recursively
            get_all_website_links(href, urls)
        time.sleep(1)
    except (requests.exceptions.TooManyRedirects, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(f"Error occurred while processing {url}: {str(e)}")

    return urls

#Usage
urls = get_all_website_links('https://prod-bjc-org-webapp.bjc.org/specialties/neurosciences')
for url in urls:
    print(url)