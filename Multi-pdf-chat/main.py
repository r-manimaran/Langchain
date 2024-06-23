import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAI
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(uploaded_files):
    text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator='\\n',
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks

def create_vectorstore(text_chunks):
    from langchain_openai.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def create_hf_vectorstore(text_chunks):
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def create_conversation_chain(vectorstore):
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationalRetrievalChain
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(temperature=0.7,verbose=True, max_tokens=1000),
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True,        
    )
    return conversation_chain

def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", "Please upload your documents first."), unsafe_allow_html=True)
    else:
        response = st.session_state.conversation({"question": user_question})
        st.session_state.chat_history = response["chat_history"]

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        # st.write(response)
     

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple Pdf", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple Pdf :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    st.write(user_template.replace("{{MSG}}","Hello Human"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello! I can answer questions about your documents."), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        uploaded_files = st.file_uploader("Upload your pdf doc here and click on Process button",
                                         accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # get the Pdf text
                raw_text = get_pdf_text(uploaded_files)
                ##st.write(raw_text)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                ##st.write(text_chunks)

                # create vector store
                #Vector store using FAISS and OpenAI
                vectorstore = create_vectorstore(text_chunks)

                # vector store using FAISS and HuggingFace
                ## vectorstore = create_hf_vectorstore(text_chunks)
                
                res = vectorstore.similarity_search("What is the pricing for GPT-3.5-Turbo?")
                print(res)
                retriever1=vectorstore.as_retriever()
                print("Printing from Retriever")
                print(retriever1.invoke("What is the pricing for GPT-3.5-Turbo?"))
                
                ## Create Conversation chain
                st.session_state.conversation = create_conversation_chain(vectorstore=vectorstore)
    

if __name__ == "__main__":
    main()