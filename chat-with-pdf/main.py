import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

import pickle
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="Chat with Pdf", page_icon=":robots:", layout="wide")

##side bar components
with st.sidebar:
    st.title("About")
    st.write("Chat with Pdf 🚀")
    
    add_vertical_space(5)
    st.write("Created by Manimaran [Blog](https://rmanimaran.wordpress.com)")

import threading

class PicklableFAISS(FAISS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.RLock()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.RLock()



def main():
    st.title("Chat with Pdf")
    pdf = st.file_uploader("Upload a PDF", type="pdf")
    if pdf is not None:
        st.write("PDF uploaded successfully")
        # You can now use the 'pdf' object to process the PDF file
        pdf_reader = PdfReader(pdf)
        st.write("Number of pages:", len(pdf_reader.pages))
        # extract the text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        chunks = text_splitter.split_text(text)
        st.write("Number of chunks:", len(chunks))
        store_name = pdf.name[:-4]
        # check if the vector store already exists
        if os.path.exists(f"{store_name}.faiss"):
            st.write("Vector store already exists")
            vectorstore = FAISS.load_local(f"{store_name}.faiss", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        else:
            st.write("Creating vector store...")
            #embeddings
            embeddings = OpenAIEmbeddings()
            #vectorstore = PicklableFAISS.from_texts(chunks, embeddings)
            vectorstore = FAISS.from_texts(chunks, embeddings)
            # store the vector for the pdf and save using picke
            
            vectorstore.save_local(f"{store_name}.faiss")
            st.write("Vector store saved successfully")

            #load the vector store
            vectorstore = FAISS.load_local(f"{store_name}.faiss", embeddings, allow_dangerous_deserialization=True)
            st.write("Vector store loaded successfully")

        #Accept user question
        query = st.text_input("Ask a question about your PDF:")
        if query:
            docs = vectorstore.similarity_search(query,k=3)
            #st.write(docs)
            #st.write("Answer:", docs)
            # Now create the chain and pass to LLM
            llm = OpenAI(temperature=0)
            chain = load_qa_chain(llm, chain_type="stuff")
            # Run the chain and get the response
            with st.spinner("Generating response..."):
                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=query)
                    st.sidebar.success(f"Total Tokens: {cb.total_tokens}")
                    st.sidebar.success(f"Prompt Tokens: {cb.prompt_tokens}")
                    st.sidebar.success(f"Completion Tokens: {cb.completion_tokens}")
                    st.sidebar.success(f"Total Cost (USD): ${cb.total_cost}")   
                st.write(response)
    else:
        st.write("Please upload a PDF file")

if __name__ == "__main__":
    main()