# Connecting Chains Together using LangChain and OpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import argparse
import argparse
import os
from dotenv import load_dotenv

load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument("--task", type=str, required=True,default="Print hello world")
parser.add_argument("--language", type=str, required=True, default="python")
args = parser.parse_args()

llm = OpenAI()

code_prompt = PromptTemplate(
    input_variables=["task","language"],
    template="Write a {language} code to {task}",
)

test_prompt = PromptTemplate(
    input_variables=["language","code"],
    template="Write a test cases for the {code} written in {language}",
)

code_chain = LLMChain(llm=llm,
                      prompt=code_prompt,
                      output_key="code")


test_chain = LLMChain(llm=llm,
                      prompt=test_prompt,
                      output_key="test")

chain = SequentialChain(chains=[code_chain, test_chain],
                        input_variables=["task","language"],
                        output_variables=["code","test"])
result = chain({
    "task": args.task,
    "language": args.language
})