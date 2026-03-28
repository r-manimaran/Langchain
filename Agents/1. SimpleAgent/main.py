import os
from dotenv import load_dotenv
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

load_dotenv()
secret_key = os.getenv("GOOGLE_API_KEY")

def main():
    print("Hello from 1-simpleagent!")
    print("Langchain version", langchain.__version__)
    model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=secret_key)
    course_agent = create_agent(model = model)
    response = course_agent.invoke(
        { "messages":[
                {
                "role":"user",
                "content":"Can you provide 3 topic on Agentic AI using Langchain? Answer in less than 100 words"
                }
                ]
        })
    content = response["messages"][-1].content
    if isinstance(content, list):
        print(content[0]["text"])
    else:
        print(content)


if __name__ == "__main__":
    main()
