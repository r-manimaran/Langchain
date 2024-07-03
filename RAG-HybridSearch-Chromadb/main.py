#from langchain.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
# from langchain.llms import HuggingFaceHub
from langchain_community.retrievers import BM25Retriever 

#from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers import EnsembleRetriever
import os
from dotenv import load_dotenv

load_dotenv()
#load the pdf
file_path = 'LangChainExamples.pdf'

#check file exists
if os.path.exists(file_path):
    print("file exists!")

data_file = UnstructuredPDFLoader(file_path=file_path)
docs = data_file.load()
print(f"loaded {len(docs)} documents")

# create chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
chunks = splitter.split_documents(docs)
print(f"created {len(chunks)} chunks")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# create and store embeddings
#embeddings = OpenAIEmbeddings()

embeddings = HuggingFaceInferenceAPIEmbeddings(
    model_id="sentence-transformers/all-MiniLM-L6-v2",    
    api_key=HF_TOKEN
)
db_path = "chromadb"
if not os.path.exists(db_path):
    print("Creating embeddings...")
    vectorstore = Chroma.from_documents(
    chunks,
    embeddings    
    )    
    print("Embeddings created and stored successfully")
else:
    print("Embeddings already exist, loading from file")
    vectorstore = Chroma.load(db_path)
    print("loaded existsing DB")

# vectorbase retriever
vectorstore_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#Keyword based search
keyword_retriever = BM25Retriever.from_documents(chunks,k=3)

#print(f'keyword retriever:{keyword_retriever}')
#Combine Vector Store Retriever and Keyword retriver using Ensemble
ensemble_retriever = EnsembleRetriever(
    retrievers=[vectorstore_retriever, keyword_retriever],
    weights=[0.5,0.5]
)

# Uses OpenAI for Answering. So defining the LLM here
llm = OpenAI(temperature=0.0,verbose=True)

template = """
<<|system|>>
You are a helpful assistant. Use the following context to answer the user's question.
Think step by step, before answering the query.
{context}

</s>
<<|user|>>
{query}
</s>

<|assistant|>

"""

prompt = ChatPromptTemplate.from_template(template=template)
output_parser = StrOutputParser()

# create chain using Langchain Expression language (LEL)
chain = ({
    "context":ensemble_retriever,
    "query": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
    )

# print(chain)
response = chain.invoke("About Biden")
print(response)
