import streamlit as st
import pandas as pd

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('ejmatrix_cleaned.csv')
    return data

df = load_data()

# Select Tools
tool_options = df['tool name'].unique()
selected_tools = st.multiselect('Select up to 3 tools to compare:', tool_options, default=tool_options[:3])

# Filter data based on selection
if selected_tools:
    filtered_df = df[df['tool name'].isin(selected_tools)]

    # Assuming that the DataFrame 'filtered_df' now contains the rows for the selected tools,
    # and each column (other than 'tool name' and maybe 'Affilation') represents a different indicator.
    # We need to highlight differences between the tools. This can be a complex task depending on the data's nature.
    # A simple way could be to transpose the data for better visualization.
    comparison_df = filtered_df.set_index('tool name').T

    st.dataframe(comparison_df.style.apply(lambda x: ["background: yellow" if v != x[0] else "" for v in x], axis=1))

# Instructions for running the Streamlit app
# Save this script as app.py and run it using the command: streamlit run app.py
