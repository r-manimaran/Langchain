import os
import logging
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from enum import Enum
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.indexes import SQLRecordManager, index
import uvicorn

load_dotenv(find_dotenv())  # take environment variables from .env.

CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/vectordb"
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
namespace = f'pgvector/{COLLECTION_NAME}'

record_manager = SQLRecordManager(namespace,db_url=CONNECTION_STRING)
record_manager.create_schema()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"COLLECTION_NAME: {COLLECTION_NAME}")
logger.info(f"CONNECTION_STRING: {CONNECTION_STRING}")
logger.info(f"namespace: {namespace}")
class DocumentRequest(BaseModel):
    page_content: str
    metadata: dict

class CleanupMethod(str,Enum):
    incremental = "incremental"
    full = "full"

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0.0)
vectorStore = PGVector(collection_name= COLLECTION_NAME,
                       connection_string= CONNECTION_STRING,
                       embedding_function=embeddings)
prompt_template ="""
You are a helpful assistant for our resturant. Pease helps the user to find the answer to their question.
You will use the following pieces of context and answer the question:
{context}

Question: {question}
Answer here:
"""     
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)          

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorStore.as_retriever(),
    chain_type_kwargs=chain_type_kwargs    
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/index")
async def index_documents(request: list[DocumentRequest],
                          cleanup:CleanupMethod = CleanupMethod.incremental) -> dict:
    docs = [Document(
        metadata=req.metadata,
        page_content=req.page_content
    ) for req in request]

    result = index(docs,
                   record_manager,
                   vectorStore,
                   cleanup=cleanup.value,
                   source_id_key="source")
    return result

@app.post("/query")
async def query_endpoint(query: str) -> dict:
    result = qa.run(query = query)
    return {"result": result}

@app.get("/")
def read_root():
    return {"Hello": "World"}


if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=8000)