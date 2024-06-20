from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task",default="return a list of numbers?")
parser.add_argument("--language", default="python")
args = parser.parse_args()

## Here the Open API Key is taken from the .env file
# ensure the .env  variable names is  OPENAI_API_KEY

llm = OpenAI()


code_prompt = PromptTemplate(
    input_variables=["task"],
    template="Write a {language} code to {task}",
)

code_chain = LLMChain(llm=llm, prompt=code_prompt)

result =code_chain({
    "task": args.task,
    "language": args.language
})

print(result["text"])