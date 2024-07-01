import chromadb
from chromadb.utils import embedding_functions
import json

import csv
import os


# Store the csv files line to a array
documents = []
# Store the metadata to a array
metadatas = []
# Store the unique id to a array
ids = []

#Load csv file
if os.path.exists('menu-items.csv'):
    print('File exists')
    # Open the CSV file for reading
    with open('menu-items.csv', 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        id=1
        # # Iterate over each row in the CSV
        # Iterate over each row in the csv using reader object
        for i, line in enumerate(reader):
            # Skip the header row
            if i == 0:
                continue
            # Add the document, metadata and id to the respective arrays
            documents.append(line[1])
            metadatas.append({'item_id': line[0]})
            ids.append(str(id))
            id+=1


# print(documents)
# create the Chroma Client
# client = chromadb.Client()
client = chromadb.PersistentClient(path='my_vectordb')
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction("all-mpnet-base-v2")
collection = client.get_or_create_collection("menu-items", embedding_function=sentence_transformer_ef)

# add the documents to the collection
collection.add(documents=documents, metadatas=metadatas, ids=ids)

# Query mispelled words
results = collection.query(
    query_texts=["sphagetti"],
    n_results=5,
    include=["documents", "distances","metadatas"]
)
print(results['documents'])

results = collection.query(
    query_texts=["chicken"],
    n_results=5,
    include=["documents", "distances","metadatas"]
)
print(results['documents'])
results = collection.query(
    query_texts=["shrimp"],
    n_results=5,
    include=["documents", "distances","metadatas"]
)
print(f"Search Result for shrimp:\n{results['documents']}")