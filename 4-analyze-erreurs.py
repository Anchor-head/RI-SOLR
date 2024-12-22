import os
from lxml import etree
import re

# Path to your folder with XML files
folder_path = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\collectionID"
# Dictionary to count errors
error_count = {}
# Validate XML files

def count_doc_tags(file_path):
    try:
        # Open and read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Count the occurrences of <doc> tags
            doc_count = content.lower().count('<doc>')
            return doc_count
    except Exception as e:
        print(f"Error reading {os.path.basename(file_path)}: {e}")
        return 0
    
def validate_xml(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            etree.parse(file)  # Parse the XML file
    except etree.XMLSyntaxError as e:
        error_message = str(re.findall(r"'(.*?)'", str(e)))
        if len(error_message)>2:
            error_message=error_message[2:-2]
        doc_count=count_doc_tags(file_path)
        # Count the error type
        if error_message not in error_count:
            error_count[error_message] = doc_count
        else:
            error_count[error_message] += doc_count

# Iterate through all XML files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xml'):  # Only process XML files
        file_path = os.path.join(folder_path, file_name)
        validate_xml(file_path)

# Write the summary of errors to a file
print(error_count)