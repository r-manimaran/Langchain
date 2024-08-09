import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch
from langchain_community.document_loaders import AzureBlobStorageContainerLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

model = "text-embedding-ada-002"
vector_store_address = os.getenv("AZURE_AI_SEARCH_SERVICE_NAME")
vector_store_key = os.getenv("AZURE_AI_SEARCH_API_KEY")

embeddings:OpenAIEmbeddings = OpenAIEmbeddings(model=model, chunk_size=1)
index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME") #"langchain-vector-demo"
vector_store:AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_key,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

loader = AzureBlobStorageContainerLoader(
    conn_str=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    container="filescontainer",
)
print(loader)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
docs = text_splitter.split_documents(documents)
vector_store.add_documents(docs)
print("Data embedded and stored in Azure Search index.")


