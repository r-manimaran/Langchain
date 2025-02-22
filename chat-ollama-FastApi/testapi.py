import requests
from dotenv import load_dotenv
import os
load_dotenv()

url="http://localhost:8000/generate?prompt=hello"
headers ={"x-api-key":os.getenv("API_KEY"),"Content-Type":"application/json"}

response = requests.get(url,headers=headers)
print(response.json())