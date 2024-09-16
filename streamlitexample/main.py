import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data Dashboard")

#FileUpload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    data = pd.read_csv(uploaded_file)


    st.subheader("Data Preview")
    st.write(data.head())

    st.subheader("Data Summary")
    st.write(data.describe())

    st.subheader("Filter Data")
    columns = data.columns.tolist()
    selected_column = st.selectbox("Select a column", columns)
    unique_values = data[selected_column].unique()
    filter_value = st.selectbox("Enter a value to filter",unique_values)
    filtered_data = data[data[selected_column] == filter_value]
    st.write(filtered_data)
 

    #Plotting
    st.subheader("Data Visualization")
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)
    if st.button("Plot Data"):
        st.line_chart(filtered_data.set_index(x_column)[y_column])
else:
    st.write("Please upload a CSV file")  

## To This using Streamlit run as below
## streamlit run main.py