#Import Agents and Tools
from langchain.agents import initialize_agent, Tool, AgentType 
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities import TextRequestsWrapper
from langchain_openai import OpenAI

#import OpenAI API key and other required imports
import os
from dotenv import load_dotenv
from langchain.tools import BaseTool
import requests

load_dotenv()

#setup the LLM
llm = OpenAI(temperature=0.0)

# Tools to be added

def get_police_forces():
    # Fetch police force data from an API
    url = "https://data.police.uk/api/forces"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_police_forces(name):
    # Search for a specific police force by name
    forces = get_police_forces()
    matching_forces = []
    if forces:
        for force in forces:
            if  name.lower() in force["name"].lower():
                matching_forces.append(force)

        return matching_forces
    
    return None

class search_police_force(BaseTool):
    name = "search_police_force"
    description = "Useful for when you need to search for a specific police force by name"

    def _run(self, query:str) -> str:
        # Use the search_police_force function to search for a police force
        forces = search_police_forces(query)
        return forces
    
    async def _arun(self, query:str) -> str:
        # Use the search_police_force function to search for a police force
        raise NotImplementedError("tool does not support async")
'''   
#example usuage
force_id = "devon"
police_force_data = search_police_forces(force_id)
print(police_force_data)
'''


def get_police_force_id(force_id):
    url=f'https://data.police.uk/api/forces/{force_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
class get_police_force_details(BaseTool):
    name = "get_police_force_details"
    description = "Useful for when you need to get details of a specific police force by ID"

    def _run(self, query:str) -> str:
        # Use the get_police_force_details function to get details of a police force
        force_details = get_police_force_id(query)
        return force_details

    async def _arun(self, query:str) -> str:
        # Use the get_police_force_details function to get details of a police force
        raise NotImplementedError("tool does not support async")

'''   
#example usuage
force_id = "devon-and-cornwall"
police_force_data = get_police_force_id(force_id)
print(police_force_data)
'''

def get_police_force_people(force_id):
    url=f'https://data.police.uk/api/forces/{force_id}/people'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
class get_police_force_peoples(BaseTool):
    name = "get_police_force_people"
    description = "Useful for when you need to get people details of a specific police force by ID"

    def _run(self, query:str) -> str:
        # Use the get_police_force_people function to get details of people in a police force
        force_people = get_police_force_people(query)
        return force_people

    async def _arun(self, query:str) -> str:
        # Use the get_police_force_people function to get details of people in a police force
        raise NotImplementedError("tool does not support async")
'''   
# example usage
force_id = "devon-and-cornwall"
police_force_data = get_police_force_people(force_id)
print(police_force_data)
'''   

def get_neighbourhoods(force_id):
    url =f'https://data.police.uk/api/{force_id}/neighbourhoods'
    cleaned_url = url.replace("'", "")
    response = requests.get(cleaned_url)
    neighbourhoods = response.json()

    if response.status_code == 200:
        names = [neighbourhood['name'] for neighbourhood in neighbourhoods]
        names_string = ', '.join(names)
        return names_string
    else:
        return None
    
class get_police_neighbourhoods(BaseTool):
    name = "get_police_neighbourhoods"
    description = "Useful for when you need to get a list of neighbourhoods in a specific police force by ID"

    def _run(self, query:str) -> str:
        # Use the get_neighbourhoods function to get a list of neighbourhoods in a police force
        neighbourhoods = get_neighbourhoods(query)
        return neighbourhoods

    async def _arun(self, query:str) -> str:
        # Use the get_neighbourhoods function to get a list of neighbourhoods in a police force
        raise NotImplementedError("tool does not support async")

'''     
#usage
force_id = "\'devon-and-cornwall\'"
neighbourhoods = get_neighbourhoods(force_id)
print(neighbourhoods)
'''

def locate_neighbourhood(latlong):
    url=f'https://data.police.uk/api/locate-neighbourhood?q={latlong}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
class locate_police_neighbourhood(BaseTool):
    name = "locate_police_neighbourhood"
    description = "Useful for when you need to locate a specific police force neighbourhood by latitude and longitude"

    def _run(self, query:str) -> str:
        # Use the locate_neighbourhood function to locate a neighbourhood in a police force
        neighbourhood = locate_neighbourhood(query)
        return neighbourhood

    async def _arun(self, query:str) -> str:
        # Use the locate_neighbourhood function to locate a neighbourhood in a police force
        raise NotImplementedError("tool does not support async")
'''   
# example usage
latlong = "51.509865,-0.118092"
neighbourhood_data = locate_neighbourhood(latlong)
print(neighbourhood_data)
'''

#Load the tools config that are needed

tools =[
    Tool(
        name="search_police_force",
        func=search_police_force().run,
        description="Useful for when you need to search for a specific police force by name"
    ),
    Tool(
        name="get_police_force_details",
        func=get_police_force_details().run,
        description="Useful for when you need to get details of a specific police force by ID"
    ),
    Tool(
        name="get_police_force_people",
        func=get_police_force_peoples().run,
        description="Useful for when you need to get people details of a specific police force by ID"
    ),
    Tool(
        name="get_police_neighbourhoods",
        func=get_police_neighbourhoods().run,
        description="Useful for when you need to get a list of neighbourhoods in a specific police force by ID"
    ),
    Tool(
        name="locate_police_neighbourhood",
        func=locate_police_neighbourhood().run,
        description="Useful for when you need to locate a specific police force neighbourhood by latitude and longitude"
    ),
]

tools = [search_police_force(),get_police_force_details(),get_police_neighbourhoods(), locate_police_neighbourhood()]
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
response = agent.run("Get the contact number for latitude 50.365, longitude -4.1423 police station")
print(response)