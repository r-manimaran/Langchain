
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from dotenv import load_dotenv  


load_dotenv()


chat = ChatOpenAI(temperature=0)

memory = ConversationBufferMemory(
    memory_key="messages",
    return_messages=True,
    chat_memory=FileChatMessageHistory("history.json")
)
prompt = ChatPromptTemplate(
    input_variables=["content","messages"],
    messages =[
        MessagesPlaceholder(variable_name="messages"),
        SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(llm=chat, 
                 prompt=prompt,
                 memory=memory)
while True:
    content =input(">> ")

    result = chain(
        {"content":content})
    
    print(result["text"])
