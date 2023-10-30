import pandas as pd
import streamlit as st

# Load the dataset from the provided GitHub URL
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

df = load_data("https://github.com/rmkenv/ejchat/blob/main/ejtoolmatrix.csv?raw=true")

# Dictionary to hold tool names and their indicators
tool_indicators = {}

# Process the dataframe
for i in range(2, len(df), 2):  # Start from the third row, skipping 'Metric' and 'Source'
    tool_name = df.iloc[i]['Unnamed: 0'].split(' - ')[0]
    indicators = set()
    for col in df.columns[1:]:
        indicator = df.iloc[i][col]
        if pd.notna(indicator):
            indicators.add(indicator)
    tool_indicators[tool_name] = indicators

def compare_tool_indicators(tool1, tool2):
    """Function to compare indicators between two tools."""
    unique_to_tool1 = tool_indicators[tool1] - tool_indicators[tool2]
    unique_to_tool2 = tool_indicators[tool2] - tool_indicators[tool1]
    return unique_to_tool1, unique_to_tool2

# Streamlit app
st.title("Environmental Tools Indicator Comparison")

# Dropdown for selecting tools
tool_list = list(tool_indicators.keys())
tool1 = st.selectbox("Select the first tool:", tool_list)
tool2 = st.selectbox("Select the second tool:", tool_list)

# Button to compare indicators
if st.button("Compare Tools"):
    unique_to_tool1, unique_to_tool2 = compare_tool_indicators(tool1, tool2)
    st.write(f"Indicators unique to {tool1}:")
    st.write(unique_to_tool1)
    st.write(f"Indicators unique to {tool2}:")
    st.write(unique_to_tool2)
