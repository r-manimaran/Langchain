from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

#enable logging
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#logger.log("Logging Started")

def get_completion(topic, model="gpt-4o-mini"):
    """Get completion from OpenAI API with specified prompt and model."""
    llm = ChatOpenAI(model=model, temperature=0.8, max_tokens=5000)
    output_parser = StrOutputParser()
    prompt = PromptTemplate.from_template("""You are a experienced computer programmer and Architect.
                                       Provide me 20 real world scenario type interview questions and answers on {topic}
                                       Split it in to basic and advanced questions in the response.
                                      """)
    chain = prompt | llm | output_parser
    return chain.invoke({"topic": topic})

import streamlit as st
st.set_page_config(page_title="Interview Question Generator", page_icon=":robot:")
st.title("Interview Question Generator")
topic = st.text_input("Enter the topic for the interview questions")
if st.button("Generate"):
    logging.info("----------------------")
    logging.info(f"Topic: {topic}")
    logging.info("----------------------")
    response = get_completion(topic=topic)
    logging.info(response)
    st.write(response)
# response  = get_completion(topic="Python Fastapi")
# #logger.info(response)
# print(response)

