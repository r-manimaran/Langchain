from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ParentDocumentRetriever
from langchain_openai import OpenAIEmbeddings

## Text Splitting or DocLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()
# Load Document by document using TextLoader
loader =[
    TextLoader('data/ai.txt'),
    TextLoader('data/ai2.txt')
]
# Load all the documents in a Folder
# loader = DirectoryLoader('../data', glob='*.txt', loader_cls=TextLoader)
docs = []
print("Loading data....")
for doc in loader:
    docs.extend(doc.load())
# Retrieve full documents instead of chunks
child_splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap  = 50)

vector_store = Chroma(
    collection_name="full_documents",
    embedding_function=embeddings    
)
store = InMemoryStore()
print("Storing data....")

full_doc_retriever = ParentDocumentRetriever(vectorstore=vector_store,
                                             docstore= store,
                                             child_splitter=child_splitter)
full_doc_retriever.add_documents(docs, ids=None)
resp = list(store.yield_keys())
print(resp)

sub_docs = vector_store.similarity_search("What is Amazon Athena",k=2)
print("With Chucks --- Output")
print(len(sub_docs[0].page_content))
print(len(sub_docs))
print(sub_docs[0].page_content)
print("----------------")
print("With Full Doc --- Output")
retrieved_document = full_doc_retriever.invoke("What is Amazon Athena")
print(len(retrieved_document[0].page_content))
print(retrieved_document[0].page_content)

print("***********************************************")
## 2 Method - Retriving Larger Chunks
parent_splitter1 = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter1 = RecursiveCharacterTextSplitter(chunk_size=400)
vectorStore = Chroma(collection_name="split_parents",
                     embedding_function=embeddings,
                     )
store1 = InMemoryStore()
big_chucks_retriever = ParentDocumentRetriever(vectorstore=vectorStore,
                                               docstore=store1,
                                               child_splitter=child_splitter1,
                                               parent_splitter=parent_splitter1)
big_chucks_retriever.add_documents(docs)
resp1 = list(store1.yield_keys())
print(resp1)

sub_docs1 = vectorStore.similarity_search("What is Amazon Athena", k=2)
print("With Chucks --- Output") 
print(len(sub_docs1[0].page_content))
print(sub_docs1[0].page_content)

retrieved_document1 = big_chucks_retriever.invoke("What is Amazon Athena")
print("With Full Doc --- Output")
print(len(retrieved_document1[0].page_content))
print(retrieved_document1[0].page_content)

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=big_chucks_retriever
    )
query = "What is Amazon Athena"
response = qa.invoke(query)
print(f'Response:{response}')
