import requests
import re
from bs4 import BeautifulSoup, UnicodeDammit
from urllib.parse import urlparse, urljoin

tracking_scripts = [
    "AddThis", "Alida", "Bing", "cpx\.to", "dialogtech", "DoubleClick", "cloudfront.net",
    "Eloqua", "Google Analytics", "HotJar", "Invoca", "Krux", "krxd\.net", "Lucky Orange", 
    "Meta Pixel", "Microsoft Clarity", "narrative\.io", "Pippio", "rezync", "rfihub", 
    "ShareThis", "The Trade Desk", "Adsrvr", "Yahoo"
]

pattern = re.compile("|".join(tracking_scripts), re.IGNORECASE)

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def spider_website(url, visited, output_file):
    response = requests.get(url)
    detected_encoding = UnicodeDammit(response.content).original_encoding
    soup = BeautifulSoup(response.content, "html.parser", from_encoding=detected_encoding)

    visited.add(url)
    for idx, script in enumerate(soup.find_all("script")):
        script_content = script.string if script.string else ''
        script_src = script.get("src", '')

        if script_src:
            print(f"Examining external script SRC: {urljoin(url, script_src)}")
        else:
            print(f"Examining inline script at {url} (line {idx + 1})")

        # Exclude scripts with ActionForm, DotNetNuke, EasyDNN, Telerik
        exclude_patterns = ["ActionForm", "DotNetNuke", "EasyDNN", "Telerik"]
        if any(patt in script_content or patt in script_src for patt in exclude_patterns):
            continue


        # Exclude scripts with source from the root directory
        if script_src.startswith('/') and not script_src.startswith('//'):
            continue

        if (pattern.search(script_content) or pattern.search(script_src)):
            result = (
                f'URL: {url}\n'
                f'Line Number: {idx + 1}\n'
                f'Script Snippet: {script_content.strip()}\n'
                f'Script Source: {script_src}\n'
                f'{"-----" * 10}\n'
            )
            print(result)
            output_file.write(result)

        # Traverse new local URLs
    for link in soup.find_all('a'):
        href = link.get("href")
        joined_url = urljoin(url, href)
        if not is_valid(joined_url):
            continue

        if joined_url not in visited and urlparse(joined_url).netloc == urlparse(url).netloc:
            spider_website(joined_url, visited, output_file)

websites = [
    "AltonMemorialHospital.org",
    "BarnesCare.com",
    "BarnesJewish.org",
    "BarnesJewishCollege.edu",
    "BarnesJewishWestCounty.org",
    "BJC.org",
    "BJCBehavioralHealth.org",
    "BJCEAP.com",
    "BJCHomeCare.org",
    "BJCHospice.org",
    "BJCMedicalGroup.org",
    "BJCSchoolOutreach.org",
    "BJCStCharlesCounty.org",
    "BJCTotalRewards.org",
    "BJSPH.org",
    "ChristianHospital.org",
    "CommunityBenefit.bjc.org",
    "covid19.bjc.org",
    "Epic1.org",
    "FoundationBarnesJewish.org",
    "MissouriBaptist.org",
    "MissouriBaptistSullivan.org",
    "MOBapBaby.org",
    "MoveByBJC.org",
    "PositioningForTheFuture.bjc.org",
    "ParklandHealthCenter.org",
    "ProgressWest.org",
    "BJCMedia-Services.carenet.org"
]
def main():
    with open('output.txt', 'w') as output_file:
        visited = set()
        for site in websites:
            print(f'Spidering website: {site}')
            output_file.write(f'Spidering website: {site}\n')

            try:
                url = "http://" + site
                print(f"Processing page: {url}")  # Console log for each page being processed
                spider_website(url, visited, output_file)

            except requests.exceptions.RequestException as e:
                error_msg = f"Error: {e}\n"
                print(error_msg)
                output_file.write(error_msg)

if __name__ == "__main__":
    main()