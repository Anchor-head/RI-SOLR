import os
from lxml import etree

folder_path = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel2"
error_code = {'lsqb':'[',
              'rsqb':']',
              'equals':'=',
              'plus':'+'}

def unbug_xml(file_path):
    with open(file_path, 'r',encoding='utf-8') as my_file:
        bad_file_content=my_file.read()
        try:
            etree.parse(file_path)
        except etree.XMLSyntaxError as e:
            print(e)
            with open(file_path, 'w',encoding='utf-8') as file:

                #block pour les erreurs "no-name"
                good_file_content=bad_file_content.replace('&\n', '&amp;\n').replace('& ', '&amp; ')

                #block pour les autres erreurs
                for error in error_code:
                    good_file_content = good_file_content.replace(f'&{error};', error_code[error])
                file.write(good_file_content)

for file_name in os.listdir(folder_path):
    if file_name.endswith('.xml'):
        print(file_name)
        file_path = os.path.join(folder_path, file_name)
        unbug_xml(file_path)
