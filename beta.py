import streamlit as st
import pandas as pd

# Load the data from the GitHub URL
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/rmkenv/ejchat/main/cleaned_ejtoolmatrix.csv'
    data = pd.read_csv(url)
    return data

data = load_data()

# Sidebar for tool selection
st.sidebar.header("Tool Selection")
tool1 = st.sidebar.selectbox("Select the first tool for comparison:", options=data['Indicator'].unique())
tool2 = st.sidebar.selectbox("Select the second tool for comparison:", options=data['Indicator'].unique())

# Filter data based on selections
filtered_data_tool1 = data[data['Indicator'] == tool1]
filtered_data_tool2 = data[data['Indicator'] == tool2]

# Display results
st.title("Environmental Metrics Comparison")

# Define a function to generate the response for a given tool and metrics as a dataframe-style table
def generate_response(tool, metrics):
    st.subheader(tool)
    st.dataframe(metrics)

