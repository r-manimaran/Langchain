from langchain_openai import OpenAI

api_key = "API Key Goes here"

llm = OpenAI(temperature=0, openai_api_key=api_key)

result = llm("What is the meaning of life?")
print(result)