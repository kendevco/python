import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://slchlabtestguide.bjc.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract various elements to build the CSP string
scripts = soup.find_all('script', src=True)
styles = soup.find_all('link', rel='stylesheet')

# Get a set of unique script and style source domains
script_domains = {urlparse(tag['src']).netloc for tag in scripts if tag['src']}
style_domains = {urlparse(tag['href']).netloc for tag in styles if tag['href']}

# Build the CSP string
csp_string = "default-src 'self'; script-src 'self' {}; style-src 'self' {};".format(
    ' '.join(script_domains),
    ' '.join(style_domains)
)

print(csp_string)