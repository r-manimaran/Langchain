from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

tools = load_tools(["serpapi"], llm=ChatOpenAI(temperature=0))
template = """You are an intellegent search agent who search in internet using Serpapi tool"""
prompt = ChatPromptTemplate.from_template(template)
agent = initialize_agent(
    tools,
    llm=ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    prompt=prompt
)
st.title("Langchain App to search in internet")
st.write("This app allows you to search in internet using Serpapi tool")
input_text = st.text_input("Search query", key="input")
submit = st.button("Search")
if submit:
    st.write(agent.run(input_text))
