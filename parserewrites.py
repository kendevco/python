import xml.etree.ElementTree as ET
import csv

def parse_file(file_name):
    # parse the xml file
    tree = ET.parse(file_name)

    # create empty list to hold the data
    data = []

    for rewrite_map in tree.findall('rewriteMap'):
        name = rewrite_map.get('name')

        for item in rewrite_map.findall('add'):
            key = item.get('key')
            value = item.get('value')
            data.append({'Name': name, 'Key': key, 'Value': value})

    return data


def main():
    file_name = './Input/urls.config'  # specify your file path
    data = parse_file(file_name)

    # specify the file to be written
    output_file_name = './Output/bjcrewrites.csv'
    # create the csv writer object
    with open(output_file_name, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Key', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write the header
        writer.writeheader()

        # writing the data rows
        for item in data:
            writer.writerow(item)


if __name__ == "__main__":
    main()