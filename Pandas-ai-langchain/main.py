import streamlit as st
from pandasai import SmartDataframe
import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="PandasAI App", page_icon=":bar_chart:", layout="wide")
#define the LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
#Read Students data
students_df = pd.read_csv("Data/students.csv")
students_sdf = SmartDataframe(students_df, config={"llm": llm})

#read cars data
cars_df = pd.read_csv("Data/cars.csv")
cars_sdf = SmartDataframe(cars_df, config={"llm": llm})

st.title("PandasAI App to analyze student data")
options = ["Students", "Cars"]
choice = st.selectbox("Select an option", options)

if choice == "Students":
    question = st.text_input("Ask a question about the student data")
    if st.button("Get Answer"):
        st.write(students_sdf.chat(question))

if choice == "Cars":
    question = st.text_input("Ask a question about the car data")
    if st.button("Get Answer"):
        st.write(cars_sdf.chat(question))

