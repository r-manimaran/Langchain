from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import ollama
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Lanchain Server",
              version="0.1",
              description="Lanchain server for serving LLMs")

add_routes(app, 
           ChatOpenAI(),
           path="/openai")
model =ChatOpenAI()
'''
##ollama llam2
llm = ollama(model="llama2")
'''
prompt1 = ChatPromptTemplate.from_template("Write an essay about {topic} with 100 worrds")

##prompt2 = ChatPromptTemplate.from_Template("Write a poem about {topic} with 100 words")

add_routes(app,
           prompt1|model,
           path="/essay")
'''
add_routes(app,
           prompt2|model,
           path="/poem")
'''
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)