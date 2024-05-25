import requests
from bs4 import BeautifulSoup
import csv

def main():
    url = 'https://www.bjcmedicalgroup.org/sitemaps'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    with open("bjcmedicalgroup_links_table.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Link Text', 'Link Href']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for link in links:
            link_text = link.text.strip()
            link_href = link.get('href', '')
            writer.writerow({fieldnames[0]: link_text, fieldnames[1]: link_href})

    print("CSV file generated: links_table.csv")

if __name__ == '__main__':
    main()