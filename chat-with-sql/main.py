##check the version of python packages using Pip commnad
#pip freeze | grep langchain

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain_openai import OpenAI
from langchain.agents.agent import AgentType
from langchain.agents.agent_toolkits import  SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
from langchain_community.callbacks import get_openai_callback

import streamlit as st
from dotenv import load_dotenv
import os

st.set_page_config(page_title="SQL Query", page_icon=":robot:")
st.header("SQL Query")
load_dotenv()

query = st.text_input("Ask here about your database")

# Enterprise DB to be used
DRIVER = "ODBC Driver 17 for SQL Server"
USERNAME = "sa"
PSSWD = "passwordhere"  # replace with your password
# SQL Server instance name
SERVERNAME = "DARSHAN-PC"
INSTANCENAME = "\SQLEXPRESS"
DB = "GasExpense"
TABLE = "GasExpenses"


conn_executemany = create_engine(
    f"mssql+pyodbc://{USERNAME}:{PSSWD}@{SERVERNAME}{INSTANCENAME}/{DB}?driver={DRIVER}", fast_executemany=True
)

db = SQLDatabase(conn_executemany)
llm = ChatOpenAI(temperature=0.0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
toolkit.get_tools()

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        you are a very intelligent AI assistant who is expert in identifing relevant questions from user and converting into sql queriers to generate coorect answer.
        Please use the belolw context to write the microsoft sql queries, dont use mysql queries.
        context:
        you must query against the connected database,it has 1 table GasExpenses.
        """
        ),
        ("user","{question}\ ai: ")
    ]

        )

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    prefix="Agent",
    agent="zero-shot-react-description",
    format_instructions=False,
    max_execution_time=100,
    max_iterations=1000
)

if st.button("Submit"):
     with st.spinner("Generating response..."):
        with get_openai_callback() as cb:
            response = agent.invoke({"input": query}, include_run_info=True)
            print(cb)
            st.sidebar.success(f"Total Tokens: {cb.total_tokens}")
            st.sidebar.success(f"Prompt Tokens: {cb.prompt_tokens}")
            st.sidebar.success(f"Completion Tokens: {cb.completion_tokens}")
            st.sidebar.success(f"Total Cost (USD): ${cb.total_cost}")
        st.write(response["output"])




