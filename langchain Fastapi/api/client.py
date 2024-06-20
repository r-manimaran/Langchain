import requests
import streamlit as st

def get_openai_response(prompt):
    response = requests.post(
        "http://127.0.0.1:8000/essay/invoke",
        json={
            'input':{'topic':prompt}            
        })
    return response.json()['output']

### Streamlit app
st.title("Essay Generator")
input_prompt = st.text_input("Enter your prompt here")

if input_prompt:
    response = get_openai_response(input_prompt)
    st.write(response)