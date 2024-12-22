import pysolr
import re

import nltk.corpus
nltk.download('wordnet')
from nltk.corpus import wordnet

solr_url = "http://localhost:8983/solr/BM25_sans_pret"

topics_file_path = r"TREC-AP-88-90\Topics-requetes\topics.1-150.txt"
results_file_path = r"C:\Documents\UQAM\INF7546\Projet1\trec_eval-9.0.7\solrman\BM25_avec_pret_long.txt" 

rows = 1000
topic_titles=[]

def parse_topics(file_path):
    with open(file_path, 'r') as f:
        content = f.read().split("<top>")
        return [parse_topic(entry) for entry in content if entry.strip()]

def parse_topic(topic_entry):

    #choisir l'option "title" qui correspond au type de requête désiré
    #option requête courte
    #title = re.search(r"<title>\s*Topic:\s*(.*)", topic_entry).group(1)

    #option requête longue
    title = re.search(r"<title>\s*Topic:\s*(.*)", topic_entry).group(1) + ' ' + re.search(r"<desc>\s*Description:\s*((.*\n)*?)<", topic_entry).group(1).replace(':','')
    
    num = re.search(r"<num>\s*Number:\s*(\d+)", topic_entry).group(1)
    topic_titles.append([num,title.strip()])
    return {"num": int(num), "title": title.strip()}

def query_solr(query):
    solr = pysolr.Solr(solr_url)
    params = {
        "fl": "id,score",
        "rows": rows,
        "echoParams": "all",
        "debugQuery": "true",
        "df": "_text_pro_"
    }
        # changer le paramètre "df" à:
        # "_text_" pour BM25 sans prétraitement,
        # "_text_pro_" pour BM25 avec prétraitement,
        # "_idf_" pour tf*idf sans prétraitement,
        # "_idf_pro_" pour tf*idf avec prétraitement

    response = solr.search(q=query,**params)
    return response.docs

def expand_query(query):
    newquery=query
    for term in query.split():
        for s in range(2):
            try:
                synset=wordnet.synsets(term)[s]
                # Ajouter les synonymes
                try:
                    synset.lemmas()
                    synonym=synset.lemmas()[0].name().replace('_',' ')
                    newquery += ' ' + synonym
                except:
                    pass
                # Ajouter les hyperonymes
                try:
                    synset.hypernyms()[0].lemmas()
                    hlemma = synset.hypernyms()[0].lemmas()[0]
                    hypernym=hlemma.name().replace('_',' ')
                    newquery += ' ' + hypernym
                except:
                    pass
            except:
                pass
    return newquery

def write_results_to_file(topics, output_file):
    with open(output_file, 'w') as f:
        for topic in topics:
            query = topic["title"]
            # activer/commenter la prochaine ligne pour activer/déactiver l'expansion de requête
            #query=expand_query(query)
            query_id = topic["num"]
            results = query_solr(query)     
            for rank, doc in enumerate(results, start=1):
                doc_id = doc["id"].upper()
                score = doc["score"]
                f.write(f"{query_id} Q0{doc_id}{rank} {score} BM25_avec_pret_long\n")

topics = parse_topics(topics_file_path)

write_results_to_file(topics, results_file_path)

print(f"Results written to {results_file_path}")
