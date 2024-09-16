import streamlit as st
st.title("My Streamlit App - Title")
st.header("My Streamlit App- Heading")
st.subheader("My Streamlit App - subheading")

st.checkbox("yes")
st.button("Click")
st.radio("Pick your gender", ["Male", "Female"])
st.selectbox("Pick your gender", ["Male", "Female"])

st.success("You did it!")