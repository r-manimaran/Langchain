from langchain.agents import create_agent, create_react_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from faker import Faker
import random
import os
from dotenv import load_dotenv

load_dotenv()
fake = Faker()

# -- define the tools
@tool
def get_weather(location: str) -> str:
    """Get weather for a location"""
    conditions = ["sunny", "cloudy", "rainy", "windy", "snowy", "foggy"]
    temp = random.randint(-10, 40)
    condition = random.choice(conditions)
    humidity = random.randint(20, 95)
    return f"The weather in {location} is {condition}, {temp}°C, humidity {humidity}%"
@tool
def get_current_utc_time() -> str:
    """Get current UTC time"""
    from datetime import datetime
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# -- Create Agent
google_api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=google_api_key)
agent = create_agent(model, tools=[get_weather, get_current_utc_time])

# -- Test the agent
response = agent.invoke({"messages": [{"role": "user", "content": "What is the weather like in London and current time?"}]})
content = response["messages"][-1].content
if isinstance(content, list):
    print(content[0]["text"])
else:
    print(content)
