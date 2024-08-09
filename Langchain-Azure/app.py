# This is the streamlit app
# Run this app with `streamlit run app.py`
# Ensure the vectors are loaded to Azure Search AI
import streamlit as st
from streamlit_chat import message
from langchain_community.retrievers import AzureCognitiveSearchRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")


def load_chain():
    prompt_template = """ You are a helpful assistant for answering about the restaurant in the context

    {context}
    question :{question}
    Ans here:
    """
    prompt =  PromptTemplate.from_template(template=prompt_template)
    retriever = AzureCognitiveSearchRetriever(content_key="content", top_k="3")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, combine_docs_chain_kwargs={"prompt":prompt})
    return chain

chain = load_chain()

st.set_page_config(page_title="RAG Chatbot", page_icon=":robot:")
st.title("RAG Chatbot")
st.header("Langchain Azure Demo")

def get_input():
    input = st.text_input("You: ", key="input")
    return input

# Set the Session
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

user_input = get_input()

if user_input:   
    output = chain.invoke(question=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")