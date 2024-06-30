from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

# Tool 1 - Wikipedia 
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
print(f'1. Tool Name: {wiki.name}')

#Tool 2: Web Page Scrapper
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
load_dotenv()
loader = WebBaseLoader("https://docs.smith.langchain.com/")
docs = loader.load()
RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200).split_documents(docs)
#embeddings
embeddings = OpenAIEmbeddings()
# check for path not exists
# store the faiss Vector db locally and avoid recreating the embedding everytime... Some cost saving 
if not os.path.exists(f"web.faiss"):
    vector_db = FAISS.from_documents(docs, embeddings)
    vector_db.save_local(f"web.faiss")    
    print("Vector store saved successfully")

vectorstore = FAISS.load_local(f"web.faiss", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()
print(f'2. Tool Name: {retriever}')

from langchain.tools.retriever import create_retriever_tool
retriever_tool = create_retriever_tool(retriever, "langsmith_search", "Search for information about langsmith. For any questions about Langsmith, you can use this tool")
print(f'3. Tool Name: {retriever_tool.name}')

# Tool 4: Arxiv : where researchers upload their papers
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
api_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper)
print(f'4. Tool Name: {arxiv.name}')

# combine all the tools
# the results are searched in the order provided below
tools = [wiki, arxiv, retriever_tool]

#query from this tools using Agents
from langchain.agents import create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
llm = ChatOpenAI(temperature=0,verbose=True)
# Get the Already stored prompt from the hub
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_tools_agent(llm,tools,prompt=prompt)
# print(f'5. Prompt: {prompt}')

# execute the agent
from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# uncomment one by one and see the results from each tools automatically

# Below uses langsmith_search
# response =agent_executor.invoke({"input": "What is Langsmith?"}, include_run_info=True)
# print(f'6. Response: {response["output"]}')

# Below uses wikipedia
# response = agent_executor.invoke({"input": "USA Independance day"}, include_run_info=True)
# print(f'6. Response: {response["output"]}')

#Below uses Arxiv and search in research paper
response = agent_executor.invoke({"input": "What is the paper 1605.08386 talks about?"}, include_run_info=True)
print(f'6. Response: {response["output"]}')

# use streamlit app to get output and print response
import streamlit as st

st.title("Agent App")
query = st.text_input("Enter your query")
if st.button("Get Response"):
    response = agent_executor.invoke({"input": query}, include_run_info=True)
    st.write(response["output"])

