import os
import re

folder_path = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel1"
output_folder = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel2"

def convert_to_solr_format(input_file, output_file):
    try:
        with open(input_file, 'r', encoding="utf-8") as file:
            content = file.read()
            content = content.lower()
            content = content.replace('<doc>', 'DOC').replace('</doc>', '/DOC')
            content = re.sub("</[a-z]+?>","/field",content)
            content = re.sub('<', '<field name="',content)
            content = re.sub('>', '">',content)
            content=content.replace('/DOC','</doc>').replace('DOC','<doc>').replace('/field','</field>').replace('docno','id')
            content = "<add>\n"+content+"</add>"

        with open(output_file, 'w',encoding='utf-8') as file:
            file.write(content)

    except Exception as e:
        print(f"Error processing {input_file}: {e}")

for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        input_file = os.path.join(folder_path, filename)
        
        # Output file path (same name but in the output folder)
        output_file = os.path.join(output_folder, filename)

        # Convert the file to Solr-friendly format
        convert_to_solr_format(input_file, output_file)
