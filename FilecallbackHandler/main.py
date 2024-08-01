from langchain.callbacks import FileCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from dotenv import load_dotenv,find_dotenv
import os
import logging

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

os.environ["SERAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = load_tools(["serpapi"], llm=llm)
handler = FileCallbackHandler("output.txt")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    callbacks=[handler],
)
logger.info("Agent initialized")
logger.info(agent)

result = agent.run("Who win the ICC Mens T20 World cup recently?")
print(result)
logger.info(result)