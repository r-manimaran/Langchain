import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from langchain.callbacks import get_openai_callback

# Load the environment variable details from .env
load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(
    page_title="Streaming Streamlit application",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)
st.title("Streaming the Output from LLM")

# function for getting response
def get_response(query, chat_history):
    template = """
            You are a helpful assistant.
            Answer the following question based on the following chat history of the conversation:
            
            Conversation: {chat_history}
            
            user question: {question}
             """
    prompt = ChatPromptTemplate.from_template(template)
    # load the LLM model
    llm = OpenAI(temperature=0.0)
    output_parser = StrOutputParser()
    # create a chain and set the values for the variables
    # uses the Langchain Expression Language (LCEL)
    chain = prompt | llm | output_parser
    # response = chain.invoke({"question": query, "chat_history": chat_history})
    response = chain.stream({"question": query, "chat_history": chat_history})           
       
    return response

# Show the conversation from the chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.chat_message("Human").markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("AI").markdown(message.content)

user_input = st.chat_input("Enter the Query")
if user_input is not None and user_input !="":
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("Human"):
        st.markdown(user_input)

    with st.chat_message("AI"):
        # get the response from the LLM model
        #response = get_response(user_input, st.session_state.chat_history)
        #st.markdown(response)
        response = st.write_stream(get_response(user_input, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(response))




    


