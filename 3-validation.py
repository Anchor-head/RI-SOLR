import os
from lxml import etree

# Path to your folder with XML files
folder_path = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel2"
# Path to the errors output file
errors_file_path = r"C:\Documents\UQAM\INF7546\Projet1\prepretraitement\errors.txt"

# Validate XML files
with open(errors_file_path, 'w',encoding='utf-8') as error_file:
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            try:
                etree.parse(file)  # Parse the XML file
                print(f"{os.path.basename(file_path)}: Valid")
            except etree.XMLSyntaxError as e:
                print(e)
                error_file.write(f'{str(e)}\n')

print(f"Error summary written to: {errors_file_path}")
