import os
import shutil

source_folder = r"C:\Documents\UQAM\INF7546\Projet1\TREC-AP-88-90\collection de documents\AP_unzipped"
destination_folder = r"C:\Documents\UQAM\INF7546\Projet1\solr-9.7.0\officiel1"

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    new_file_path = os.path.join(destination_folder, filename)

    # Read file to check if it's XML
    with open(file_path, 'r') as file:
        myfile = file.read().strip()
        if myfile.startswith("<") and myfile.endswith(">"):
            new_file = os.path.splitext(new_file_path)[0] + '.xml'
            try:
                shutil.move(file_path, new_file)
            except PermissionError as e:
                print(e)
        else:
            print(f"{filename} is poorly formatted")
