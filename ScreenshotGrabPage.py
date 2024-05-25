import http.client
from urllib.parse import urlparse

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

# Usage
site = "https://kendev.co"
print(get_robots_txt_file(site))