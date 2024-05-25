import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def is_valid_url(url):
    # You can add/check for the conditions which can validate if the url is valid or not
    return True

def get_all_website_links(url, urls=set()):
    urls_to_process = [url]
    
    while urls_to_process:
        current_url = urls_to_process.pop(0)
        domain_name = urlparse(current_url).netloc

        try:
            print(f"Processing: {current_url}")
            response = requests.get(current_url, timeout=5)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            for a_tag in soup.findAll("a"):
                href = a_tag.attrs.get("href")
                if href == "" or href is None:
                    continue
                href = urljoin(current_url, href)
                parsed_href = urlparse(href)
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid_url(href):
                    continue
                if href in urls:
                    continue
                if domain_name not in href:
                    continue
                urls.add(href)
                urls_to_process.append(href)
                print(f"URLs found so far: {len(urls)}")  # Prints the number of URLs found thus far

            time.sleep(1)
        except (requests.exceptions.TooManyRedirects, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            print(f"Error occurred while processing {current_url}: {str(e)}")

        save_links_to_txt(current_url, urls)

    return urls

def save_links_to_txt(base_url, urls):
    # Normalize file name
    parsed_base_url = urlparse(base_url)
    netloc_normalized = parsed_base_url.netloc.replace(".", "_")
    filename = netloc_normalized + '.txt'
    with open(filename, mode='w', newline='') as file:
        for url in urls:
            file.write(f"{url}\n")

# List of domain names/urls
url_list = [
    "https://www.barnesjewishwestcounty.org", 
    "https://www.memhosp.org",
    "https://www.altonmemorialhospital.org",
    "https://www.bjsph.org",
    "https://www.progresswest.org",
    "https://www.parklandhealthcenter.org",
    "https://www.missouribaptistsullivan.org",
    "https://www.bjcstcharlescounty.org",
    "https://www.memorialbreasthealthcenter.org",
    "https://www.memorialbirthingcenter.org",
    "https://www.memorialheartvascular.org",
    "https://www.ortho-neurocenter.org",
]  # Updated URL list

# Process all URLs
for url in url_list:
    get_all_website_links(url)