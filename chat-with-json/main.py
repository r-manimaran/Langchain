from dotenv import load_dotenv, find_dotenv
import json
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.agent_toolkits import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec

load_dotenv(find_dotenv())

# load the Json file
json_filename = "openai-openapi-spec.json"
with open(json_filename, "r") as f:
    data = json.load(f)
    f.close()

spec = JsonSpec(dict_=data, max_value_length=4000)
toolkit = JsonToolkit(spec=spec)
agent = create_json_agent(llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"), toolkit=toolkit, verbose=True)
response = agent.run("How many endpoints are there?")
print(response)