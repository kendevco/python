import csv
import requests
from bs4 import BeautifulSoup
import socket
import ssl
import re

domain_names = [
 "owmb.org",
 "bjcgovernmentrelations.com",
 "bjcimaging.org",
 "ourworldmadebetter.com",
 "bjchealthcare.com",
 "bjchealthsolutions.net",
 "bjccommunityhealth.net",
 "bjchealthcare.jobs",
 "yourcareermadebetter.jobs",
 "ourworldmadebetter.org",
 "bjcnorthcounty.org",
 "bjcaco.org",
 "bjccommunityhealthservices.org",
 "bjctodayonline.com",
 "bjc.healthcare",
 "bjcconciergecare.org",
 "bjcgovernmentrelations.org",
 "bjcimaging.com",
 "bjcaco.com",
 "bjcgovernmentrelations.net",
 "bjcjobs.org",
 "bjccenterofexcellence.org",
 "bjcradiology.com",
 "bjcjobs.com",
 "bjcaco.net",
 "bjc.jobs",
 "choosebettermedicine.org",
 "bjcnorthcounty.com",
 "progresswestbaby.org",
 "bjccommunityhealthliteracy.com",
 "bjhne.ws",
 "bjcortho.org",
 "choosebettermedicine.net",
 "bjchealthsolutions.org",
 "bjccommunityhealthliteracy.org",
 "bjctodayonline.org",
 "progresswestbaby.com",
 "bjccollaborative.net",
 "makemedicinebetter.com",
 "bjcbooks.org",
 "bjccollaborative.com",
 "bjcimaging.net",
 "bjcstcharlescountyknee.net",
 "bjcradiology.net",
 "bjccommunityhealth.com",
 "bjcschooloutreach.com",
 "bjccommunityhealth.org",
 "makemedicinebetter.net",
 "bjcbooks.net",
 "bjctodayonline.net",
 "bjchealthsolutions.com",
 "progresswestbaby.net",
 "bjcconciergecare.net",
 "bjcstcharlescountyknee.com",
 "bjcorthopedics.net",
 "bjcstcharlescountyknee.org",
 "bjccommunityhealthservices.com",
 "bjcconciergecare.com",
 "bjcortho.net",
 "bjchealthcare.net",
 "bjcschooloutreach.org",
 "bjccommunityhealthliteracy.net",
 "bjchealthcare.org",
 "bjcradiology.org",
 "bjctoday.online",
 "bjcmedicalgroup.net",
 "bjcmedicalgroup.com"
]

def get_website_title(domain):
    url = domain if domain.startswith('http') else 'https://' + domain
    try:
        # Attempt to get the title using requests and BeautifulSoup
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip(), response.url  # Also return the final URL
    except Exception as e:
        print(f"Failed to get title from {url} using requests/BeautifulSoup. Error: {e}")

    try:
        # If BeautifulSoup fails, try to get the title using socket and ssl
        context = ssl.create_default_context()
        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                ssock.sendall(b"GET / HTTP/1.1\r\nHost: "+bytes(url, 'utf-8')+b"\r\nConnection: close\r\n\r\n")
                data = ssock.recv(4096)
        title = re.search(b'<title>(.*?)</title>', data, re.I)
        if title:
            return title.group(1).decode('utf-8'), url
    except Exception as e:
        print(f"Failed to get title from {url} using socket/ssl. Error: {e}")
        
    return "No title found", url

with open('domain_titles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Original Domain", "Title", "Final URL"])  # Writing headers

    for domain in domain_names:
        title, final_url = get_website_title(domain)
        print(f'The title of {domain} is "{title}" and it redirects to "{final_url}"')
        writer.writerow([domain, title, final_url])  # Writing data