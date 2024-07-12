from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import requests

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()
loading = DirectoryLoader("./Data", glob="**/*.txt", loader_cls=TextLoader)
docs = loading.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
documents = text_splitter.split_documents(docs)
print(len(documents))
docs_data = [doc.dict() for doc in documents]

url="http://127.0.0.1:8000//index?cleanup=full"
response = requests.post(url, json=docs_data)
print(response.json())