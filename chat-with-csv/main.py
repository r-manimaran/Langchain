import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain_openai import OpenAI
from dotenv import load_dotenv
import tabulate

def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your CSV", page_icon=":smiley:")
    st.header("Ask your CSV")

    user_csv = st.file_uploader("Upload your CSV file", type=["csv"])
    st.write("File uploaded successfully")
    if user_csv is None:
            st.write("Please upload a CSV file")
            return
    user_question = st.text_input("Ask a question about your CSV")
    if user_question is None:
        st.write("Please ask a question")
        return
    
    if st.button("Ask"):
        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True, allow_dangerous_code=True)
        response = agent.run(user_question)
        st.write(response)




if __name__ == "__main__":
    main()

## Run the Streamlit app
## > Streamlit run main.py