import xml.etree.ElementTree as ET

# Update the path below with the path to your XML file
xml_file_path = r'.\input\app.xml'
output_file_path = r'.\output\2sxcArticlesSchema.xsd'

# Load and parse the XML file
try:
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
except ET.ParseError as e:
    print(f"Error parsing XML file: {e}")
    exit(1)

# Sort the File nodes by Id attribute
file_nodes = root.findall(".//PortalFiles/File")
file_nodes.sort(key=lambda node: node.get("Id"))

# Sort the Folder nodes by Id attribute
folder_nodes = root.findall(".//PortalFolders/Folder")
folder_nodes.sort(key=lambda node: node.get("Id"))

# Find duplicate File Id nodes
duplicate_file_ids = set()
for file_node in file_nodes:
    file_id = file_node.get("Id")
    if file_id in duplicate_file_ids:
        print(f"Found duplicate File Id: {file_id}")
    else:
        duplicate_file_ids.add(file_id)

# Find duplicate Folder Id nodes
duplicate_folder_ids = set()
for folder_node in folder_nodes:
    folder_id = folder_node.get("Id")
    if folder_id in duplicate_folder_ids:
        print(f"Found duplicate Folder Id: {folder_id}")
    else:
        duplicate_folder_ids.add(folder_id)

# Write the XML schema to the output file with UTF-8 encoding
try:
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(ET.tostring(root, encoding='unicode'))
    print(f"XML schema written to {output_file_path}")
except IOError as e:
    print(f"Error writing XML schema to file: {e}")