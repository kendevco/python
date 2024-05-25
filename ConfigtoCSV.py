import xml.etree.ElementTree as ET
import csv

# Define the path to the XML file
xml_file_path = './Input/rewritemaps.config'

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Define the path to the CSV file
csv_file_path = './Output/rewritemaps.csv'

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='') as csvfile:
    # Define the CSV writer
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["key", "value"])

    # Iterate over each 'add' element in the XML file
    for add_element in root.iter('add'):
        # Extract the 'key' and 'value' attributes
        key = add_element.get('key')
        value = add_element.get('value')

        # Write the row to the CSV file
        writer.writerow([key, value])

print('CSV file has been created.')
