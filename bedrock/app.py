import boto3
import os
import sys
import json
import streamlit as st

from langchain.embeddings import BedrockEmbeddings

from langchain.llms.bedrock import Bedrock

# Data Ingestion
import numpy as np
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader


#vector Embedding and Vector Store
from langchain.vectorstores import FAISS

# LLM models from Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Bedrock client setup
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
bedrock_embeddings = BedrockEmbeddings(model_id='XXXXXXXXXXXXXXXXXXXXXX',
                                       client=bedrock)
#Data Ingestion
def data_ingestion():
    loader = PyPDFDirectoryLoader('data')
    documents = loader.load()

    # Splitting the data
    text_splitter = CharacterTextSplitter(chunk_size=10000, 
                                          chunk_overlap=1000)
    docs = text_splitter.split_documents(documents)
    return docs

#Vector Embedding and vector store
def vector_embedding(docs):
    embeddings = FAISS.from_documents(docs, bedrock_embeddings)
    embeddings.save_local('embeddings')


def get_claude_llm():
    # LLM model from Bedrock
    llm = Bedrock(model_id='XXXXXXXXXXXXXXXXXXXXXX',
                  client=bedrock,
                  model_kwargs={'temperature': 0.5,'max_tokens':512},
                  verbose=True)
    return llm

##get Llama2 LLM model
def get_llama2_llm():
    llm = Bedrock(model_id='XXXXXXXXXXXXXXXXXXXXXX',
                  client=bedrock,
                  model_kwargs={'temperature': 0.5,'max_gen_len':512},
                  verbose=True)
    return llm


prompt_template = """

Human: use the following pieces of context to answer the question at the end.Alteast summarize with 100 words
with brief explanation. If the question is not related to the context, say "I don't know", and 
don't try to make up an answer.
<context>
 {context}
</context>

Question: {question}
Assistant: 
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


#get the response
def get_response(question, llm, embeddings):
    chain = RetrievalQA.from_chain_type(llm=llm,
                                         chain_type="stuff",
                                         retriever=embeddings.as_retriever(search_type="similarity",search_kwargs={"k":3}),
                                         return_source_documents=True,
                                         chain_type_kwargs={"prompt": PROMPT}
                                        )
    ans = chain({"query":question})
    return ans["result"]

#create streamlit app
def main():
    st.set_page_config("Chat Pdf")
    st.header("Chat with PDF using AWS BedRock")
    st.title("Ask your question")
   

with st.sidebar:
    st.title("update or create Vector Store:")

    if st.button("Vector Update"):
        with st.spinner("Updating Vector Store..."):
            docs = data_ingestion()
            vector_embedding(docs)
            st.success("Vector Store Updated!")
    
    if st.button("Claude Output"):
        with st.spinner("Generating response..."):
            embeddings = FAISS.load_local('embeddings', bedrock_embeddings)
            question = st.text_input("Enter your question")
            llm = get_claude_llm()

            ans = get_response(question, llm, embeddings)
            st.write(ans)
            st.success("Response Generated!")

    if st.button("Llama2 Output"):
        with st.spinner("Generating response..."):
            embeddings = FAISS.load_local('embeddings', bedrock_embeddings)
            question = st.text_input("Enter your question")
            llm = get_llama2_llm()

            ans = get_response(question, llm, embeddings)
            st.write(ans)
            st.success("Response Generated!")

if __name__ == "__main__":
    main()  

