import os
from lxml import etree

folder_path = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel2"
errors_file_path = r"C:\Documents\UQAM\INF7546\Projet1\prepretraitement\errors.txt"

with open(errors_file_path, 'w',encoding='utf-8') as error_file:
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            try:
                etree.parse(file)
                print(f"{os.path.basename(file_path)}: Valid")
            except etree.XMLSyntaxError as e:
                print(e)
                error_file.write(f'{str(e)}\n')

print(f"Les erreurs ont été écrites ici: {errors_file_path}")
