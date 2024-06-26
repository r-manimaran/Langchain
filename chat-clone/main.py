import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_chat import message as st_message

from langchain_openai import ChatOpenAI
from langchain.globals import get_verbose
from langchain.callbacks import get_openai_callback

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    # load the environment file data
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") =="":
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
        exit(1)
    else:
        print("OPENAI_API_KEY is set.")

    st.set_page_config(
        page_title="ChatGPT",
        page_icon=":robot:"
    )
    st.title("Chat Like ChatGPT")
    st.sidebar.header("Instructions")
    st.sidebar.markdown("1. Type your chat message in the text box")
    st.sidebar.markdown("2. Click Enter to Submit")
    st.sidebar.markdown("3. Wait for the response")

def main():
    
    init()
    # create a chat model
    chat = ChatOpenAI(temperature=0.7, verbose=get_verbose())
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
       
        ]

    
    with st.sidebar:
        user_input = st.text_input("Enter your message", key="user_input")
    
    if user_input:
        #st_message(user_input, is_user=True)
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Waiting for response..."):
            with get_openai_callback() as cb:
                response = chat.invoke(st.session_state.messages)
                st.sidebar.success(f"Total Tokens: {cb.total_tokens}")
                st.sidebar.success(f"Prompt Tokens: {cb.prompt_tokens}")
                st.sidebar.success(f"Completion Tokens: {cb.completion_tokens}")
                st.sidebar.success(f"Total Cost (USD): ${cb.total_cost}")  
        
        response_content = response.content        
       # st_message(response_content, is_user=False)
        st.session_state.messages.append(AIMessage(response_content))
    
    messages = st.session_state.get("messages", [])
    if messages:
        for i, message in enumerate(messages):
            # This is a message from the user
            if isinstance(message, HumanMessage):
                st_message(message.content, is_user=True, key=str(i)+"_user")
            elif isinstance(message, SystemMessage):
                st_message(message.content, is_user=False, key=str(i+1)+"_sys")
            elif isinstance(message, AIMessage):
                st_message(message.content, is_user=False,key=str(i+1)+"_ai")
            




if __name__ == "__main__":
    main()

# run the app using
# streamlit run main.py