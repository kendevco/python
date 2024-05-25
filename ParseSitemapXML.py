import csv
from xml.etree import ElementTree

def main():
    xml_file_path = "C:/Data/Dev/Python/Input/rentmyequipment.com_equipment-sitemap.xml"
    tree = ElementTree.parse(xml_file_path)
    root = tree.getroot()

    # Update the namespace to match the XML file
    namespaces = {'ns': 'https://www.sitemaps.org/schemas/sitemap/0.9'} 

    with open("rentmyequipment_links_table.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Location', 'Lastmod']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in root.findall('ns:url', namespaces):
            location = url.find('ns:loc', namespaces).text
            lastmod = url.find('ns:lastmod', namespaces).text if url.find('ns:lastmod', namespaces) is not None else ''
            writer.writerow({fieldnames[0]: location, fieldnames[1]: lastmod})

    print("CSV file generated: rentmyequipment_links_table.csv")

if __name__ == '__main__':
    main()
